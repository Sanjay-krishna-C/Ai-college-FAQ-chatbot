import pytest
from app.modules.ai.config import (
    AIConfigError,
    get_gemini_api_key,
    get_gemini_model,
)


def test_valid_api_key_loaded(monkeypatch: pytest.MonkeyPatch) -> None:
    """1. Test that a valid API key can be loaded from the environment."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-secret-key-12345")
    assert get_gemini_api_key() == "test-secret-key-12345"


def test_model_name_loaded_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """2. Test that the model name can be loaded from the environment."""
    monkeypatch.setenv("GEMINI_MODEL", "gemini-1.5-pro")
    assert get_gemini_model() == "gemini-1.5-pro"


def test_missing_api_key_raises_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """3. Test that a missing API key raises a clear AIConfigError."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(AIConfigError, match="GEMINI_API_KEY is missing or empty"):
        get_gemini_api_key()


def test_empty_api_key_treated_as_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """4. Test that an empty or whitespace-only API key is treated as missing."""
    monkeypatch.setenv("GEMINI_API_KEY", "   ")
    with pytest.raises(AIConfigError, match="GEMINI_API_KEY is missing or empty"):
        get_gemini_api_key()
