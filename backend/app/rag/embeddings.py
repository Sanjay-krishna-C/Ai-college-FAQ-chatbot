import os
import time
from typing import List, Optional, Dict, Any
from app.core.config import settings
from app.core.logging import logger


class GeminiEmbeddingError(Exception):
    """Raised when Gemini embedding generation fails or is misconfigured."""
    pass


class GeminiEmbeddingService:
    """
    Dedicated embedding generator using Google Gemini's current embedding model: gemini-embedding-2.
    Explicitly requests and validates 768-dimensional output for the ChromaDB RAG index.
    Strictly forbids fallback to local or default Chroma models.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
        self.model = model or settings.EMBEDDING_MODEL or "gemini-embedding-2"
        self.target_dimension: int = settings.EXPECTED_EMBEDDING_DIM or 768
        self.detected_dimension: Optional[int] = None
        self._client = None
        self._init_client()

    def _init_client(self):
        """
        Initialize Google GenAI client.
        Verifies API key presence and reports exact configuration issues.
        """
        if not self.api_key or len(self.api_key.strip()) < 10:
            logger.warning("GEMINI_API_KEY is not configured in backend/.env or environment.")
            return

        try:
            from google import genai
            self._client = genai.Client(api_key=self.api_key)
            logger.info(f"Initialized Gemini Embedding Service using model '{self.model}' via google.genai")
        except Exception as e:
            logger.warning(f"Could not initialize google.genai: {e}. Trying google.generativeai fallback...")
            try:
                import google.generativeai as legacy_genai
                legacy_genai.configure(api_key=self.api_key)
                self._client = legacy_genai
                logger.info(f"Initialized Gemini Embedding Service using model '{self.model}' via legacy google.generativeai")
            except Exception as leg_err:
                raise GeminiEmbeddingError(
                    f"Failed to initialize Gemini SDK with provided configuration: {leg_err}"
                )

    def is_configured(self) -> bool:
        """Check whether the Gemini API key is configured and client initialized."""
        return bool(self.api_key and len(self.api_key.strip()) >= 10 and self._client is not None)

    def detect_dimension(self) -> int:
        """
        Actively probe the Gemini API to detect and validate the embedding vector dimensionality.
        Verifies that gemini-embedding-2 returns exactly 768 dimensions.
        Raises GeminiEmbeddingError if the key is missing, invalid, or returned dimension is not 768.
        """
        if not self.is_configured():
            raise GeminiEmbeddingError(
                "GEMINI_API_KEY is not configured or missing in backend/.env. "
                "Please configure a valid Google Gemini API key to proceed with Phase 6B Gemini embeddings."
            )

        if self.detected_dimension is not None:
            return self.detected_dimension

        try:
            probe_results = self.embed_texts(["CampusAI probe for dimension validation"], batch_size=1)
            if not probe_results or not probe_results[0]:
                raise GeminiEmbeddingError("Received empty embedding vector from Gemini API probe.")

            actual_dim = len(probe_results[0])
            if actual_dim != self.target_dimension:
                raise GeminiEmbeddingError(
                    f"Gemini embedding dimension mismatch! Expected {self.target_dimension}, but received {actual_dim} from '{self.model}'."
                )

            self.detected_dimension = actual_dim
            logger.info(f"Verified Gemini embedding dimensionality: exactly {self.detected_dimension} dimensions")
            return self.detected_dimension

        except Exception as exc:
            raise GeminiEmbeddingError(
                f"Failed to validate Gemini embedding dimension for model '{self.model}': {exc}"
            )

    def embed_texts(self, texts: List[str], batch_size: int = 50) -> List[List[float]]:
        """
        Generate vector embeddings for a list of text strings in batches using Google Gemini.
        Explicitly requests 768-dimensional output from gemini-embedding-2.
        NEVER falls back to local or Chroma default embedding functions.
        """
        if not self.is_configured():
            raise GeminiEmbeddingError(
                "GEMINI_API_KEY is not configured. Please set GEMINI_API_KEY in backend/.env "
                "or export it in your environment before generating Gemini embeddings."
            )

        if not texts:
            return []

        all_embeddings: List[List[float]] = []

        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            max_retries = 3
            success = False

            for attempt in range(max_retries):
                try:
                    # Modern google.genai client
                    if hasattr(self._client, "models") and hasattr(self._client.models, "embed_content"):
                        from google.genai import types
                        model_id = self.model.replace("models/", "")
                        config = types.EmbedContentConfig(output_dimensionality=self.target_dimension)

                        # Wrap each individual text as a separate Content object to get 1 embedding per text
                        contents = [
                            types.Content(parts=[types.Part.from_text(text=t)])
                            for t in batch
                        ]

                        response = self._client.models.embed_content(
                            model=model_id,
                            contents=contents,
                            config=config
                        )

                        if hasattr(response, "embeddings") and response.embeddings:
                            for emb in response.embeddings:
                                vec = list(emb.values)
                                if len(vec) != self.target_dimension:
                                    raise GeminiEmbeddingError(
                                        f"Received vector with dimension {len(vec)}, expected {self.target_dimension}"
                                    )
                                all_embeddings.append(vec)
                                if self.detected_dimension is None:
                                    self.detected_dimension = len(vec)
                            success = True
                            break
                        else:
                            raise GeminiEmbeddingError(f"Unexpected response structure from embed_content: {response}")

                    else:
                        # Legacy google.generativeai interface
                        model_id = self.model if self.model.startswith("models/") else f"models/{self.model}"
                        result = self._client.embed_content(
                            model=model_id,
                            content=batch,
                            output_dimensionality=self.target_dimension
                        )
                        if "embedding" in result:
                            embeddings = result["embedding"]
                            if isinstance(embeddings[0], list):
                                for vec in embeddings:
                                    all_embeddings.append(vec)
                                    if self.detected_dimension is None:
                                        self.detected_dimension = len(vec)
                            else:
                                all_embeddings.append(embeddings)
                                if self.detected_dimension is None:
                                    self.detected_dimension = len(embeddings)
                            success = True
                            break
                        else:
                            raise GeminiEmbeddingError(f"Unexpected response from legacy embed_content: {result.keys()}")

                except Exception as exc:
                    err_str = str(exc)
                    is_rate_limit = "RESOURCE_EXHAUSTED" in err_str or "429" in err_str
                    if is_rate_limit:
                        # Extract retry delay or default to 52s
                        delay = 52
                        import re
                        m = re.search(r"retry in (\d+(?:\.\d+)?)s", err_str)
                        if m:
                            delay = int(float(m.group(1))) + 2
                        elif "retryDelay" in err_str:
                            m2 = re.search(r"retryDelay': '(\d+)s", err_str)
                            if m2:
                                delay = int(m2.group(1)) + 2

                        logger.warning(f"Gemini Free-Tier rate limit reached. Pausing {delay}s before retry (attempt {attempt+1}/{max_retries})...")
                        print(f"   [QUOTA-WAIT] Rate limit reached. Waiting {delay}s for quota window to reset...")
                        time.sleep(delay)
                    elif attempt < max_retries - 1:
                        logger.warning(f"Batch embedding retry {attempt+1}/{max_retries} due to: {exc}")
                        time.sleep(3 * (attempt + 1))
                    else:
                        logger.error(f"Gemini embedding batch generation failed (batch {i} to {i+len(batch)}): {exc}")
                        raise GeminiEmbeddingError(
                            f"Gemini embedding API call failed: {exc}. Please verify GEMINI_API_KEY and model '{self.model}'."
                        )

        return all_embeddings

    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding vector for a user search query using Gemini (768 dimensions).
        """
        if not self.is_configured():
            raise GeminiEmbeddingError(
                "Cannot embed query: GEMINI_API_KEY is not configured in backend/.env."
            )
        results = self.embed_texts([query], batch_size=1)
        if not results:
            raise GeminiEmbeddingError("Failed to generate Gemini embedding for query.")
        return results[0]

    def get_info(self) -> Dict[str, Any]:
        """
        Return embedding provider metadata.
        """
        return {
            "provider": "Google Gemini",
            "model": self.model,
            "is_configured": self.is_configured(),
            "detected_dimension": self.detected_dimension or self.target_dimension
        }
