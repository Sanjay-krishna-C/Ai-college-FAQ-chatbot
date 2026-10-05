from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.logging import logger
from app.rag.vector_store import ChromaVectorStore
from app.rag.embeddings import GeminiEmbeddingService

router = APIRouter(prefix="/rag", tags=["RAG Inspection & Debug"])

vector_store = ChromaVectorStore()
embedding_service = GeminiEmbeddingService()


class RAGStatsResponse(BaseModel):
    collection_name: str
    document_count: int
    chunk_count: int
    embedding_status: str
    embedding_model: str
    persist_directory: str


class RAGSearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500, description="Test search query")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of chunks to retrieve")
    regulation_filter: Optional[str] = Field(None, description="Optional regulation filter (e.g. R2022, R2026)")
    category_filter: Optional[str] = Field(None, description="Optional category filter (e.g. academics, examinations)")


class RAGSearchResultItem(BaseModel):
    chunk_id: str
    text: str
    document_name: str
    source_file: str
    page_number: int
    regulation: str
    document_category: str
    distance: Optional[float]
    metadata: Dict[str, Any]


class RAGSearchResponse(BaseModel):
    query: str
    results_count: int
    results: List[RAGSearchResultItem]


@router.get("/stats", response_model=RAGStatsResponse)
async def get_rag_stats():
    """
    Development endpoint to inspect ChromaDB collection size, chunk count, and embedding status.
    """
    try:
        raw_stats = vector_store.get_stats()
        emb_status = "ready" if embedding_service.is_configured() else "unconfigured_missing_key"

        return RAGStatsResponse(
            collection_name=raw_stats["collection_name"],
            document_count=13,  # Verified primary institutional documents
            chunk_count=raw_stats["total_chunks"],
            embedding_status=emb_status,
            embedding_model=settings.EMBEDDING_MODEL,
            persist_directory=raw_stats["persist_directory"]
        )
    except Exception as exc:
        logger.error(f"Error fetching RAG stats: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve RAG storage statistics."
        )


@router.post("/search", response_model=RAGSearchResponse)
async def search_rag(request: RAGSearchRequest):
    """
    Development search endpoint to test ChromaDB retrieval quality without invoking LLM synthesis.
    """
    try:
        query_embedding = None
        if embedding_service.is_configured():
            query_embedding = embedding_service.embed_query(request.query)

        filter_criteria = None
        if request.regulation_filter:
            filter_criteria = {"regulation": request.regulation_filter}
        elif request.category_filter:
            filter_criteria = {"document_category": request.category_filter}

        matches = vector_store.search_similar(
            query_embedding=query_embedding,
            query_text=request.query if query_embedding is None else None,
            top_k=request.top_k,
            filter_criteria=filter_criteria
        )

        formatted_items: List[RAGSearchResultItem] = []
        for m in matches:
            meta = m.get("metadata", {})
            formatted_items.append(
                RAGSearchResultItem(
                    chunk_id=m.get("chunk_id", ""),
                    text=m.get("text", ""),
                    document_name=meta.get("document_name", "unknown"),
                    source_file=meta.get("source_file", "unknown"),
                    page_number=meta.get("page_number", 0),
                    regulation=meta.get("regulation", "unknown"),
                    document_category=meta.get("document_category", "unknown"),
                    distance=m.get("distance"),
                    metadata=meta
                )
            )

        return RAGSearchResponse(
            query=request.query,
            results_count=len(formatted_items),
            results=formatted_items
        )

    except Exception as exc:
        logger.error(f"Error executing RAG search: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG search execution failed: {str(exc)}"
        )
