def retrieve_context(query: str) -> str:
    print("[RETRIEVER] Searching knowledge base")

    with open("app/knowledge.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    matched = [line.strip() for line in lines if any(word.lower() in line.lower() for word in query.split())]

    if not matched:
        return "No relevant context found."

    return " ".join(matched)


def keyword_retrieval(chunks: list, question: str) -> list:
    print("\n[RETRIEVER] Performing Keyword Search")

    relevant_chunks = []

    for chunk in chunks:
        for word in question.lower().split():
            if word in chunk.lower():
                relevant_chunks.append(chunk)
                break

    return relevant_chunks