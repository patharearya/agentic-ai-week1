import os
from dotenv import load_dotenv
 
# Load environment variables from .env file
load_dotenv()
 
# Get environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")
phoenix_api_key = os.getenv("PHOENIX_API_KEY")
phoenix_endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT")
 
# Validate required environment variables
required_vars = {
    "OPENAI_API_KEY": openai_api_key,
    "SERPER_API_KEY": serper_api_key,
    "PHOENIX_API_KEY": phoenix_api_key,
    "PHOENIX_COLLECTOR_ENDPOINT": phoenix_endpoint,
}
 
missing_vars = [key for key, value in required_vars.items() if not value]
if missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_vars)}. "
        "Please set them in your .env file."
    )
 
# ============================================================================
# Get Started with Tracing
# ============================================================================
 
from phoenix.otel import register

tracer_provider = register(
    project_name="crewai-tracing-quickstart",
    auto_instrument=True,
    endpoint="https://app.phoenix.arize.com/v1/traces",
    headers={"Authorization": f"Bearer {phoenix_api_key}"},
)
 
from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool
 
search_tool = SerperDevTool()
 
researcher = Agent(
    role="Financial Research Analyst",
    goal="Gather up-to-date financial data, trends, and news for the target companies or markets",
    backstory="""
        You are a Senior Financial Research Analyst.
    """,
    verbose=True,
    allow_delegation=False,
    max_iter=2,
    tools=[search_tool],
)
 
writer = Agent(
    role="Financial Report Writer",
    goal="Compile and summarize financial research into clear, actionable insights",
    backstory="""
        You are an experienced financial content writer.
    """,
    verbose=True,
    allow_delegation=True,
    max_iter=1,
)
 
task1 = Task(
    description="""
        Research: {tickers}
        Focus on: {focus}
    """,
    expected_output="Detailed financial research summary with web search findings",
    agent=researcher,
)
 
task2 = Task(
    description="Write a report based on the research above.",
    expected_output="A polished financial analysis report",
    agent=writer,
)
 
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=1,
    process=Process.sequential,
)
 
user_inputs = {"tickers": "TSLA", "focus": "financial analysis and market outlook"}
 
result = crew.kickoff(inputs=user_inputs)