from app.memory import init_memory
from app.planner_agent import planner_step
from app.executor_agent import executor_step

if __name__ == "__main__":
    goal = "Explain the Aurangabad college exam form process, deadlines, and consequences of late submission in simple words."

    memory = init_memory(goal)

    print("\n[MAIN] Starting Multi-Agent System")
    print("[MAIN] Goal:", goal)

    while not memory["completed"]:
        plan = planner_step(memory)

        if plan == "stop":
            break

        executor_step(memory, plan)

    print("\n[MAIN] System finished cleanly")