import os
import unittest
from pathlib import Path

from app.core.config import settings
from app.rag.metadata import DATASET_REGISTRY, get_document_spec
from app.rag.extractor import PDFExtractor
from app.rag.chunking import IntelligentChunker
from app.rag.vector_store import ChromaVectorStore


class TestRAGPipeline(unittest.TestCase):
    """
    Quality and regression tests for Phase 6A RAG Document Ingestion.
    """

    def setUp(self):
        self.dataset_dir = Path(settings.DATASET_DIRECTORY)
        self.extractor = PDFExtractor()
        self.chunker = IntelligentChunker(target_chunk_size=700, chunk_overlap=100)

    def test_01_metadata_classification(self):
        """Verify that all 16 PDFs are cataloged and separated correctly."""
        total_registered = len(DATASET_REGISTRY)
        self.assertEqual(total_registered, 16, f"Expected 16 registered PDFs, found {total_registered}")

        included = [s for s in DATASET_REGISTRY.values() if s.is_included_in_primary_rag]
        excluded = [s for s in DATASET_REGISTRY.values() if not s.is_included_in_primary_rag]

        self.assertEqual(len(included), 13, f"Expected 13 included documents, found {len(included)}")
        self.assertEqual(len(excluded), 3, f"Expected 3 excluded policy documents, found {len(excluded)}")

        # Verify regulation versions are distinct
        regulations = {s.regulation for s in included}
        self.assertIn("R2022", regulations)
        self.assertIn("R2026", regulations)
        self.assertIn("R2024", regulations)
        self.assertIn("R2021", regulations)

    def test_02_pdf_extraction_sample(self):
        """Verify extraction on UG regulation document."""
        ug_file = self.dataset_dir / "B.E.-B.Tech-Regulations-2022-Version-1_-18.09.2026.pdf"
        self.assertTrue(ug_file.exists(), f"File not found: {ug_file}")

        pages = self.extractor.extract_document(ug_file)
        self.assertEqual(len(pages), 30, f"Expected 30 pages, got {len(pages)}")
        self.assertFalse(pages[0].is_empty)
        self.assertIn("BANNARI AMMAN INSTITUTE OF TECHNOLOGY", pages[0].page_text)
        self.assertEqual(pages[0].spec.regulation, "R2022")

    def test_03_deterministic_chunk_ids(self):
        """Verify that chunk generation produces deterministic and unique IDs."""
        ug_file = self.dataset_dir / "Amendments_R2022_32-ACM.pdf"
        pages = self.extractor.extract_document(ug_file)
        chunks_run1 = self.chunker.chunk_page(pages[0])
        chunks_run2 = self.chunker.chunk_page(pages[0])

        self.assertEqual(len(chunks_run1), len(chunks_run2))
        for c1, c2 in zip(chunks_run1, chunks_run2):
            self.assertEqual(c1.chunk_id, c2.chunk_id)
            self.assertTrue(c1.chunk_id.startswith("BIT-R2022-"))

    def test_04_chromadb_persistence_and_idempotency(self):
        """Verify that ChromaDB upsert is idempotent and does not create duplicates."""
        test_store = ChromaVectorStore(
            persist_dir=str(Path(settings.CHROMA_PERSIST_DIRECTORY) / "test_store"),
            collection_name="test_idempotency_collection"
        )
        sample_page = self.extractor.extract_document(self.dataset_dir / "Amendments_R2022_32-ACM.pdf")[0]
        sample_chunks = self.chunker.chunk_page(sample_page)

        # First upsert
        count_first = test_store.upsert_chunks(sample_chunks)
        initial_total = test_store.collection.count()
        self.assertEqual(count_first, len(sample_chunks))

        # Second upsert with identical chunks
        count_second = test_store.upsert_chunks(sample_chunks)
        subsequent_total = test_store.collection.count()

        self.assertEqual(initial_total, subsequent_total, "ChromaDB count doubled! Idempotency failed.")


if __name__ == "__main__":
    unittest.main()
