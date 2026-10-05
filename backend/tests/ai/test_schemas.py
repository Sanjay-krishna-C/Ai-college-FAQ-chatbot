import unittest
from pydantic import ValidationError
from app.modules.ai.schemas import (
    AIResponse,
    ResponseStatus,
    RetrievedChunk,
    RetrievedContext,
    SourceReference,
)


class TestAISchemas(unittest.TestCase):
    def test_valid_retrieved_chunk(self):
        """1. Test creating a valid RetrievedChunk."""
        chunk = RetrievedChunk(
            text="Admissions deadline is May 1st.",
            source="handbook.pdf",
            page=12,
        )
        self.assertEqual(chunk.text, "Admissions deadline is May 1st.")
        self.assertEqual(chunk.source, "handbook.pdf")
        self.assertEqual(chunk.page, 12)

    def test_valid_retrieved_context(self):
        """2. Test creating a valid RetrievedContext."""
        chunk1 = RetrievedChunk(text="Tuition fee is $5,000.", source="fees.pdf", page=3)
        chunk2 = RetrievedChunk(text="Scholarships available.", source="fees.pdf", page=4)
        context = RetrievedContext(
            query="What is the tuition fee?",
            chunks=[chunk1, chunk2],
        )
        self.assertEqual(context.query, "What is the tuition fee?")
        self.assertEqual(len(context.chunks), 2)
        self.assertEqual(context.chunks[0].text, "Tuition fee is $5,000.")

    def test_valid_source_reference(self):
        """3. Test creating a valid SourceReference."""
        ref = SourceReference(source="handbook.pdf", page=12)
        self.assertEqual(ref.source, "handbook.pdf")
        self.assertEqual(ref.page, 12)

    def test_valid_ai_response(self):
        """4. Test creating a valid AIResponse."""
        source = SourceReference(source="handbook.pdf", page=12)
        response = AIResponse(
            answer="The admissions deadline is May 1st.",
            sources=[source],
            status=ResponseStatus.GROUNDED,
        )
        self.assertEqual(response.answer, "The admissions deadline is May 1st.")
        self.assertEqual(response.status, ResponseStatus.GROUNDED)
        self.assertEqual(response.status, "grounded")
        self.assertEqual(len(response.sources), 1)

    def test_preservation_of_source_and_page_info(self):
        """5. Test preservation of source and page information (including optional/None page)."""
        chunk = RetrievedChunk(text="Library hours are 8am-10pm.", source="campus_guide.pdf", page=None)
        self.assertEqual(chunk.source, "campus_guide.pdf")
        self.assertIsNone(chunk.page)

        ref = SourceReference(source="campus_guide.pdf", page=15)
        self.assertEqual(ref.source, "campus_guide.pdf")
        self.assertEqual(ref.page, 15)

    def test_rejection_of_invalid_required_fields(self):
        """6. Test rejection of missing or invalid required fields."""
        # Missing required 'text' in RetrievedChunk
        with self.assertRaises(ValidationError):
            RetrievedChunk(source="doc.pdf")  # type: ignore

        # Missing required 'query' in RetrievedContext
        with self.assertRaises(ValidationError):
            RetrievedContext(chunks=[])  # type: ignore

        # Missing required 'answer' in AIResponse
        with self.assertRaises(ValidationError):
            AIResponse(sources=[], status=ResponseStatus.GROUNDED)  # type: ignore

    def test_validation_of_allowed_response_statuses(self):
        """7. Test validation of allowed response statuses (grounded, insufficient_context, error)."""
        for valid_status in [ResponseStatus.GROUNDED, ResponseStatus.INSUFFICIENT_CONTEXT, ResponseStatus.ERROR]:
            response = AIResponse(answer="Sample answer", sources=[], status=valid_status)
            self.assertIn(response.status, ["grounded", "insufficient_context", "error"])

        # String representations should also validate if matching allowed enum values
        res_str = AIResponse(answer="Sample answer", sources=[], status="insufficient_context")  # type: ignore
        self.assertEqual(res_str.status, ResponseStatus.INSUFFICIENT_CONTEXT)

        # Invalid status string should raise ValidationError
        with self.assertRaises(ValidationError):
            AIResponse(answer="Sample answer", sources=[], status="invalid_status")  # type: ignore


if __name__ == "__main__":
    unittest.main()
