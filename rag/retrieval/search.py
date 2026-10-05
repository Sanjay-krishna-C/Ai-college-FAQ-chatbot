from pathlib import Path
import re

import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# Configuration
# ============================================================

VECTORSTORE_DIR = Path("rag/vectorstore")
COLLECTION_NAME = "college_knowledge"
MODEL_NAME = "all-MiniLM-L6-v2"

RETRIEVE_K = 8
FINAL_K = 5


# ============================================================
# Load embedding model
# ============================================================

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded.")


# ============================================================
# Connect to ChromaDB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=str(VECTORSTORE_DIR)
)

collection = chroma_client.get_collection(
    name=COLLECTION_NAME
)


# ============================================================
# Basic keyword extraction
# ============================================================

def extract_keywords(text: str):
    """
    Extract useful words from the query.

    Very common words are ignored because they don't help
    identify the relevant document.
    """

    stop_words = {
        "what",
        "is",
        "are",
        "the",
        "a",
        "an",
        "to",
        "of",
        "for",
        "and",
        "or",
        "in",
        "on",
        "with",
        "can",
        "does",
        "do",
        "if",
        "how",
        "many",
        "student",
        "students",
    }

    words = re.findall(r"[a-zA-Z0-9%]+", text.lower())

    keywords = {
        word
        for word in words
        if word not in stop_words and len(word) > 2
    }

    return keywords


# ============================================================
# Keyword score
# ============================================================

def keyword_score(query: str, document: str):
    """
    Calculate a simple keyword overlap score.

    This is NOT replacing semantic search.
    It is only helping us rerank the retrieved chunks.
    """

    query_keywords = extract_keywords(query)

    if not query_keywords:
        return 0.0

    document_lower = document.lower()

    matches = 0

    for keyword in query_keywords:
        if keyword in document_lower:
            matches += 1

    return matches / len(query_keywords)


# ============================================================
# Reranking
# ============================================================

def rerank_results(query: str, results):
    """
    Combine semantic distance with simple keyword matching.

    Lower final score = better result.
    """

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    ranked = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        score = keyword_score(query, document)

        # Convert keyword score into a small bonus.
        keyword_bonus = score * 0.35

        # R2026 is the current regulation document.
        # Give it a small preference when it is already
        # semantically relevant.
        source_bonus = 0.0

        source_name = metadata["source"]

        if "R2026" in source_name:
            source_bonus = 0.05

        final_score = distance - keyword_bonus - source_bonus

        ranked.append({
            "document": document,
            "metadata": metadata,
            "distance": distance,
            "keyword_score": score,
            "final_score": final_score,
        })

    ranked.sort(key=lambda item: item["final_score"])

    return ranked[:FINAL_K]


# ============================================================
# Search
# ============================================================

def search(query: str, retrieve_k: int = RETRIEVE_K):

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=retrieve_k
    )

    return rerank_results(query, results)


# ============================================================
# Display results
# ============================================================

def display_results(results):

    print("\n" + "=" * 70)
    print("RERANKED RESULTS")
    print("=" * 70)

    for i, result in enumerate(results, start=1):

        print(f"\n--- RESULT {i} ---")

        print(f"Source        : {result['metadata']['source']}")
        print(f"Chunk         : {result['metadata']['chunk_id']}")
        print(f"Distance      : {result['distance']:.4f}")
        print(f"Keyword score : {result['keyword_score']:.4f}")
        print(f"Final score   : {result['final_score']:.4f}")

        print("\nContent:")
        print(result["document"][:700])

        if len(result["document"]) > 700:
            print("...")


# ============================================================
# Main
# ============================================================

def main():

    query = input("\nAsk a college question: ").strip()

    if not query:
        print("Please enter a question.")
        return

    results = search(query)

    display_results(results)

    print("\n" + "=" * 70)
    print("RETRIEVAL COMPLETE")
    print("=" * 70)

    print(f"Retrieved and reranked: {len(results)} chunks")

    print("=" * 70)


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()