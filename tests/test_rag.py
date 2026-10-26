import pytest

from genai.retriever import Retriever


def test_retriever_finds_cancellation_policy():
    retriever = Retriever()

    results = retriever.search(
        query="Can I cancel an order that is already being prepared?",
        top_k=3
    )

    assert results
    
    assert any(result["source"] == "cancellation_policy.md"
               for result in results)


def test_retriever_finds_weather_guidelines():
    retriever = Retriever()

    results = retriever.search(
        query="How can snow and icy roads affect delivery?",
        top_k=3
    )

    assert results
    
    assert any(result["source"] == "weather_delivery_guidelines.md"
               for result in results)


def test_retriever_rejects_empty_query():
    retriever = Retriever()

    with pytest.raises(ValueError, match="Query must not be empty"):
        retriever.search("  ")


def test_retriever_returns_valid_metadata():
    retriever = Retriever()

    results = retriever.search(
        query="How can I track my order?",
        top_k=3
    )

    assert results

    for result in results:
        assert result["source"]
        assert result["chunk_id"]
        assert result["text"]
        assert 0 <= result["score"] <= 1


def test_retriever_rejects_invalid_top_k():
    retriever = Retriever()

    with pytest.raises(ValueError, match="top_k must be at least 1"):
        retriever.search(query="How can I track my order?",
                         top_k=0)

