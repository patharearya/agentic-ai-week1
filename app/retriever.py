def retrieve_context(query: str) -> str:
    print("[RETRIEVER] Searching knowledge base")

    with open("app/knowledge.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    matched = [line.strip() for line in lines if any(word.lower() in line.lower() for word in query.split())]

    if not matched:
        return "No relevant context found."

    return " ".join(matched)