# CampusAI RAG Package
from app.rag.metadata import DATASET_REGISTRY, DocumentSpec, get_document_spec
from app.rag.extractor import PDFExtractor, ExtractedPage
from app.rag.chunking import IntelligentChunker, DocumentChunk
from app.rag.embeddings import GeminiEmbeddingService, GeminiEmbeddingError
from app.rag.vector_store import ChromaVectorStore
from app.rag.ingestion import IngestionPipeline

__all__ = [
    "DATASET_REGISTRY",
    "DocumentSpec",
    "get_document_spec",
    "PDFExtractor",
    "ExtractedPage",
    "IntelligentChunker",
    "DocumentChunk",
    "GeminiEmbeddingService",
    "GeminiEmbeddingError",
    "ChromaVectorStore",
    "IngestionPipeline",
]
