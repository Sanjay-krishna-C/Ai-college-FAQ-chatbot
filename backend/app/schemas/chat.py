from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class ChatSourceItem(BaseModel):
    """
    Metadata for retrieved institutional documents supporting an answer.
    Preserves document name, page, regulation, and snippet citations.
    """
    document_name: str = Field(..., description="Name of the PDF document or title")
    source_file: Optional[str] = Field(None, description="Source PDF filename in dataset")
    title: Optional[str] = Field(None, description="Document or section title")
    page_number: Optional[int] = Field(None, description="Page number of citation")
    regulation: Optional[str] = Field(None, description="Regulation version (e.g. R2026, R2021)")
    clause_reference: Optional[str] = Field(None, description="Clause or regulation number (e.g. Clause 14.2)")
    snippet: Optional[str] = Field(None, description="Relevant excerpt from document")
    relevance_score: Optional[float] = Field(None, description="Similarity / relevance score")


class ChatRequest(BaseModel):
    """
    Incoming chat request from the student portal frontend.
    """
    message: str = Field(..., min_length=1, max_length=2000, description="User's query")
    conversation_id: Optional[str] = Field(None, description="Optional conversation session ID")
    category: Optional[str] = Field(None, description="Optional filter: academics, exams, hostel, fees, etc.")
    user_context: Optional[Dict[str, Any]] = Field(None, description="Optional contextual details (e.g. degree: UG/PG)")


class ChatResponse(BaseModel):
    """
    Structured AI response returned to the frontend.
    """
    answer: str = Field(..., description="Generated answer text")
    sources: List[ChatSourceItem] = Field(default_factory=list, description="Citations and referenced documents")
    mode: str = Field(default="rag_gemini", description="Execution mode: development, mock, or rag_gemini")
    confidence: Optional[float] = Field(None, description="Answer confidence score")
    session_id: Optional[str] = Field(None, description="Conversation session ID")
