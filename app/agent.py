from app.control import decide_next_step
from app.llm import call_llm
from app.tools import joke_tool
from app.memory import init_memory, save_memory

def run_agent(goal: str):
    memory = init_memory(goal)

    print("\n[AGENT] Starting agent")
    print("[AGENT] Goal:", goal)

    while True:
        step = decide_next_step(memory)
        print("[AGENT] Control decided:", step)

        if step == "call_llm":
            result = call_llm(goal)
            memory["steps"].append(result)

            if result == "LLM_FAILED":
                memory["tool_retries"] += 1

        elif step == "use_tool":
            tool_result = joke_tool()
            print("[AGENT] Tool Result:", tool_result)
            memory["steps"].append(tool_result)
            memory["completed"] = True

        elif step == "stop":
            print("[AGENT] Agent stopped cleanly")
            save_memory(memory)
            break