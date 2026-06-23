import config
from crew_setup import crew

topic = "Artificial Intelligence"
result = crew.kickoff(inputs={"topic": topic})

print("\n\n========================")
print("FINAL RESULT:")
print(result)