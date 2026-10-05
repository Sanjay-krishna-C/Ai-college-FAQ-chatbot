from app.modules.ai.schemas import (
    AIResponse,
    ResponseStatus,
    RetrievedContext,
    SourceReference,
)

DEFAULT_INSUFFICIENT_CONTEXT_MESSAGE = (
    "Sufficient information is not available in the college documents to answer this question."
)
DEFAULT_ERROR_MESSAGE = (
    "An error occurred while processing your request. Please try again later."
)


def build_grounded_response(answer: str, context: RetrievedContext) -> AIResponse:
    """Build a grounded AIResponse containing generated answer and extracted source references.

    Args:
        answer: Generated response string from Gemini.
        context: RetrievedContext containing retrieved chunks.

    Returns:
        AIResponse instance with grounded status and deduplicated source references.
    """
    sources: list[SourceReference] = []
    seen: set[tuple[str, int | None]] = set()

    if context and context.chunks:
        for chunk in context.chunks:
            key = (chunk.source, chunk.page)
            if key not in seen:
                seen.add(key)
                sources.append(SourceReference(source=chunk.source, page=chunk.page))

    return AIResponse(
        answer=answer,
        sources=sources,
        status=ResponseStatus.GROUNDED,
    )


def build_insufficient_context_response() -> AIResponse:
    """Build an AIResponse for cases where retrieved context is missing or insufficient.

    Returns:
        AIResponse with student-friendly message, empty sources, and insufficient_context status.
    """
    return AIResponse(
        answer=DEFAULT_INSUFFICIENT_CONTEXT_MESSAGE,
        sources=[],
        status=ResponseStatus.INSUFFICIENT_CONTEXT,
    )


def build_error_response() -> AIResponse:
    """Build a clean, user-friendly AIResponse for system or API failures.

    Returns:
        AIResponse with generic error message, empty sources, and error status.
    """
    return AIResponse(
        answer=DEFAULT_ERROR_MESSAGE,
        sources=[],
        status=ResponseStatus.ERROR,
    )
