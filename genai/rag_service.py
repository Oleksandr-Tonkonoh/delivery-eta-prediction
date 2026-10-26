import json
from .llm_client import generate_RAG_response
from .retriever import Retriever


retriever= Retriever()


def answer_delivery_question(question: str) -> dict:
    question = question.strip()

    if not question:
        raise ValueError("Question must not be empty")

    results = retriever.search(query=question,
                               top_k=3)

    if not results:
        return {
            "answer": (
                "I could not find enough information in the delivery "
                "documents to answer this question. Please contact "
                "customer support."
            ),
            "sources": [],
        }


    context_documents = [
        {
            "source": result["source"],
            "chunk_id": result["chunk_id"],
            "text": result["text"],
        }
        for result in results
    ]


    llm_input = json.dumps(
        {
            "question": question,
            "context": context_documents
        },
        ensure_ascii=False,
        indent=2
    )

    answer = generate_RAG_response(input=llm_input)

    return {
        "answer": answer,
        "sources": [
            {
                "source": result["source"],
                "chunk_id": result["chunk_id"],
                "score": round(result["score"], 4)
            }
            for result in results
        ]
    }

