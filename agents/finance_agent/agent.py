from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings


#Verify the env variables
settings = Settings()
settings.validate()


finance_agent = Agent(
    model=OpenAIChat(id="gpt-4o", api_key=settings.openai_api_key),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            historical_prices=True,
            company_info=True,
            company_news=True,
        )
    ],
    instructions=dedent("""\
        You are a veteran financial analyst specializing in equity markets 📈💼

        When conducting your analysis, proceed as follows:

        1) Stock Snapshot:
           - Current price and recent movement
           - Annual high and low range
        2) Financial Metrics Review:
           - Key ratios such as P/E, Market Capitalization, EPS
        3) Expert Commentary:
           - Summary of analyst ratings and upgrades/downgrades
        4) Sector & Market Overview:
           - Industry trends affecting the company
           - Competitive landscape and peer comparison
           - Investor sentiment indicators

        Style Guidelines:
        - Start with a brief summary for executives
        - Present data in clear tables
        - Use headers to structure your output
        - Incorporate trend emojis like 📊⬆️⬇️
        - Highlight critical insights using bullet points
        - Compare figures against sector averages
        - Explain jargon or technical terms for clarity
        - Conclude with strategic outlook and risk factors

        Always emphasize possible risks, market volatility, and relevant regulations.
    """),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
)

finance_agent.print_response(
    "Provide a detailed financial and market overview of Microsoft (MSFT), focusing on recent earnings and analyst sentiment.",
    stream=True,
)

finance_agent.print_response(
    dedent("""\
    Assess the cloud computing sector with emphasis on:
    - Amazon (AMZN)
    - Alphabet (GOOGL)
    - Salesforce (CRM)
    Compare growth potential and competitive positioning."""),
    stream=True,
)

finance_agent.print_response(
    dedent("""\
    Analyze the electric vehicle market status:
    - Rivian (RIVN)
    - Lucid Motors (LCID)
    - Ford (F)
    Include progress in EV adoption and financial health."""),
    stream=True,
)

# Additional example queries (for your test or documentation)
"""
Advanced inquiries:
1. "Contrast the P/E ratios of Facebook and Snap Inc."
2. "Discuss the effects of supply chain issues on Tesla's production costs."
3. "How does Nvidia's R&D spending influence its stock valuation?"
4. "Evaluate Netflix’s subscriber trends and revenue forecasts."
5. "Break down Google's revenue by business segment."

Sector focus:
Cloud Computing:
1. "What is the impact of AWS growth on Amazon's stock?"
2. "Analyze Google Cloud's competitive advantages."
3. "Review Microsoft Azure's market share evolution."

Electric Vehicles:
1. "Compare profitability margins across EV makers."
2. "Discuss challenges traditional automakers face transitioning to EVs."
3. "Examine how rising interest rates affect EV financing."
4. "Evaluate Tesla's innovation pipeline versus competitors."
"""
