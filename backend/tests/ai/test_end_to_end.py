from unittest.mock import MagicMock, patch
import pytest

from app.modules.ai.llm import LLMError
from app.modules.ai.pipeline import generate_response
from app.modules.ai.schemas import (
    AIResponse,
    ResponseStatus,
    RetrievedChunk,
    RetrievedContext,
)


@patch("app.modules.ai.pipeline.generate_answer")
def test_end_to_end_successful_flow(mock_generate_answer: MagicMock) -> None:
    """1. Test complete successful AI pipeline flow from retrieved context to grounded response."""
    expected_answer = (
        "According to the retrieved college information, students must follow the "
        "attendance requirements specified in the official regulations."
    )
    mock_generate_answer.return_value = expected_answer

    mock_context = RetrievedContext(
        query="What is the attendance requirement?",
        chunks=[
            RetrievedChunk(
                text="Students must satisfy the attendance requirements specified in the official college regulations.",
                source="academic_regulations.pdf",
                page=12,
            ),
            RetrievedChunk(
                text="Students are expected to follow the attendance policy described in the student handbook.",
                source="student_handbook.pdf",
                page=8,
            ),
        ],
    )

    response = generate_response(mock_context)

    # Verifications
    assert isinstance(response, AIResponse)
    mock_generate_answer.assert_called_once()

    # Verify query and retrieved chunk text were passed to LLM
    passed_query, passed_context_text = mock_generate_answer.call_args[0]
    assert passed_query == "What is the attendance requirement?"
    assert "Students must satisfy the attendance requirements" in passed_context_text
    assert "Students are expected to follow the attendance policy" in passed_context_text

    # Verify response structure, answer, status, and source metadata
    assert response.status == ResponseStatus.GROUNDED
    assert response.status == "grounded"
    assert response.answer == expected_answer
    assert len(response.sources) == 2

    assert response.sources[0].source == "academic_regulations.pdf"
    assert response.sources[0].page == 12
    assert response.sources[1].source == "student_handbook.pdf"
    assert response.sources[1].page == 8


@patch("app.modules.ai.pipeline.generate_answer")
def test_end_to_end_no_retrieved_context(mock_generate_answer: MagicMock) -> None:
    """2. Test pipeline behavior when RAG returns no chunks."""
    context = RetrievedContext(
        query="What is the attendance requirement?",
        chunks=[],
    )

    response = generate_response(context)

    assert isinstance(response, AIResponse)
    mock_generate_answer.assert_not_called()
    assert response.status == ResponseStatus.INSUFFICIENT_CONTEXT
    assert response.status == "insufficient_context"
    assert response.sources == []


@patch("app.modules.ai.pipeline.generate_answer")
def test_end_to_end_empty_retrieved_context(mock_generate_answer: MagicMock) -> None:
    """3. Test pipeline behavior when retrieved chunks contain only whitespace."""
    context = RetrievedContext(
        query="What is the attendance requirement?",
        chunks=[
            RetrievedChunk(
                text="   \n\t  ",
                source="academic_regulations.pdf",
                page=12,
            )
        ],
    )

    response = generate_response(context)

    assert isinstance(response, AIResponse)
    mock_generate_answer.assert_not_called()
    assert response.status == ResponseStatus.INSUFFICIENT_CONTEXT
    assert response.status == "insufficient_context"
    assert response.sources == []


@patch("app.modules.ai.pipeline.generate_answer")
def test_end_to_end_gemini_failure(mock_generate_answer: MagicMock) -> None:
    """4. Test pipeline behavior when Gemini LLM call raises an exception."""
    mock_generate_answer.side_effect = LLMError("Gemini API connection timeout")

    context = RetrievedContext(
        query="What is the attendance requirement?",
        chunks=[
            RetrievedChunk(
                text="Attendance rules details.",
                source="regulations.pdf",
                page=1,
            )
        ],
    )

    response = generate_response(context)

    assert isinstance(response, AIResponse)
    assert response.status == ResponseStatus.ERROR
    assert response.status == "error"
    assert response.sources == []
    # Verify no stack trace, API key, or raw exception detail is exposed
    assert "Gemini API connection timeout" not in response.answer
    assert "Traceback" not in response.answer
    assert "Exception" not in response.answer


@patch("app.modules.ai.pipeline.generate_answer")
def test_end_to_end_multiple_sources_and_deduplication(mock_generate_answer: MagicMock) -> None:
    """5. Test pipeline handling of multiple sources and deduplication of identical source/page pairs."""
    mock_generate_answer.return_value = "Attendance requirement is 75 percent minimum."

    context = RetrievedContext(
        query="Attendance minimum percentage?",
        chunks=[
            RetrievedChunk(text="Minimum 75% attendance.", source="rules.pdf", page=5),
            RetrievedChunk(text="75% required for exams.", source="rules.pdf", page=5),  # Duplicate source/page
            RetrievedChunk(text="Medical condonation available.", source="policy.pdf", page=2),
        ],
    )

    response = generate_response(context)

    # Verify all chunk contents reach LLM context
    _, passed_context_text = mock_generate_answer.call_args[0]
    assert "Minimum 75% attendance." in passed_context_text
    assert "75% required for exams." in passed_context_text
    assert "Medical condonation available." in passed_context_text

    # Verify duplicate source/page is deduplicated cleanly in final response
    assert response.status == ResponseStatus.GROUNDED
    assert len(response.sources) == 2
    assert response.sources[0].source == "rules.pdf"
    assert response.sources[0].page == 5
    assert response.sources[1].source == "policy.pdf"
    assert response.sources[1].page == 2
