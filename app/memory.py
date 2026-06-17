import json
import os

MEMORY_FILE = "app/memory.json"

def init_memory(goal: str) -> dict:
    if os.path.exists(MEMORY_FILE):
        print("[MEMORY] Loading memory from file")
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)
        memory["goal"] = goal
        return memory

    print("[MEMORY] Initializing fresh memory")
    return {
        "goal": goal,
        "steps": [],
        "completed": False,
        "tool_retries": 0
    }


def save_memory(memory: dict):
    print("[MEMORY] Saving memory to file")
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)