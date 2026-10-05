import os
from typing import List, Optional
from app.core.config import settings
from app.core.logging import logger


class GeminiEmbeddingError(Exception):
    """Raised when Gemini embedding generation fails or is misconfigured."""
    pass


class GeminiEmbeddingService:
    """
    Dedicated embedding generator using Google Gemini's embedding models.
    Supports configurable models (e.g., text-embedding-004) and batch processing.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
        self.model = model or settings.EMBEDDING_MODEL or "text-embedding-004"
        self._client = None
        self._init_client()

    def _init_client(self):
        """
        Initialize the official Google GenAI / Gemini client.
        Verifies API key presence and reports exact configuration issues.
        """
        if not self.api_key or len(self.api_key.strip()) < 10:
            logger.warning("GEMINI_API_KEY is not configured in the environment.")
            return

        try:
            # Modern Google GenAI SDK (v2.x)
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            logger.info(f"Initialized Gemini Embedding Service using model '{self.model}' via google.genai")
        except Exception as e:
            logger.warning(f"Could not initialize google.genai: {e}. Trying google.generativeai fallback...")
            try:
                import google.generativeai as legacy_genai
                legacy_genai.configure(api_key=self.api_key)
                self._client = legacy_genai
                logger.info(f"Initialized Gemini Embedding Service using model '{self.model}' via google.generativeai")
            except Exception as leg_err:
                raise GeminiEmbeddingError(
                    f"Failed to initialize Gemini SDK with provided configuration: {leg_err}"
                )

    def is_configured(self) -> bool:
        """Check whether the Gemini API key is configured."""
        return bool(self.api_key and len(self.api_key.strip()) >= 10 and self._client is not None)

    def embed_texts(self, texts: List[str], batch_size: int = 50) -> List[List[float]]:
        """
        Generate vector embeddings for a list of text strings in batches.
        """
        if not self.is_configured():
            raise GeminiEmbeddingError(
                "Gemini API key is not configured. Please set GEMINI_API_KEY in backend/.env "
                "or export it in your environment before generating embeddings."
            )

        all_embeddings: List[List[float]] = []

        # Process in batches to respect API limits
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                # Use modern google.genai client if initialized
                if hasattr(self._client, "models") and hasattr(self._client.models, "embed_content"):
                    # Format model identifier properly
                    model_id = self.model if "/" in self.model else f"models/{self.model}"
                    response = self._client.models.embed_content(
                        model=model_id,
                        contents=batch
                    )
                    # Extract embeddings
                    if hasattr(response, "embeddings"):
                        for emb in response.embeddings:
                            all_embeddings.append(list(emb.values))
                    else:
                        raise GeminiEmbeddingError(f"Unexpected response structure from embed_content: {response}")
                else:
                    # Legacy google.generativeai interface
                    model_id = self.model if self.model.startswith("models/") else f"models/{self.model}"
                    result = self._client.embed_content(
                        model=model_id,
                        content=batch
                    )
                    if "embedding" in result:
                        embeddings = result["embedding"]
                        if isinstance(embeddings[0], list):
                            all_embeddings.extend(embeddings)
                        else:
                            all_embeddings.append(embeddings)
                    else:
                        raise GeminiEmbeddingError(f"Unexpected response from legacy embed_content: {result.keys()}")

            except Exception as exc:
                logger.error(f"Gemini embedding batch generation failed (batch {i} to {i+len(batch)}): {exc}")
                raise GeminiEmbeddingError(
                    f"Gemini embedding API call failed: {exc}. Please verify GEMINI_API_KEY and model '{self.model}'."
                )

        return all_embeddings

    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a single user search query.
        """
        results = self.embed_texts([query], batch_size=1)
        if not results:
            raise GeminiEmbeddingError("Failed to generate embedding for query.")
        return results[0]
