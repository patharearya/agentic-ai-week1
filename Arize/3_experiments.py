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
# Get Started with Experiments
# ============================================================================

from phoenix.otel import register

tracer_provider = register(project_name="crewai-tracing-quickstart", auto_instrument=True)

from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

researcher = Agent(
    role="Financial Research Analyst",
    goal="""Gather up-to-date financial data, trends, and news for the target companies/markets.
        Make sure to include more than 1 financial ratios (such as P/E or P/B), news from the last 6 months, and current stock price or performance data.""",
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
    goal="Compile and summarize financial research into clear, actionable insights. If there are multiple tickers, make sure to include a dedicated comparison section.",
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

updated_crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=1,
    process=Process.sequential,
)


def my_task(example):
    result = updated_crew.kickoff(inputs=example.input)
    return result


financial_completeness_template = """
You are evaluating whether a financial research report correctly completes ALL parts of the user's task with COMPREHENSIVE coverage.
User input: {attributes.input.value}
Generated report:
{attributes.output.value}
To be marked as "complete", the report MUST meet ALL of these strict requirements:
1. TICKER COVERAGE (MANDATORY):
   - Cover ALL companies/tickers mentioned in the input
   - If multiple tickers are listed, EACH must have dedicated analysis (not just mentioned in passing)
   - For multiple tickers, the report must provide COMPARATIVE analysis when relevant
2. FOCUS AREA COVERAGE (MANDATORY):
   - Address ALL focus areas mentioned in the input
   - If the focus mentions multiple topics (e.g., "earnings and outlook"), BOTH must be thoroughly addressed
   - Each focus area must have substantial content, not just a brief mention
3. FINANCIAL DATA REQUIREMENTS (MANDATORY):
   - For EACH ticker, the report must include:
     * Current/recent stock price or performance data
     * At least 2 key financial ratios (P/E, P/B, debt-to-equity, ROE, etc.)
     * Revenue or earnings information
     * Recent news or developments (within last 6 months)
   - If focus mentions specific metrics (e.g., "P/E ratio"), those MUST be explicitly provided
4. DEPTH REQUIREMENT (MANDATORY):
   - Each ticker must have at least 3-4 sentences of dedicated analysis
   - Generic statements without specific data do NOT count
   - The report must demonstrate thorough research, not superficial coverage
5. COMPARISON REQUIREMENT (if multiple tickers):
   - If 2+ tickers are requested, the report MUST include direct comparisons
   - Comparisons should cover multiple key metrics side-by-side
   - Generic statements like "both companies are good" do NOT satisfy this requirement
   - Must explicitly state which company performs better/worse on specific metrics
The report is "incomplete" if it fails ANY of the above requirements, including:
- Missing any ticker or only mentioning it briefly
- Failing to address any focus area or only addressing it superficially
- Missing required financial data for any ticker
- Providing generic analysis without specific metrics or data
- Failing to provide comparisons when multiple tickers are requested
- Not meeting the depth requirement for any ticker
Respond with ONLY one word: "complete" or "incomplete"
Then provide a detailed explanation of which specific requirements were met or failed.
"""

from phoenix.evals import LLM

llm = LLM(model="gpt-4o", provider="openai")

from phoenix.evals import ClassificationEvaluator

completeness_evaluator = ClassificationEvaluator(
    name="completeness",
    prompt_template=financial_completeness_template,
    llm=llm,
    choices={"complete": 1.0, "incomplete": 0.0},
)


def completeness(input, output):
    results = completeness_evaluator.evaluate(
        {"attributes.input.value": input, "attributes.output.value": output}
    )
    return results[0].score


evaluators = [completeness]

from phoenix.client import Client

dataset = Client().datasets.get_dataset(dataset="python quickstart fails")

from phoenix.experiments import run_experiment

experiment = run_experiment(dataset, my_task, evaluators)