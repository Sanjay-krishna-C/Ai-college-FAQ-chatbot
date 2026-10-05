import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import pypdf

from app.core.logging import logger
from app.rag.metadata import DocumentSpec, get_document_spec


@dataclass
class ExtractedPage:
    """
    Structured extraction result for a single page of a PDF.
    """
    document_name: str
    source_file: str
    page_number: int  # 1-indexed
    page_text: str
    is_empty: bool
    spec: DocumentSpec


class PDFExtractor:
    """
    Robust PDF text extractor that preserves page-level provenance,
    cleans extraction artifacts, and retains structural headings/paragraphs.
    """

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean common PDF extraction artifacts while preserving paragraph structure.
        """
        if not text:
            return ""

        # Normalize unicode ligatures or common extraction glitches
        cleaned = text.replace("\u00a0", " ")
        cleaned = cleaned.replace("/t_i.liga", "ti")
        cleaned = cleaned.replace("\ufeff", "")
        cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")

        # Replace excessive multiple blank lines (keep max 2 newlines)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

        # Collapse excessive inline spaces (more than 2 spaces -> single space)
        cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)

        return cleaned.strip()

    def extract_document(self, file_path: Path) -> List[ExtractedPage]:
        """
        Extract all pages from a single PDF document.
        """
        file_name = file_path.name
        spec = get_document_spec(file_name)
        extracted_pages: List[ExtractedPage] = []

        if not file_path.exists():
            logger.error(f"PDF file not found: {file_path}")
            return []

        try:
            reader = pypdf.PdfReader(str(file_path))
            total_pages = len(reader.pages)

            for page_idx in range(total_pages):
                page_num = page_idx + 1
                try:
                    raw_text = reader.pages[page_idx].extract_text() or ""
                    cleaned = self.clean_text(raw_text)
                    is_empty = len(cleaned) < 15

                    extracted_pages.append(
                        ExtractedPage(
                            document_name=spec.document_name,
                            source_file=file_name,
                            page_number=page_num,
                            page_text=cleaned,
                            is_empty=is_empty,
                            spec=spec
                        )
                    )
                except Exception as page_err:
                    logger.warning(
                        f"Error extracting page {page_num} of {file_name}: {page_err}"
                    )
                    extracted_pages.append(
                        ExtractedPage(
                            document_name=spec.document_name,
                            source_file=file_name,
                            page_number=page_num,
                            page_text="",
                            is_empty=True,
                            spec=spec
                        )
                    )

            logger.info(
                f"Extracted {len(extracted_pages)} pages from {file_name} "
                f"({sum(1 for p in extracted_pages if not p.is_empty)} non-empty)"
            )

        except Exception as exc:
            logger.error(f"Failed to read PDF {file_name}: {exc}", exc_info=True)

        return extracted_pages
