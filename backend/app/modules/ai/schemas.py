from enum import Enum
from pydantic import BaseModel, Field


class ResponseStatus(str, Enum):
    GROUNDED = "grounded"
    INSUFFICIENT_CONTEXT = "insufficient_context"
    ERROR = "error"


class RetrievedChunk(BaseModel):
    text: str = Field(..., description="The content of the retrieved document chunk.")
    source: str = Field(..., description="Source document identifier or filename.")
    page: int | None = Field(default=None, description="Page number where chunk was found.")


class RetrievedContext(BaseModel):
    query: str = Field(..., description="The user query.")
    chunks: list[RetrievedChunk] = Field(default_factory=list, description="List of retrieved chunks.")


class SourceReference(BaseModel):
    source: str = Field(..., description="Source document identifier or filename.")
    page: int | None = Field(default=None, description="Page number of the reference.")


class AIResponse(BaseModel):
    answer: str = Field(..., description="The generated response answer.")
    sources: list[SourceReference] = Field(default_factory=list, description="List of source references used.")
    status: ResponseStatus = Field(..., description="Status of the AI response generation.")
