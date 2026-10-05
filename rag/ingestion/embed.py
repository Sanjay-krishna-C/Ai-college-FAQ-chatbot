from pathlib import Path
import re

import chromadb
from sentence_transformers import SentenceTransformer


CHUNKS_DIR = Path("rag/data/chunks")
VECTORSTORE_DIR = Path("rag/vectorstore")

COLLECTION_NAME = "college_knowledge"

MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 32


print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)
print("Embedding model loaded.")


chroma_client = chromadb.PersistentClient(
    path=str(VECTORSTORE_DIR)
)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME
)


def load_chunks():
    documents = []
    ids = []
    metadatas = []

    for file_path in CHUNKS_DIR.glob("*_chunks.txt"):
        text = file_path.read_text(encoding="utf-8")

        parts = re.split(r"--- CHUNK (\d+) ---", text)

        source_name = file_path.stem.replace("_chunks", "")

        for i in range(1, len(parts), 2):
            chunk_number = parts[i]
            chunk_text = parts[i + 1].strip()

            if not chunk_text:
                continue

            chunk_id = f"{source_name}_chunk_{chunk_number}"

            documents.append(chunk_text)
            ids.append(chunk_id)

            metadatas.append({
                "source": source_name,
                "chunk_id": int(chunk_number),
            })

    return documents, ids, metadatas


def create_embeddings(documents):
    print(f"Creating embeddings for {len(documents)} chunks...")

    embeddings = model.encode(
        documents,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    return embeddings.tolist()


def main():
    documents, ids, metadatas = load_chunks()

    if not documents:
        print("No chunks found.")
        return

    print(f"Loaded {len(documents)} chunks.")

    embeddings = create_embeddings(documents)

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print("\nIndexing completed!")
    print(f"Stored documents: {collection.count()}")
    print(f"Collection: {COLLECTION_NAME}")


if __name__ == "__main__":
    main()