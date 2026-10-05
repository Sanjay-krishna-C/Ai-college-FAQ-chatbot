from app.core.logging import logger
from app.schemas.chat import ChatRequest, ChatResponse, ChatSourceItem


class ChatService:
    """
    Service responsible for orchestrating chat queries and document retrieval.
    Currently operating in Phase 5 foundation mode (pre-RAG).
    """

    async def generate_response(self, request: ChatRequest) -> ChatResponse:
        """
        Process incoming chat message.
        In this phase, validates request flow and returns structured foundation payload.
        Phase 6 will plug in ChromaDB retrieval and Phase 7 will plug in Gemini LLM synthesis.
        """
        logger.info(
            f"Received chat query: '{request.message[:80]}...' | "
            f"category: {request.category} | conversation_id: {request.conversation_id}"
        )

        # Temporary development response as required for Phase 5 foundation
        answer_text = (
            "CampusAI backend is connected successfully. "
            "AI retrieval will be enabled in the next phase."
        )

        return ChatResponse(
            answer=answer_text,
            sources=[],
            mode="development",
            session_id=request.conversation_id or "dev-session"
        )


chat_service = ChatService()
