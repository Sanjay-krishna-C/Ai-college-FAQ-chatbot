from app.modules.ai.pipeline import generate_response
from app.modules.ai.schemas import AIResponse, RetrievedContext


def answer_question(context: RetrievedContext) -> AIResponse:
    """Public service entry point for the AI module.

    Delegates the processing of retrieved context to the AI pipeline to produce a grounded response.

    Args:
        context: RetrievedContext containing the student query and retrieved document chunks.

    Returns:
        AIResponse instance containing generated answer, sources, and status.
    """
    return generate_response(context)
