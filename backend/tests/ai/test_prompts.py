from app.modules.ai.prompts import SYSTEM_PROMPT, build_user_prompt


def test_system_prompt_exists_and_not_empty():
    """1. Test that SYSTEM_PROMPT exists and is a non-empty string."""
    assert isinstance(SYSTEM_PROMPT, str)
    assert len(SYSTEM_PROMPT.strip()) > 0
    assert "AI College FAQ Assistant" in SYSTEM_PROMPT


def test_user_prompt_contains_question():
    """2. Test that the generated prompt contains the student's question."""
    question = "What is the application deadline?"
    context = "The application deadline for Fall 2026 is June 30."
    prompt = build_user_prompt(question, context)
    assert question in prompt


def test_user_prompt_contains_context():
    """3. Test that the generated prompt contains the retrieved context."""
    question = "What is the application deadline?"
    context = "The application deadline for Fall 2026 is June 30."
    prompt = build_user_prompt(question, context)
    assert context in prompt


def test_user_prompt_instructs_only_retrieved_information():
    """4. Test that the generated prompt explicitly tells the model to use only retrieved information."""
    prompt = build_user_prompt("How much is tuition?", "Tuition is $10,000 per year.")
    assert "ONLY" in prompt or "only" in prompt.lower()
    assert "retrieved college information" in prompt.lower()


def test_user_prompt_contains_insufficient_information_instruction():
    """5. Test that the generated prompt contains an insufficient-information instruction."""
    prompt = build_user_prompt("Where is campus library?", "Library details unavailable.")
    assert "insufficient" in prompt.lower()
    assert "sufficient information is not available" in prompt.lower()


def test_user_prompt_handles_different_questions_and_contexts():
    """6. Test that different questions and contexts are correctly inserted without losing values."""
    q1 = "Is financial aid available?"
    c1 = "Financial aid is offered to eligible undergraduate students."
    prompt1 = build_user_prompt(q1, c1)
    assert q1 in prompt1
    assert c1 in prompt1

    q2 = "What are the hostel rules?"
    c2 = "Curfew time for all hostels is 10:00 PM."
    prompt2 = build_user_prompt(q2, c2)
    assert q2 in prompt2
    assert c2 in prompt2
    assert q1 not in prompt2
    assert c1 not in prompt2
