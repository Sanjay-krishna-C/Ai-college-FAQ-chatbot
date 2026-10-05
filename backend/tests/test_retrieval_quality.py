import unittest
from pathlib import Path

from app.core.config import settings
from app.rag.metadata import DATASET_REGISTRY
from app.rag.extractor import PDFExtractor
from app.rag.chunking import IntelligentChunker
from app.rag.vector_store import ChromaVectorStore


class TestRetrievalQuality(unittest.TestCase):
    """
    Retrieval quality tests for the 5 key domain queries:
    1. Attendance requirement
    2. Examination regulations
    3. Academic calendar
    4. Hostel information
    5. Relative grading
    """

    @classmethod
    def setUpClass(cls):
        dataset_dir = Path(settings.DATASET_DIRECTORY)
        extractor = PDFExtractor()
        chunker = IntelligentChunker()
        cls.store = ChromaVectorStore()

        # If collection is empty, ingest the 13 verified documents
        if cls.store.collection.count() == 0:
            print("[INFO] Populating institutional knowledge collection for retrieval testing...")
            all_chunks = []
            for pdf_file in sorted(dataset_dir.iterdir()):
                if not pdf_file.name.endswith(".pdf"):
                    continue
                spec = DATASET_REGISTRY.get(pdf_file.name)
                if not spec or not spec.is_included_in_primary_rag:
                    continue
                pages = extractor.extract_document(pdf_file)
                for page in pages:
                    if not page.is_empty:
                        all_chunks.extend(chunker.chunk_page(page))

            cls.store.upsert_chunks(all_chunks)
            print(f"[INFO] Populated {len(all_chunks)} chunks into ChromaDB.")

    def test_query_1_attendance_requirement(self):
        """Verify query 'attendance requirement' retrieves official regulations."""
        results = self.store.search_similar(query_text="What is the minimum attendance requirement to appear for exams?", top_k=3)
        self.assertGreater(len(results), 0, "No results returned for attendance query")

        combined_text = " ".join([r["text"].lower() for r in results])
        self.assertTrue(
            "attendance" in combined_text,
            f"Expected 'attendance' in retrieved text. Got: {combined_text[:200]}"
        )
        # Verify metadata preserves regulation
        for r in results:
            self.assertIn("regulation", r["metadata"])
            self.assertIn("source_file", r["metadata"])

    def test_query_2_examination_regulations(self):
        """Verify query 'examination regulations' retrieves exam & evaluation clauses."""
        results = self.store.search_similar(query_text="Continuous assessment and semester end examination marks evaluation", top_k=3)
        self.assertGreater(len(results), 0)
        combined_text = " ".join([r["text"].lower() for r in results])
        self.assertTrue(
            "assessment" in combined_text or "examination" in combined_text or "marks" in combined_text
        )

    def test_query_3_academic_calendar(self):
        """Verify query 'academic calendar' retrieves schedule documents."""
        results = self.store.search_similar(query_text="Academic schedule reopening dates and semester calendar", top_k=3)
        self.assertGreater(len(results), 0)
        categories = [r["metadata"].get("document_category") for r in results]
        self.assertTrue("schedule" in categories or "academics" in categories)

    def test_query_4_hostel_information(self):
        """Verify query 'hostel facilities' retrieves AICTE disclosure."""
        results = self.store.search_similar(query_text="Hostel accommodation rooms mess and student amenities", top_k=3)
        self.assertGreater(len(results), 0)
        source_files = [r["metadata"].get("source_file") for r in results]
        self.assertIn("aicte-mandatory-disclosure.pdf", source_files)

    def test_query_5_relative_grading(self):
        """Verify query 'relative grading' retrieves 32nd ACM amendment."""
        results = self.store.search_similar(query_text="Relative grading criteria when student strength is greater than 30", top_k=3)
        self.assertGreater(len(results), 0)
        combined_text = " ".join([r["text"].lower() for r in results])
        self.assertTrue("relative grading" in combined_text or "grading" in combined_text)


if __name__ == "__main__":
    unittest.main()
