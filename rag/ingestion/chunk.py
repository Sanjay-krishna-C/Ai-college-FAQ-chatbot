from pathlib import Path
import re


INPUT_DIR = Path("rag/data/extracted")
OUTPUT_DIR = Path("rag/data/chunks")

CHUNK_SIZE = 2200
CHUNK_OVERLAP = 300


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
def create_chunks(text: str):
    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + CHUNK_SIZE, text_length)

        # Try to find a natural paragraph boundary
        if end < text_length:
            paragraph_break = text.rfind("\n\n", start, end)

            if paragraph_break > start + 500:
                end = paragraph_break

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Always move forward by at least the chunk size minus overlap
        next_start = end - CHUNK_OVERLAP

        if next_start <= start:
            next_start = start + CHUNK_SIZE - CHUNK_OVERLAP

        start = next_start

    return chunks
    
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    txt_files = list(INPUT_DIR.glob("*.txt"))

    print(f"Found {len(txt_files)} extracted document(s).\n")

    total_chunks = 0

    for txt_path in txt_files:
        print(f"Chunking: {txt_path.name}")

        text = txt_path.read_text(encoding="utf-8")
        text = clean_text(text)

        chunks = create_chunks(text)

        output_path = OUTPUT_DIR / f"{txt_path.stem}_chunks.txt"

        with output_path.open("w", encoding="utf-8") as f:
            for i, chunk in enumerate(chunks, start=1):
                f.write(f"\n--- CHUNK {i} ---\n")
                f.write(chunk)
                f.write("\n")

        print(f"Created {len(chunks)} chunks.")
        total_chunks += len(chunks)

    print(f"\nTotal chunks created: {total_chunks}")


if __name__ == "__main__":
    main()