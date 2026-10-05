from pathlib import Path
from pypdf import PdfReader


KNOWLEDGE_DIR = Path("knowledge")
OUTPUT_DIR = Path("rag/data/extracted")


def extract_pdf(pdf_path: Path):
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append(
            f"\n--- PAGE {page_number} ---\n{text}"
        )

    return "\n".join(pages)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(KNOWLEDGE_DIR.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF(s).\n")

    for pdf_path in pdf_files:
        print(f"Extracting: {pdf_path.name}")

        text = extract_pdf(pdf_path)

        output_path = OUTPUT_DIR / f"{pdf_path.stem}.txt"
        output_path.write_text(text, encoding="utf-8")

        print(f"Saved: {output_path}\n")

    print("PDF extraction completed.")


if __name__ == "__main__":
    main()