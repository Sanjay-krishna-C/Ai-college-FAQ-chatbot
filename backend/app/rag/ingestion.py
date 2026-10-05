import sys
import time
from pathlib import Path
from typing import Dict, Any, List

from app.core.config import settings
from app.core.logging import logger
from app.rag.metadata import DATASET_REGISTRY
from app.rag.extractor import PDFExtractor
from app.rag.chunking import IntelligentChunker, DocumentChunk
from app.rag.embeddings import GeminiEmbeddingService, GeminiEmbeddingError
from app.rag.vector_store import ChromaVectorStore


class IngestionPipeline:
    """
    End-to-end institutional PDF ingestion pipeline for Gemini RAG (Phase 6B).
    Reads official college documents, extracts pages, chunks text,
    generates official Google Gemini embeddings, and persists to ChromaDB.
    """

    def __init__(self):
        self.dataset_dir = Path(settings.DATASET_DIRECTORY)
        self.extractor = PDFExtractor()
        self.chunker = IntelligentChunker(
            target_chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        self.embedding_service = GeminiEmbeddingService()
        self.vector_store = ChromaVectorStore(
            collection_name=settings.CHROMA_COLLECTION_NAME
        )

    def run(self, dry_run_if_no_key: bool = False) -> Dict[str, Any]:
        """
        Execute full ingestion across verified institutional documents using Gemini embeddings.
        """
        print("=================================================================")
        print("  CampusAI Phase 6B Gemini RAG Ingestion Pipeline")
        print("=================================================================")
        print(f"Dataset Directory : {self.dataset_dir}")
        print(f"Target Collection : {settings.CHROMA_COLLECTION_NAME}")
        print(f"Embedding Model   : {settings.EMBEDDING_MODEL}")
        print("-----------------------------------------------------------------")

        if not self.dataset_dir.exists():
            error_msg = f"Dataset directory not found at: {self.dataset_dir}"
            logger.error(error_msg)
            print(f"[ERROR] {error_msg}")
            return {"status": "error", "message": error_msg}

        # Step 0: Validate Gemini API credentials and detect embedding dimension
        if not self.embedding_service.is_configured():
            print("[ERROR] GEMINI_API_KEY is not configured or missing in backend/.env.")
            print("[STOP] Ingestion halted as required by Phase 6B: Gemini embeddings are strictly required.")
            print(">> Please add your GEMINI_API_KEY to backend/.env and re-run ingestion:")
            print(">> python -m app.rag.ingest")
            if not dry_run_if_no_key:
                return {
                    "status": "halted_missing_gemini_key",
                    "reason": "GEMINI_API_KEY environment variable is missing or empty in backend/.env"
                }

        detected_dim = 0
        if self.embedding_service.is_configured():
            try:
                print("Probing Gemini API and validating embedding dimension...")
                detected_dim = self.embedding_service.detect_dimension()
                print(f"[OK] Gemini embedding model verified. Dimension: {detected_dim}")
            except GeminiEmbeddingError as probe_err:
                print(f"[ERROR] Gemini API probe failed: {probe_err}")
                return {
                    "status": "gemini_probe_failed",
                    "reason": str(probe_err)
                }

        # Classify files in dataset directory
        all_pdf_files = sorted([f for f in self.dataset_dir.iterdir() if f.name.endswith(".pdf")])
        total_considered = len(all_pdf_files)
        included_files: List[Path] = []
        excluded_files: List[Dict[str, str]] = []

        for pdf_path in all_pdf_files:
            file_name = pdf_path.name
            spec = DATASET_REGISTRY.get(file_name)
            if spec and spec.is_included_in_primary_rag:
                included_files.append(pdf_path)
            else:
                reason = spec.exclusion_reason if spec else "Not registered in primary institutional collection"
                excluded_files.append({"file": file_name, "reason": reason})

        print("\nDocument Discovery Summary:")
        print(f"   * Total PDFs Considered : {total_considered}")
        print(f"   * Included for RAG      : {len(included_files)}")
        print(f"   * Excluded              : {len(excluded_files)}")

        # Step 1 & 2: Extract text and chunk
        total_pages = 0
        empty_pages = 0
        all_chunks: List[DocumentChunk] = []
        failed_documents = 0

        print("\nExtracting text and chunking included documents...")
        for pdf_path in included_files:
            try:
                pages = self.extractor.extract_document(pdf_path)
                total_pages += len(pages)
                doc_chunks = 0
                for page in pages:
                    if page.is_empty:
                        empty_pages += 1
                        continue
                    chunks = self.chunker.chunk_page(page)
                    all_chunks.extend(chunks)
                    doc_chunks += len(chunks)

                print(f"   [OK] {pdf_path.name[:45]:<45} | {len(pages):>3} pages | {doc_chunks:>3} chunks")
            except Exception as e:
                failed_documents += 1
                logger.error(f"Failed processing {pdf_path.name}: {e}")
                print(f"   [FAIL] {pdf_path.name[:45]:<45} | FAILED: {e}")

        print("\nChunking Results:")
        print(f"   * Total Pages Processed : {total_pages}")
        print(f"   * Empty/Unread Pages    : {empty_pages}")
        print(f"   * Total Chunks Created  : {len(all_chunks)}")

        # Step 3: Embed and Store incrementally in batches
        chunks_stored = 0
        batch_size = 40

        if self.embedding_service.is_configured() and all_chunks:
            print(f"\nGenerating Gemini Embeddings ({settings.EMBEDDING_MODEL}) & Upserting into ChromaDB...")
            print(f"Target Collection: {settings.CHROMA_COLLECTION_NAME}")

            total_chunks = len(all_chunks)
            for b_idx in range(0, total_chunks, batch_size):
                chunk_batch = all_chunks[b_idx:b_idx + batch_size]
                batch_ids = [c.chunk_id for c in chunk_batch]

                # Check if this batch is already indexed in ChromaDB
                try:
                    existing = self.vector_store.collection.get(ids=batch_ids, include=[])
                    existing_set = set(existing.get("ids", []))
                except Exception:
                    existing_set = set()

                unindexed_chunks = [c for c in chunk_batch if c.chunk_id not in existing_set]

                if not unindexed_chunks:
                    print(f"   [SKIP] Chunks {b_idx+1}-{min(b_idx+batch_size, total_chunks)} of {total_chunks} already indexed.")
                    chunks_stored += len(chunk_batch)
                    continue

                unindexed_texts = [c.text for c in unindexed_chunks]
                try:
                    embeddings = self.embedding_service.embed_texts(unindexed_texts, batch_size=batch_size)
                    self.vector_store.upsert_chunks(unindexed_chunks, embeddings=embeddings)
                    chunks_stored += len(unindexed_chunks)
                    print(f"   [INDEXED] Chunks {b_idx+1}-{min(b_idx+batch_size, total_chunks)} of {total_chunks} stored (768 dim).")
                    time.sleep(1.0)
                except GeminiEmbeddingError as emb_err:
                    print(f"   [ERROR] Embedding generation failed: {emb_err}")
                    return {
                        "status": "embedding_failed",
                        "reason": str(emb_err)
                    }
        else:
            print("\n[NOTE] Dry-run complete. Embeddings generation paused pending GEMINI_API_KEY.")

        # Final Summary Print
        print("\n" + "=" * 65)
        print("  INGESTION SUMMARY REPORT")
        print("=" * 65)
        print(f"Target Collection   : {settings.CHROMA_COLLECTION_NAME}")
        print(f"Documents processed : {len(included_files)}")
        print(f"Pages processed     : {total_pages}")
        print(f"Chunks created      : {len(all_chunks)}")
        print(f"Embeddings generated: {len(embeddings)}")
        print(f"Chunks stored       : {chunks_stored}")
        print(f"Embedding dimension : {detected_dim or 'N/A'}")
        print(f"Failed documents    : {failed_documents}")
        print("=" * 65)

        return {
            "status": "success" if self.embedding_service.is_configured() else "prepared_awaiting_key",
            "collection_name": settings.CHROMA_COLLECTION_NAME,
            "total_considered": total_considered,
            "included_count": len(included_files),
            "excluded_count": len(excluded_files),
            "excluded_details": excluded_files,
            "pages_processed": total_pages,
            "empty_pages": empty_pages,
            "chunks_created": len(all_chunks),
            "embeddings_generated": len(embeddings),
            "chunks_stored": chunks_stored,
            "embedding_dimension": detected_dim,
            "failed_documents": failed_documents,
            "collection_stats": self.vector_store.get_stats()
        }


def main():
    pipeline = IngestionPipeline()
    dry_run = "--dry-run" in sys.argv or "--check" in sys.argv
    result = pipeline.run(dry_run_if_no_key=dry_run)
    sys.exit(0 if result.get("status") in ["success", "prepared_awaiting_key"] else 1)


if __name__ == "__main__":
    main()
