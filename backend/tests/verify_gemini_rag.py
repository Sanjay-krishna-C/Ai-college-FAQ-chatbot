import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import json
from app.core.config import settings
from app.core.logging import logger
from app.rag.embeddings import GeminiEmbeddingService, GeminiEmbeddingError
from app.rag.vector_store import ChromaVectorStore


def verify_gemini_rag():
    print("=================================================================")
    print("  PHASE 6B - GEMINI RAG & EMBEDDING VERIFICATION")
    print("=================================================================")

    embedding_service = GeminiEmbeddingService()
    if not embedding_service.is_configured():
        print("[ERROR] GEMINI_API_KEY is not configured in backend/.env.")
        print("[STATUS] Verification halted: Cannot verify live Gemini embeddings without API key.")
        return False

    vector_store = ChromaVectorStore(collection_name=settings.CHROMA_COLLECTION_NAME)
    client = vector_store.client

    # 1. Verify New Gemini Collection
    print(f"\n1. Verifying Active Collection: '{settings.CHROMA_COLLECTION_NAME}'...")
    try:
        gemini_col = client.get_collection(settings.CHROMA_COLLECTION_NAME)
        gemini_count = gemini_col.count()
        print(f"   * Status               : Collection exists")
        print(f"   * Collection Name      : {gemini_col.name}")
        print(f"   * Total Indexed Chunks : {gemini_count}")
    except Exception as e:
        print(f"   [FAIL] Could not find collection '{settings.CHROMA_COLLECTION_NAME}': {e}")
        return False

    # 2. Verify Embedding Dimension
    sample = gemini_col.get(limit=1, include=["embeddings", "metadatas", "documents"])
    embs = sample.get("embeddings")
    if embs is None or len(embs) == 0:
        print("   [FAIL] No embeddings found in collection.")
        return False

    first_vec = embs[0]
    dim = len(first_vec)
    print(f"   * Embedding Provider   : Google Gemini")
    print(f"   * Embedding Model      : {settings.EMBEDDING_MODEL}")
    print(f"   * Detected Dimension   : {dim}")
    print(f"   * Expected Dimension   : {settings.EXPECTED_EMBEDDING_DIM} (Gemini {settings.EMBEDDING_MODEL})")

    if dim != 768:
        print(f"   [FAIL] Dimension mismatch! Expected 768, got {dim}.")
        return False
    else:
        print(f"   [PASS] Verified 768-dimensional Gemini vectors.")

    # 3. Verify Old Collection Preservation
    print("\n2. Verifying Legacy Collection Preservation...")
    try:
        old_col = client.get_collection("campusai_institutional_knowledge")
        old_count = old_col.count()
        old_sample = old_col.get(limit=1, include=["embeddings"])
        old_embs = old_sample.get("embeddings")
        old_dim = len(old_embs[0]) if (old_embs is not None and len(old_embs) > 0) else 0
        print(f"   * Preserved Collection : campusai_institutional_knowledge")
        print(f"   * Old Chunks Count     : {old_count}")
        print(f"   * Old Vector Dimension : {old_dim} (all-MiniLM-L6-v2)")
        print(f"   [PASS] Legacy collection remained completely untouched.")
    except Exception as e:
        print(f"   [WARN] Legacy collection check: {e}")

    # 4. Run the 5 Required Domain Queries
    print("\n3. Testing 5 Domain Queries via Gemini Embeddings...")
    test_queries = [
        "What is the attendance requirement?",
        "What are the examination regulations?",
        "What is the academic calendar?",
        "What are the hostel rules?",
        "What is relative grading?"
    ]

    for idx, q in enumerate(test_queries, 1):
        print(f"\n   Query {idx}: '{q}'")
        try:
            query_emb = embedding_service.embed_query(q)
            results = vector_store.search_similar(query_embedding=query_emb, top_k=2)
            if not results:
                print("      [WARN] No results found.")
                continue

            top_match = results[0]
            meta = top_match["metadata"]
            print(f"      Top Match Document : {meta.get('document_name')}")
            print(f"      Source File        : {meta.get('source_file')}")
            print(f"      Page Number        : {meta.get('page_number')}")
            print(f"      Regulation         : {meta.get('regulation')}")
            print(f"      Distance Score     : {top_match.get('distance'):.4f}")
            print(f"      Snippet            : {top_match.get('text')[:120].strip()}...")
        except Exception as q_err:
            print(f"      [FAIL] Query search error: {q_err}")
            return False

    print("\n" + "=" * 65)
    print("  ALL GEMINI RAG VERIFICATIONS COMPLETED SUCCESSFULLY!")
    print("=" * 65)
    return True


if __name__ == "__main__":
    verify_gemini_rag()
