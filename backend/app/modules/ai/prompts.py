SYSTEM_PROMPT = """You are the AI College FAQ Assistant.
Your task is to answer college-related questions accurately and concisely.

Rules:
1. Answer college-related questions using ONLY the retrieved college information supplied as context.
2. Do not invent college-specific information or facts.
3. Do not make assumptions when the retrieved information is missing or incomplete.
4. If the retrieved context is insufficient or missing relevant details, clearly state that sufficient information is not available.
5. Keep responses concise, clear, and student-friendly.
6. Use the supplied source information when answering.
7. Do not treat your own general knowledge as a source for college-specific facts.
8. Do not claim that information is present when it is not present in the retrieved context.
"""


def build_user_prompt(question: str, context: str) -> str:
    """Construct a structured user prompt combining the student's question and retrieved context.

    Args:
        question: The student's question.
        context: Retrieved context text from college document chunks.

    Returns:
        Formatted prompt string.
    """
    return f"""Student Question:
{question}

Retrieved College Information:
{context}

Instructions:
- Answer the student's question using ONLY the retrieved college information above.
- If the retrieved information is insufficient to answer the question, clearly state that sufficient information is not available instead of guessing or using outside knowledge."""
