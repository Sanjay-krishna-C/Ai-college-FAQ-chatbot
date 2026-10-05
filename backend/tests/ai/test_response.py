from app.modules.ai.response import (
    DEFAULT_ERROR_MESSAGE,
    DEFAULT_INSUFFICIENT_CONTEXT_MESSAGE,
    build_error_response,
    build_grounded_response,
    build_insufficient_context_response,
)
from app.modules.ai.schemas import ResponseStatus, RetrievedChunk, RetrievedContext


def test_grounded_response_contains_generated_answer():
    """1. Test that grounded response stores the generated answer."""
    chunk = RetrievedChunk(text="Library hours 8am-10pm", source="guide.pdf", page=5)
    context = RetrievedContext(query="Library hours?", chunks=[chunk])
    answer = "The library is open from 8am to 10pm."

    res = build_grounded_response(answer, context)
    assert res.answer == answer


def test_grounded_response_has_grounded_status():
    """2. Test that grounded response has status 'grounded'."""
    chunk = RetrievedChunk(text="Fee is $5000", source="fee.pdf", page=1)
    context = RetrievedContext(query="Fee?", chunks=[chunk])

    res = build_grounded_response("Fee is $5000", context)
    assert res.status == ResponseStatus.GROUNDED
    assert res.status == "grounded"


def test_source_filename_preserved():
    """3. Test that source filename is preserved in source references."""
    chunk = RetrievedChunk(text="Hostel rules", source="academic_regulations.pdf", page=12)
    context = RetrievedContext(query="Hostel rules?", chunks=[chunk])

    res = build_grounded_response("Rules apply", context)
    assert len(res.sources) == 1
    assert res.sources[0].source == "academic_regulations.pdf"


def test_page_number_preserved():
    """4. Test that page number is preserved in source references."""
    chunk = RetrievedChunk(text="Exam rules", source="exams.pdf", page=42)
    context = RetrievedContext(query="Exam rules?", chunks=[chunk])

    res = build_grounded_response("Exam rules detail", context)
    assert res.sources[0].page == 42


def test_multiple_retrieved_chunks_produce_source_references():
    """5. Test that multiple retrieved chunks produce appropriate source references."""
    c1 = RetrievedChunk(text="Part 1", source="doc1.pdf", page=1)
    c2 = RetrievedChunk(text="Part 2", source="doc2.pdf", page=10)
    context = RetrievedContext(query="Query", chunks=[c1, c2])

    res = build_grounded_response("Combined answer", context)
    assert len(res.sources) == 2
    assert res.sources[0].source == "doc1.pdf"
    assert res.sources[0].page == 1
    assert res.sources[1].source == "doc2.pdf"
    assert res.sources[1].page == 10


def test_duplicate_source_page_entries_handled_cleanly():
    """6. Test that duplicate source/page entries are deduplicated."""
    c1 = RetrievedChunk(text="Text segment A", source="handbook.pdf", page=3)
    c2 = RetrievedChunk(text="Text segment B", source="handbook.pdf", page=3)
    c3 = RetrievedChunk(text="Text segment C", source="handbook.pdf", page=4)
    context = RetrievedContext(query="Query", chunks=[c1, c2, c3])

    res = build_grounded_response("Deduplicated answer", context)
    assert len(res.sources) == 2
    assert res.sources[0].source == "handbook.pdf"
    assert res.sources[0].page == 3
    assert res.sources[1].source == "handbook.pdf"
    assert res.sources[1].page == 4


def test_insufficient_context_response_has_correct_status():
    """7. Test that insufficient context response has status 'insufficient_context'."""
    res = build_insufficient_context_response()
    assert res.status == ResponseStatus.INSUFFICIENT_CONTEXT
    assert res.status == "insufficient_context"


def test_insufficient_context_response_has_no_sources():
    """8. Test that insufficient context response has an empty sources list."""
    res = build_insufficient_context_response()
    assert res.sources == []
    assert len(res.sources) == 0


def test_error_response_has_error_status():
    """9. Test that error response has status 'error'."""
    res = build_error_response()
    assert res.status == ResponseStatus.ERROR
    assert res.status == "error"


def test_error_response_does_not_expose_internal_details():
    """10. Test that error response returns a clean user-friendly message without stack traces/API keys."""
    res = build_error_response()
    assert res.answer == DEFAULT_ERROR_MESSAGE
    assert "Traceback" not in res.answer
    assert "Exception" not in res.answer
    assert "API_KEY" not in res.answer
    assert res.sources == []
