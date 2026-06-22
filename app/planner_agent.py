def planner_step(memory: dict) -> str:
    print("\n[PLANNER] Reviewing memory:", memory)

    memory.setdefault("plan", [])

    if len(memory["plan"]) == 0:
        step = "call_llm"
        memory["plan"].append(step)
        print("[PLANNER] Plan created:", step)
        return step

    if len(memory["plan"]) == 1:
        step = "review_result"
        memory["plan"].append(step)
        print("[PLANNER] Plan created:", step)
        return step

    memory["completed"] = True
    print("[PLANNER] Plan complete → STOP")
    return "stop"