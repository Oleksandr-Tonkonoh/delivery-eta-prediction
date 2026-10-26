from genai.retriever import Retriever

retriever = Retriever()

questions = [
    "Can I cancel an order that is already being prepared?",
    "How can snow and icy roads affect delivery?",
    "How can I track my order?",
    "Is the estimated delivery time guaranteed?",
    "What is the policy on space travel?",
]

for question in questions:
    print("\n" + "=" * 70)
    print(f"QUESTION: {question}")

    results = retriever.search(question, top_k=3)

    if not results:
        print("No relevant documents found.")
        continue

    for result in results:
        print(f"\nSource: {result['source']}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Similarity: {result['score']:.4f}")
        print(f"Text: {result['text']}")