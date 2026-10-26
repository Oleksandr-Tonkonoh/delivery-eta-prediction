from unittest.mock import Mock

import pytest

from genai import rag_service
from genai.llm_client import LLMClientError


def test_answer_delivery_question_success(monkeypatch):
    question = "How can I track my order?"

    search_results = [
        {
            "source": "courier_faq.md",
            "chunk_id": "courier_faq-1",
            "text": "Customers can track their order using the tracking link.",
            "score": 0.456789,
        }
    ]


    search_mock = Mock(return_value=search_results)
    llm_mock = Mock(return_value="Use the tracking link to track your order.")


    monkeypatch.setattr(rag_service.retriever, "search", search_mock)
    monkeypatch.setattr(rag_service, "generate_RAG_response", llm_mock)


    result = rag_service.answer_delivery_question(question=question)

    assert result["answer"] == "Use the tracking link to track your order."
    assert result["sources"] == [
        {
            "source": "courier_faq.md",
            "chunk_id": "courier_faq-1",
            "score": 0.4568,
        }
    ]

    search_mock.assert_called_once_with(query=question, top_k= 3)
    llm_mock.assert_called_once()


def test_answer_delivery_question_empty_query():
    with pytest.raises(ValueError, match="Question must not be empty",):
        rag_service.answer_delivery_question(question="   ")


def test_answer_delivery_question_no_results(monkeypatch):
    question = "What is the policy on space travel?"

    search_mock = Mock(return_value=[])
    llm_mock = Mock() 


    monkeypatch.setattr(rag_service.retriever, "search", search_mock)
    monkeypatch.setattr(rag_service, "generate_RAG_response", llm_mock)


    result = rag_service.answer_delivery_question(question=question)

    assert result["sources"] == []
    assert "could not find enough information" in result["answer"].lower()
    llm_mock.assert_not_called()


def test_answer_delivery_question_llm_error_propagates(monkeypatch):
    question = "How can I track my order?"
    
    search_results = [
        {
            "source": "courier_faq.md",
            "chunk_id": "courier_faq-1",
            "text": "Customers can track their order using the tracking link.",
            "score": 0.456789,
        }
    ]

    search_mock = Mock(return_value=search_results)


    monkeypatch.setattr(rag_service.retriever, "search", search_mock)
    monkeypatch.setattr(rag_service, 
                        "generate_RAG_response", 
                        Mock(side_effect=LLMClientError("LLM request failed")))


    with pytest.raises(LLMClientError, match="LLM request failed"):
        rag_service.answer_delivery_question(question=question)


def test_answer_does_not_add_sources_section(monkeypatch):
    question = "How can I track my order?"

    search_results = [
        {
            "source": "courier_faq.md",
            "chunk_id": "courier_faq-1",
            "text": "Customers can track their orders using the tracking page.",
            "score": 0.5,
        }
    ]

    answer_without_sources = (
        "Customers can track their orders using the tracking page."
    )

    search_mock = Mock(return_value=search_results)
    without_sources_mock = Mock(return_value=answer_without_sources)

    monkeypatch.setattr(rag_service.retriever, "search", search_mock)
    monkeypatch.setattr(rag_service, "generate_RAG_response", without_sources_mock)

    result = rag_service.answer_delivery_question(question)

    assert result["answer"] == answer_without_sources
    assert "Sources:" not in result["answer"]
    assert result["sources"][0]["source"] == "courier_faq.md"