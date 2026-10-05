from unittest.mock import MagicMock, patch
import pytest

from app.modules.ai.llm import LLMError
from app.modules.ai.pipeline import generate_response
from app.modules.ai.schemas import ResponseStatus, RetrievedChunk, RetrievedContext


@patch("app.modules.ai.pipeline.generate_answer")
def test_pipeline_valid_context(mock_generate_answer: MagicMock) -> None:
    """1. Test valid context pipeline execution -> grounded AIResponse."""
    mock_generate_answer.return_value = "The application deadline is June 30."

    chunk = RetrievedChunk(text="Application deadline is June 30.", source="admissions.pdf", page=4)
    context = RetrievedContext(query="When is application deadline?", chunks=[chunk])

    response = generate_response(context)

    assert response.status == ResponseStatus.GROUNDED
    assert response.status == "grounded"
    assert response.answer == "The application deadline is June 30."
    assert len(response.sources) == 1
    assert response.sources[0].source == "admissions.pdf"
    assert response.sources[0].page == 4


@patch("app.modules.ai.pipeline.generate_answer")
def test_pipeline_no_retrieved_chunks(mock_generate_answer: MagicMock) -> None:
    """2. Test pipeline with empty chunks list -> insufficient_context response, LLM not called."""
    context = RetrievedContext(query="Hostel curfew?", chunks=[])

    response = generate_response(context)

    mock_generate_answer.assert_not_called()
    assert response.status == ResponseStatus.INSUFFICIENT_CONTEXT
    assert response.sources == []


@patch("app.modules.ai.pipeline.generate_answer")
def test_pipeline_empty_whitespace_chunk(mock_generate_answer: MagicMock) -> None:
    """3. Test pipeline with whitespace-only chunk -> insufficient_context response, LLM not called."""
    chunk = RetrievedChunk(text="   \n\t  ", source="doc.pdf", page=1)
    context = RetrievedContext(query="Fee structure?", chunks=[chunk])

    response = generate_response(context)

    mock_generate_answer.assert_not_called()
    assert response.status == ResponseStatus.INSUFFICIENT_CONTEXT
    assert response.sources == []


@patch("app.modules.ai.pipeline.generate_answer")
def test_pipeline_gemini_failure(mock_generate_answer: MagicMock) -> None:
    """4. Test pipeline behavior when Gemini LLM raises an exception -> error response."""
    mock_generate_answer.side_effect = LLMError("Gemini API connection error")

    chunk = RetrievedChunk(text="Some retrieved text.", source="guide.pdf", page=2)
    context = RetrievedContext(query="Any question?", chunks=[chunk])

    response = generate_response(context)

    assert response.status == ResponseStatus.ERROR
    assert response.sources == []
    assert "Gemini API connection error" not in response.answer
    assert "Traceback" not in response.answer


@patch("app.modules.ai.pipeline.generate_answer")
def test_pipeline_multiple_chunks_formatting(mock_generate_answer: MagicMock) -> None:
    """5. Test that text from multiple chunks reaches LLM and source metadata is preserved."""
    mock_generate_answer.return_value = "Combined information answer."

    c1 = RetrievedChunk(text="Attendance must be 75%.", source="rules.pdf", page=10)
    c2 = RetrievedChunk(text="Medical leave requires doctor certificate.", source="handbook.pdf", page=15)
    context = RetrievedContext(query="Attendance rules?", chunks=[c1, c2])

    response = generate_response(context)

    mock_generate_answer.assert_called_once()
    _, kwargs_or_args = mock_generate_answer.call_args
    passed_context_arg = mock_generate_answer.call_args[0][1]

    assert "Attendance must be 75%." in passed_context_arg
    assert "Medical leave requires doctor certificate." in passed_context_arg
    assert "Source: rules.pdf" in passed_context_arg
    assert "Source: handbook.pdf" in passed_context_arg

    assert response.status == ResponseStatus.GROUNDED
    assert len(response.sources) == 2
    assert response.sources[0].source == "rules.pdf"
    assert response.sources[1].source == "handbook.pdf"


@patch("app.modules.ai.pipeline.generate_answer")
def test_pipeline_correct_question_propagation(mock_generate_answer: MagicMock) -> None:
    """6. Test that context.query is correctly passed as the question argument to generate_answer."""
    mock_generate_answer.return_value = "Answer text"

    chunk = RetrievedChunk(text="Fact text", source="fact.pdf", page=1)
    query_text = "What is the official college entrance code?"
    context = RetrievedContext(query=query_text, chunks=[chunk])

    generate_response(context)

    mock_generate_answer.assert_called_once()
    passed_question = mock_generate_answer.call_args[0][0]
    assert passed_question == query_text
