from app.llm import call_llm
from app.retriever import retrieve_context

def executor_step(memory: dict, plan: str):
    print("\n[EXECUTOR] Executing plan:", plan)

    memory.setdefault("results", [])

    if plan == "call_llm":
        context = retrieve_context(memory["goal"])
        full_prompt = f"Context:\n{context}\n\nQuestion:\n{memory['goal']}"
        answer = call_llm(full_prompt)
        memory["results"].append(answer)
        print("\n[EXECUTOR] RESULT:\n", answer)

    elif plan == "review_result":
        last_result = memory["results"][-1] if memory["results"] else "No result to review."
        print("\n[EXECUTOR] REVIEW:\n", last_result)
        memory["reviewed"] = True