import unittest
from pathlib import Path

from app.core.config import settings
from app.rag.embeddings import GeminiEmbeddingService
from app.rag.vector_store import ChromaVectorStore


class TestRetrievalQuality(unittest.TestCase):
    """
    Retrieval quality tests for the 5 key domain queries against the active collection:
    1. Attendance requirement
    2. Examination regulations
    3. Academic calendar
    4. Hostel information
    5. Relative grading
    """

    @classmethod
    def setUpClass(cls):
        cls.embedding_service = GeminiEmbeddingService()
        cls.store = ChromaVectorStore(collection_name=settings.CHROMA_COLLECTION_NAME)

    def _execute_search(self, query: str):
        if not self.embedding_service.is_configured():
            self.skipTest("GEMINI_API_KEY is not configured in backend/.env. Skipping live Gemini retrieval test.")

        query_emb = self.embedding_service.embed_query(query)
        results = self.store.search_similar(query_embedding=query_emb, top_k=3)
        return results

    def test_query_1_attendance_requirement(self):
        """Verify query 'attendance requirement' retrieves official regulations."""
        results = self._execute_search("What is the minimum attendance requirement to appear for exams?")
        self.assertGreater(len(results), 0, "No results returned for attendance query")

        combined_text = " ".join([r["text"].lower() for r in results])
        self.assertTrue(
            "attendance" in combined_text,
            f"Expected 'attendance' in retrieved text. Got: {combined_text[:200]}"
        )
        for r in results:
            self.assertIn("regulation", r["metadata"])
            self.assertIn("source_file", r["metadata"])

    def test_query_2_examination_regulations(self):
        """Verify query 'examination regulations' retrieves exam & evaluation clauses."""
        results = self._execute_search("Continuous assessment and semester end examination marks evaluation")
        self.assertGreater(len(results), 0)
        combined_text = " ".join([r["text"].lower() for r in results])
        self.assertTrue(
            "assessment" in combined_text or "examination" in combined_text or "marks" in combined_text
        )

    def test_query_3_academic_calendar(self):
        """Verify query 'academic calendar' retrieves schedule documents."""
        results = self._execute_search("Academic schedule reopening dates and semester calendar")
        self.assertGreater(len(results), 0)
        categories = [r["metadata"].get("document_category") for r in results]
        self.assertTrue("schedule" in categories or "academics" in categories)

    def test_query_4_hostel_information(self):
        """Verify query 'hostel facilities' retrieves AICTE disclosure."""
        results = self._execute_search("Hostel accommodation rooms mess and student amenities")
        self.assertGreater(len(results), 0)
        source_files = [r["metadata"].get("source_file") for r in results]
        self.assertIn("aicte-mandatory-disclosure.pdf", source_files)

    def test_query_5_relative_grading(self):
        """Verify query 'relative grading' retrieves 32nd ACM amendment."""
        results = self._execute_search("Relative grading criteria when student strength is greater than 30")
        self.assertGreater(len(results), 0)
        combined_text = " ".join([r["text"].lower() for r in results])
        self.assertTrue("relative grading" in combined_text or "grading" in combined_text)


if __name__ == "__main__":
    unittest.main()
