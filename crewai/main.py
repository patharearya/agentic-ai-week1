import config
from crew_setup import crew

topic = input("Enter a topic: ")
result = crew.kickoff(inputs={"topic": topic})

print("\n\n========================")
print("FINAL RESULT:")
print(result)