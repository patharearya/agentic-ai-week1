from app.agent import run_agent

if __name__ == "__main__":
    with open("app/notice.txt", "r", encoding="utf-8") as f:
        notice = f.read()

    goal = f"Explain this college notice in simple words:\n{notice}"
    run_agent(goal)