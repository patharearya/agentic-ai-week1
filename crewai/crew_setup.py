from crewai import Crew
from agents import planner, writer, editor
from tasks import plan, write, edit

crew = Crew(
    tasks=[plan, write, edit],
    agents=[planner, writer, editor],
    verbose=False
)