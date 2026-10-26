import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
INDEX_PATH = KNOWLEDGE_DIR / "index.json"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def split_into_chunks(text: str) -> list[str]:
    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def ingest_documents() -> int:
    documents = []

    for file_path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")
        chunks = split_into_chunks(text)

        for chunk_number, chunk in enumerate(chunks, start=1):
            documents.append(
                {
                    "source": file_path.name,
                    "chunk_id": f"{file_path.stem}-{chunk_number}",
                    "text": chunk,
                }
            )

    INDEX_PATH.write_text(
        json.dumps(documents, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return len(documents)


if __name__ == "__main__":
    count = ingest_documents()
    print(f"Created {count} chunks: {INDEX_PATH}")