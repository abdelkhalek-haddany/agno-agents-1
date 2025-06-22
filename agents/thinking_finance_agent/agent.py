"""🗞️ Finance Agent - Your Personal Market Analyst!

This example shows how to create a sophisticated financial analyst that provides
comprehensive market insights using real-time data. The agent combines stock market data,
analyst recommendations, company information, and latest news to deliver professional-grade
financial analysis.

Example prompts to try:
- "What's the latest news and financial performance of Apple (AAPL)?"
- "Give me a detailed analysis of Tesla's (TSLA) current market position"
- "How are Microsoft's (MSFT) financials looking? Include analyst recommendations"
- "Analyze NVIDIA's (NVDA) stock performance and future outlook"
- "What's the market saying about Amazon's (AMZN) latest quarter?"

Run: `pip install openai yfinance agno` to install the dependencies
"""

from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings


# Verify the env variables
settings = Settings()
settings.validate()

finance_agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini", api_key=settings.openai_api_key),
    tools=[ReasoningTools(add_instructions=True), YFinanceTools(enable_all=True)],
    instructions=dedent("""\
        You are a financial summary agent. For any stock or company:
        - Provide a concise executive summary.
        - Show the latest stock price, 52-week range, and key financial metrics in a table.
        - List analyst recommendations and recent news headlines.
        - Highlight major risks and uncertainties.
        - Use markdown formatting and bullet points for clarity.
        - Only output the summary, no extra commentary.
    """),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
    stream_intermediate_steps=True,
)

# Example usage
finance_agent.print_response(
    "Summarize the financials and risks for Microsoft (MSFT).", stream=True
)

finance_agent.print_response(
    dedent("""\
    Compare the latest financial performance and analyst sentiment for:
    - Apple (AAPL)
    - Google (GOOGL)
    - Amazon (AMZN)
    """),
    stream=True,
)