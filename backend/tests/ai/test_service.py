from unittest.mock import MagicMock, patch
import pytest

from app.modules.ai.schemas import (
    AIResponse,
    ResponseStatus,
    RetrievedChunk,
    RetrievedContext,
    SourceReference,
)
from app.modules.ai.service import answer_question


@patch("app.modules.ai.service.generate_response")
def test_answer_question_passes_context_to_pipeline(mock_generate_response: MagicMock) -> None:
    """1 & 6. Test that answer_question passes RetrievedContext to generate_response exactly once."""
    expected_response = AIResponse(
        answer="Expected answer",
        sources=[SourceReference(source="doc.pdf", page=1)],
        status=ResponseStatus.GROUNDED,
    )
    mock_generate_response.return_value = expected_response

    chunk = RetrievedChunk(text="Sample text", source="doc.pdf", page=1)
    context = RetrievedContext(query="Sample question?", chunks=[chunk])

    result = answer_question(context)

    mock_generate_response.assert_called_once_with(context)
    assert result is expected_response


@patch("app.modules.ai.service.generate_response")
def test_answer_question_returns_grounded_response_unchanged(
    mock_generate_response: MagicMock,
) -> None:
    """2 & 3. Test that a grounded AIResponse from the pipeline is returned unchanged."""
    expected_response = AIResponse(
        answer="The library closes at 10 PM.",
        sources=[SourceReference(source="campus_guide.pdf", page=10)],
        status=ResponseStatus.GROUNDED,
    )
    mock_generate_response.return_value = expected_response

    context = RetrievedContext(query="Library closing time?", chunks=[])

    result = answer_question(context)

    assert result == expected_response
    assert result.status == ResponseStatus.GROUNDED
    assert result.status == "grounded"
    assert result.answer == "The library closes at 10 PM."
    assert len(result.sources) == 1


@patch("app.modules.ai.service.generate_response")
def test_answer_question_returns_insufficient_context_response(
    mock_generate_response: MagicMock,
) -> None:
    """4. Test that an insufficient_context AIResponse from the pipeline is correctly returned."""
    expected_response = AIResponse(
        answer="Sufficient information is not available.",
        sources=[],
        status=ResponseStatus.INSUFFICIENT_CONTEXT,
    )
    mock_generate_response.return_value = expected_response

    context = RetrievedContext(query="Unknown topic?", chunks=[])

    result = answer_question(context)

    assert result == expected_response
    assert result.status == ResponseStatus.INSUFFICIENT_CONTEXT
    assert result.status == "insufficient_context"
    assert result.sources == []


@patch("app.modules.ai.service.generate_response")
def test_answer_question_returns_error_response(mock_generate_response: MagicMock) -> None:
    """5. Test that an error AIResponse from the pipeline is correctly returned."""
    expected_response = AIResponse(
        answer="An error occurred while processing your request.",
        sources=[],
        status=ResponseStatus.ERROR,
    )
    mock_generate_response.return_value = expected_response

    context = RetrievedContext(query="Any query?", chunks=[])

    result = answer_question(context)

    assert result == expected_response
    assert result.status == ResponseStatus.ERROR
    assert result.status == "error"
    assert result.sources == []
