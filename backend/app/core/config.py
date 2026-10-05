import json
import os
from pathlib import Path
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Determine base paths
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
DEFAULT_DATASET_DIR = PROJECT_ROOT / "dataset"
DEFAULT_CHROMA_DIR = BACKEND_DIR / "data" / "chroma"


class Settings(BaseSettings):
    """
    CampusAI Application Settings.
    Loaded from environment variables and .env file.
    """
    APP_NAME: str = "CampusAI Backend"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS origins allowed to access the backend API
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Secret keys (loaded securely from env)
    GEMINI_API_KEY: str = ""

    # Gemini Embedding Configuration
    EMBEDDING_MODEL: str = "text-embedding-004"

    # Dataset & ChromaDB Storage
    DATASET_DIRECTORY: str = str(DEFAULT_DATASET_DIR)
    CHROMA_PERSIST_DIRECTORY: str = str(DEFAULT_CHROMA_DIR)
    CHROMA_COLLECTION_NAME: str = "campusai_institutional_knowledge"

    # Chunking Parameters
    CHUNK_SIZE: int = 700
    CHUNK_OVERLAP: int = 100

    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, str) and v.startswith("["):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass
        return v if isinstance(v, list) else ["http://localhost:3000", "http://127.0.0.1:3000"]


settings = Settings()
