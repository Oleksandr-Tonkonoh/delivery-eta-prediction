import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = PROJECT_ROOT / "knowledge" / "index.json"

MIN_SIMILARITY = 0.05


class Retriever:
    def __init__(self, index_path: Path = INDEX_PATH):
        self.index_path = Path(index_path)
        self.documents = []
        self.vectorizer = None
        self.document_vectors = None
        self._load_index()


    def _load_index(self) -> None:
        if not self.index_path.exists():
            raise FileNotFoundError(
                f"Knowledge index not found: {self.index_path}. "
                "Run python -m genai.ingest first."
            )

        self.documents = json.loads(
            self.index_path.read_text(encoding='utf-8')
        )

        if not self.documents:
            raise ValueError("Knowledge index is empty")

        texts = [document["text"] for document in self.documents]

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            stop_words='english'
        )

        self.document_vectors = self.vectorizer.fit_transform(texts)


    def search(self, query: str, top_k: int = 3) -> list[dict]:
        query = query.strip()

        if not query:
            raise ValueError("Query must not be empty")

        if top_k < 1:
            raise ValueError("top_k must be at least 1")

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.document_vectors
        ).flatten()

        ranked_indexes = scores.argsort()[::-1]

        results = []

        for index in ranked_indexes:
            score = float(scores[index])

            if score < MIN_SIMILARITY:
                break

            document = self.documents[index]

            results.append(
                {
                    "source": document["source"],
                    "chunk_id": document["chunk_id"],
                    "text": document["text"],
                    "score": score,
                }
            )

            if len(results) >= top_k:
                break

        return results