from unittest.mock import MagicMock, patch
import pytest

from app.modules.ai.llm import LLMError, generate_answer


@patch("app.modules.ai.llm.get_client")
@patch("app.modules.ai.llm.get_gemini_model")
def test_successful_gemini_response(mock_get_model: MagicMock, mock_get_client: MagicMock) -> None:
    """1. Test that a successful Gemini response returns the expected stripped text."""
    mock_get_model.return_value = "gemini-2.5-flash"

    mock_response = MagicMock()
    mock_response.text = "  The application deadline is June 30.  "

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client

    result = generate_answer("What is the application deadline?", "Deadline: June 30")
    assert result == "The application deadline is June 30."


@patch("app.modules.ai.llm.build_user_prompt")
@patch("app.modules.ai.llm.get_client")
def test_question_and_context_passed_to_prompt_builder(
    mock_get_client: MagicMock, mock_build_prompt: MagicMock
) -> None:
    """2 & 3. Test that the question and retrieved context are passed into prompt construction."""
    mock_build_prompt.return_value = "Formatted Prompt"
    mock_response = MagicMock()
    mock_response.text = "Sample answer"
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client

    question = "How much is tuition?"
    context = "Tuition is $5,000 per term."

    generate_answer(question, context)
    mock_build_prompt.assert_called_once_with(question, context)


@patch("app.modules.ai.llm.get_gemini_model")
@patch("app.modules.ai.llm.get_client")
def test_gemini_model_configured_in_config_is_used(
    mock_get_client: MagicMock, mock_get_model: MagicMock
) -> None:
    """4. Test that the Gemini model configured in config.py is passed to generate_content."""
    mock_get_model.return_value = "custom-gemini-model"
    mock_response = MagicMock()
    mock_response.text = "Sample answer"
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client

    generate_answer("Question?", "Context")

    _, kwargs = mock_client.models.generate_content.call_args
    assert kwargs.get("model") == "custom-gemini-model"


@patch("app.modules.ai.llm.SYSTEM_PROMPT", "Test System Instruction")
@patch("app.modules.ai.llm.get_client")
def test_system_instruction_passed_to_gemini(mock_get_client: MagicMock) -> None:
    """5. Test that the system instruction is passed to the Gemini request config."""
    mock_response = MagicMock()
    mock_response.text = "Sample answer"
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client

    generate_answer("Question?", "Context")

    _, kwargs = mock_client.models.generate_content.call_args
    config = kwargs.get("config")
    assert config is not None
    assert config.system_instruction == "Test System Instruction"


@patch("app.modules.ai.llm.get_client")
def test_empty_response_raises_llm_error(mock_get_client: MagicMock) -> None:
    """6. Test that an empty response raises a clear LLMError exception."""
    mock_response = MagicMock()
    mock_response.text = "   "
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client

    with pytest.raises(LLMError, match="empty or invalid response"):
        generate_answer("Question?", "Context")


@patch("app.modules.ai.llm.get_client")
def test_gemini_api_error_handled_cleanly(mock_get_client: MagicMock) -> None:
    """7. Test that Gemini/API failures are handled cleanly as an LLMError."""
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = RuntimeError("API connection timeout")
    mock_get_client.return_value = mock_client

    with pytest.raises(LLMError, match="Gemini API call failed"):
        generate_answer("Question?", "Context")
