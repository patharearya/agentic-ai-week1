def observe_output(text: str, memory: dict):
    print("\nNEWS SUMMARY:")
    print(text)
    memory["steps"].append("observed")
    