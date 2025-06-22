from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from agno.models.openai import OpenAIChat
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings


# Verify the env variables
settings = Settings()
settings.validate()

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini", api_key=settings.openai_api_key),
    tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        ),
    ],
    instructions=[
        "Use tables to display data.",
        "Include sources in your response.",
        "Only include the analysis in your response. No other text.",
    ],
    markdown=True,
)
agent.print_response(
    "Analyze Apple Inc. (AAPL) as an investment opportunity.",
    stream=True,
    show_full_reasoning=True,
    stream_intermediate_steps=True,
)