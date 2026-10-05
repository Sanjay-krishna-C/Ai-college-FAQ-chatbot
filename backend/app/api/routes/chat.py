from fastapi import APIRouter, HTTPException, status
from app.core.logging import logger
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_endpoint(request: ChatRequest):
    """
    Primary chat interaction endpoint for CampusAI.
    Accepts user message and returns structured assistant response with sources.
    """
    try:
        response = await chat_service.generate_response(request)
        return response
    except Exception as exc:
        logger.error(f"Error processing chat request: {exc}", exc_info=True)
        # Never expose internal exceptions or stack traces to client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request. Please try again later."
        )
