from app.modules.ai.schemas import RetrievedContext


def has_sufficient_context(context: RetrievedContext) -> bool:
    """Check if the retrieved context contains at least one usable document chunk.

    Args:
        context: The RetrievedContext object containing query and retrieved chunks.

    Returns:
        True if at least one chunk contains non-empty, non-whitespace text, False otherwise.
    """
    if not context or not context.chunks:
        return False

    return any(bool(chunk.text and chunk.text.strip()) for chunk in context.chunks)
