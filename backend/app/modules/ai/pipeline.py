from app.modules.ai.grounding import has_sufficient_context
from app.modules.ai.llm import generate_answer
from app.modules.ai.response import (
    build_error_response,
    build_grounded_response,
    build_insufficient_context_response,
)
from app.modules.ai.schemas import AIResponse, RetrievedContext


def _format_context(context: RetrievedContext) -> str:
    """Format retrieved document chunks into a single text block for the LLM.

    Args:
        context: RetrievedContext object containing document chunks.

    Returns:
        Formatted context string including source, page, and chunk text.
    """
    formatted_chunks = []
    for chunk in context.chunks:
        if not chunk.text or not chunk.text.strip():
            continue

        page_str = f"\nPage: {chunk.page}" if chunk.page is not None else ""
        chunk_entry = f"Source: {chunk.source}{page_str}\nContent:\n{chunk.text.strip()}"
        formatted_chunks.append(chunk_entry)

    return "\n\n".join(formatted_chunks)


def generate_response(context: RetrievedContext) -> AIResponse:
    """Orchestrate the AI RAG pipeline to produce a grounded response.

    Pipeline steps:
    1. Validate context sufficiency using grounding check.
    2. Format retrieved chunks if context is sufficient.
    3. Generate grounded answer via Gemini LLM.
    4. Construct and return AIResponse with source metadata.

    Args:
        context: RetrievedContext object containing query and retrieved chunks.

    Returns:
        AIResponse object (grounded, insufficient_context, or error).
    """
    if not has_sufficient_context(context):
        return build_insufficient_context_response()

    try:
        formatted_context_str = _format_context(context)
        answer = generate_answer(context.query, formatted_context_str)
        return build_grounded_response(answer, context)
    except Exception:
        return build_error_response()
