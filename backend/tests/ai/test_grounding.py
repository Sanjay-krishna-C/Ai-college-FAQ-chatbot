from app.modules.ai.grounding import has_sufficient_context
from app.modules.ai.schemas import RetrievedChunk, RetrievedContext


def test_one_valid_chunk_returns_true():
    """1. Test that one chunk with valid non-empty text returns True."""
    chunk = RetrievedChunk(text="Attendance requirement is 75%.", source="handbook.pdf", page=12)
    context = RetrievedContext(query="What is attendance rule?", chunks=[chunk])
    assert has_sufficient_context(context) is True


def test_multiple_valid_chunks_returns_true():
    """2. Test that multiple valid chunks return True."""
    c1 = RetrievedChunk(text="Attendance rule is 75%.", source="handbook.pdf", page=12)
    c2 = RetrievedChunk(text="Medical leave allows 65%.", source="handbook.pdf", page=13)
    context = RetrievedContext(query="Attendance requirements?", chunks=[c1, c2])
    assert has_sufficient_context(context) is True


def test_no_chunks_returns_false():
    """3. Test that empty chunks list returns False."""
    context = RetrievedContext(query="What is the fee?", chunks=[])
    assert has_sufficient_context(context) is False


def test_chunk_with_empty_text_returns_false():
    """4. Test that chunk with empty string text returns False."""
    chunk = RetrievedChunk(text="", source="doc.pdf", page=1)
    context = RetrievedContext(query="Question?", chunks=[chunk])
    assert has_sufficient_context(context) is False


def test_chunk_with_whitespace_only_text_returns_false():
    """5. Test that chunk with whitespace-only text returns False."""
    chunk = RetrievedChunk(text="   \n\t  ", source="doc.pdf", page=1)
    context = RetrievedContext(query="Question?", chunks=[chunk])
    assert has_sufficient_context(context) is False


def test_mixed_chunks_with_at_least_one_valid_returns_true():
    """6. Test that mixed chunks containing at least one valid text return True."""
    c1 = RetrievedChunk(text="   ", source="doc1.pdf", page=1)
    c2 = RetrievedChunk(text="Library closes at 10 PM.", source="doc2.pdf", page=5)
    c3 = RetrievedChunk(text="", source="doc3.pdf", page=2)
    context = RetrievedContext(query="Library hours?", chunks=[c1, c2, c3])
    assert has_sufficient_context(context) is True
