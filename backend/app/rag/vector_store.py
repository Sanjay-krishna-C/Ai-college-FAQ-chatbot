from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings
from app.core.logging import logger
from app.rag.chunking import DocumentChunk


class ChromaVectorStore:
    """
    Persistent ChromaDB vector store manager for CampusAI institutional knowledge.
    Ensures persistent storage, deterministic upserting (idempotency), and metadata querying.
    """

    def __init__(
        self,
        persist_dir: Optional[str] = None,
        collection_name: Optional[str] = None
    ):
        self.persist_dir = Path(persist_dir or settings.CHROMA_PERSIST_DIRECTORY)
        self.collection_name = collection_name or settings.CHROMA_COLLECTION_NAME

        # Ensure directory exists outside dataset/
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Initializing Persistent ChromaDB client at: {self.persist_dir}")
        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Official Bannari Amman Institute of Technology knowledge collection"}
        )

    def get_stats(self) -> Dict[str, Any]:
        """
        Return current collection statistics for inspection.
        """
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "persist_directory": str(self.persist_dir),
            "total_chunks": count,
            "status": "ready"
        }

    def upsert_chunks(
        self,
        chunks: List[DocumentChunk],
        embeddings: Optional[List[List[float]]] = None,
        batch_size: int = 100
    ) -> int:
        """
        Idempotently insert or update document chunks with their metadata and embeddings.
        Prevents duplicate entries when re-running ingestion.
        """
        if not chunks:
            return 0

        total_stored = 0

        for i in range(0, len(chunks), batch_size):
            chunk_batch = chunks[i:i + batch_size]
            batch_ids = [c.chunk_id for c in chunk_batch]
            batch_docs = [c.text for c in chunk_batch]
            batch_metas = [c.to_metadata() for c in chunk_batch]
            batch_embeddings = embeddings[i:i + batch_size] if embeddings else None

            if batch_embeddings:
                self.collection.upsert(
                    ids=batch_ids,
                    documents=batch_docs,
                    metadatas=batch_metas,
                    embeddings=batch_embeddings
                )
            else:
                self.collection.upsert(
                    ids=batch_ids,
                    documents=batch_docs,
                    metadatas=batch_metas
                )

            total_stored += len(chunk_batch)

        logger.info(f"Upserted {total_stored} chunks into collection '{self.collection_name}' (Total in DB: {self.collection.count()})")
        return total_stored

    def search_similar(
        self,
        query_embedding: Optional[List[float]] = None,
        query_text: Optional[str] = None,
        top_k: int = 5,
        filter_criteria: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve top_k most similar document chunks matching query vector or text.
        """
        kwargs: Dict[str, Any] = {
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"]
        }

        if filter_criteria:
            kwargs["where"] = filter_criteria

        if query_embedding is not None:
            kwargs["query_embeddings"] = [query_embedding]
        elif query_text is not None:
            kwargs["query_texts"] = [query_text]
        else:
            raise ValueError("Either query_embedding or query_text must be provided.")

        results = self.collection.query(**kwargs)

        formatted_results: List[Dict[str, Any]] = []
        if not results or not results.get("ids") or not results["ids"][0]:
            return formatted_results

        ids = results["ids"][0]
        docs = results["documents"][0] if results.get("documents") else []
        metas = results["metadatas"][0] if results.get("metadatas") else []
        distances = results["distances"][0] if results.get("distances") else []

        for idx in range(len(ids)):
            formatted_results.append({
                "chunk_id": ids[idx],
                "text": docs[idx] if idx < len(docs) else "",
                "metadata": metas[idx] if idx < len(metas) else {},
                "distance": distances[idx] if idx < len(distances) else None
            })

        return formatted_results
