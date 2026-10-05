from __future__ import annotations

from typing import Any

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None  # type: ignore

    class _TypesStub:
        class GenerateContentConfig:
            def __init__(
                self,
                system_instruction: str | None = None,
                temperature: float | None = None,
                max_output_tokens: int | None = None,
            ):
                self.system_instruction = system_instruction
                self.temperature = temperature
                self.max_output_tokens = max_output_tokens

    types = _TypesStub()  # type: ignore

from app.modules.ai.config import get_gemini_api_key, get_gemini_model
from app.modules.ai.prompts import SYSTEM_PROMPT, build_user_prompt


class LLMError(Exception):
    """Raised when an error occurs during Gemini LLM response generation."""
    pass


def get_client() -> Any:
    """Initialize and return a google-genai Client instance using the configured API key.

    Returns:
        genai.Client instance.

    Raises:
        LLMError: If google-genai SDK is not installed or API key is missing.
    """
    if genai is None:
        raise LLMError("google-genai SDK is not installed. Please install requirements/ai.txt.")
    api_key = get_gemini_api_key()
    return genai.Client(api_key=api_key)


def generate_answer(question: str, context: str) -> str:
    """Generate a grounded answer for a student's question using Gemini and retrieved context.

    Args:
        question: Student's question.
        context: Retrieved college context information.

    Returns:
        Stripped string containing the generated response answer.

    Raises:
        LLMError: If the Gemini API call fails or returns an empty response.
    """
    user_prompt = build_user_prompt(question, context)
    model_name = get_gemini_model()
    client = get_client()

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
                max_output_tokens=1024,
            ),
        )
    except Exception as e:
        raise LLMError(f"Gemini API call failed: {e}") from e

    if not response or not hasattr(response, "text") or not response.text or not response.text.strip():
        raise LLMError("Received empty or invalid response from Gemini API.")

    return response.text.strip()
