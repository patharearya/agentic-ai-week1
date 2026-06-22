from app.chunking_strategies import (
    line_based_chunking,
    paragraph_based_chunking,
    fixed_size_chunking,
    overlapping_chunking
)
from app.retriever import keyword_retrieval

def demo_chunking_and_retrieval():
    text = open("app/knowledge.txt", encoding="utf-8").read()

    question = "What is the scholarship deadline?"

    print("\n==============================")
    print("QUESTION:", question)
    print("==============================")

    strategies = {
        "Line-Based": line_based_chunking(text),
        "Paragraph-Based": paragraph_based_chunking(text),
        "Fixed-Size": fixed_size_chunking(text, size=120),
        "Overlapping": overlapping_chunking(text, size=120, overlap=30),
    }

    for name, chunks in strategies.items():
        print(f"\n========== {name} ==========")
        print(f"Total Chunks: {len(chunks)}")

        relevant = keyword_retrieval(chunks, question)

        print("\nRelevant Chunks:")
        if relevant:
            for r in relevant:
                print("-", r)
        else:
            print("No relevant chunk found.")

if __name__ == "__main__":
    demo_chunking_and_retrieval()