import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class AIConfigError(ValueError):
    """Raised when required AI configuration environment variables are missing or invalid."""
    pass


def get_gemini_api_key() -> str:
    """Retrieve and validate the Gemini API key from environment variables.

    Raises:
        AIConfigError: If GEMINI_API_KEY is missing or empty.
    """
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise AIConfigError("GEMINI_API_KEY is missing or empty. Please set it in environment variables or .env file.")
    return key


def get_gemini_model() -> str:
    """Retrieve the Gemini model name from environment variables."""
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    if not model:
        raise AIConfigError("GEMINI_MODEL environment variable cannot be empty.")
    return model


def __getattr__(name: str) -> str:
    """Support dynamic module-level property access (e.g., config.GEMINI_API_KEY)."""
    if name == "GEMINI_API_KEY":
        return get_gemini_api_key()
    if name == "GEMINI_MODEL":
        return get_gemini_model()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
