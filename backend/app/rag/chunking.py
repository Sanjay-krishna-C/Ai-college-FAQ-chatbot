import re
from dataclasses import dataclass
from typing import List, Dict, Any

from app.rag.extractor import ExtractedPage


@dataclass
class DocumentChunk:
    """
    A single granular text chunk with rich provenance metadata and deterministic ID.
    """
    chunk_id: str
    text: str
    document_name: str
    source_file: str
    page_number: int
    document_category: str
    academic_year: str
    regulation: str
    program: str
    source_type: str
    document_status: str
    chunk_index_in_page: int

    def to_metadata(self) -> Dict[str, Any]:
        """
        Convert to metadata dictionary format compatible with ChromaDB.
        Note: ChromaDB requires string, int, float, or bool values in metadata.
        """
        return {
            "chunk_id": self.chunk_id,
            "document_name": self.document_name,
            "source_file": self.source_file,
            "page_number": self.page_number,
            "document_category": self.document_category,
            "academic_year": self.academic_year or "unknown",
            "regulation": self.regulation,
            "program": self.program,
            "source_type": self.source_type,
            "document_status": self.document_status,
            "chunk_index": self.chunk_index_in_page
        }


class IntelligentChunker:
    """
    Paragraph and heading-aware chunker that splits document text
    into context-rich chunks while preserving semantic integrity and metadata.
    """

    def __init__(self, target_chunk_size: int = 700, chunk_overlap: int = 100):
        self.target_chunk_size = target_chunk_size
        self.chunk_overlap = chunk_overlap

    @staticmethod
    def generate_slug(text: str) -> str:
        """
        Convert file or regulation name into a clean, deterministic identifier slug.
        """
        clean = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-")
        return clean[:30].upper()

    def chunk_page(self, page: ExtractedPage) -> List[DocumentChunk]:
        """
        Split a single extracted page into semantic chunks with deterministic IDs.
        """
        if page.is_empty or not page.page_text:
            return []

        raw_text = page.page_text
        spec = page.spec

        # Split on double newlines (paragraphs) or clear section headers
        paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]

        chunks_text: List[str] = []
        current_chunk = ""

        for para in paragraphs:
            # If paragraph itself is very long, split on single newline or sentences
            if len(para) > self.target_chunk_size:
                sub_parts = re.split(r"(?<=[.!?])\s+", para)
                for part in sub_parts:
                    if not part.strip():
                        continue
                    if len(current_chunk) + len(part) < self.target_chunk_size:
                        current_chunk = f"{current_chunk}\n{part}" if current_chunk else part
                    else:
                        if current_chunk:
                            chunks_text.append(current_chunk.strip())
                        current_chunk = part
            else:
                if len(current_chunk) + len(para) < self.target_chunk_size:
                    current_chunk = f"{current_chunk}\n\n{para}" if current_chunk else para
                else:
                    if current_chunk:
                        chunks_text.append(current_chunk.strip())
                    # Apply small overlap if previous chunk exists
                    overlap_seed = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else ""
                    current_chunk = f"... {overlap_seed}\n{para}" if overlap_seed else para

        if current_chunk.strip():
            chunks_text.append(current_chunk.strip())

        # Construct DocumentChunk objects with deterministic IDs
        reg_slug = self.generate_slug(spec.regulation or "GEN")
        file_slug = self.generate_slug(page.source_file.replace(".pdf", ""))

        result_chunks: List[DocumentChunk] = []
        for idx, text in enumerate(chunks_text):
            # Deterministic ID format: BIT-{REG}-{FILE_SLUG}-p{PAGE:03d}-c{INDEX:02d}
            chunk_id = f"BIT-{reg_slug}-{file_slug}-p{page.page_number:03d}-c{idx+1:02d}"

            result_chunks.append(
                DocumentChunk(
                    chunk_id=chunk_id,
                    text=text,
                    document_name=page.document_name,
                    source_file=page.source_file,
                    page_number=page.page_number,
                    document_category=spec.document_category,
                    academic_year=spec.academic_year or "unknown",
                    regulation=spec.regulation,
                    program=spec.program,
                    source_type=spec.source_type,
                    document_status=spec.document_status,
                    chunk_index_in_page=idx + 1
                )
            )

        return result_chunks
