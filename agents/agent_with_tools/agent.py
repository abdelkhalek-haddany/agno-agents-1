from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.yfinance import YFinanceTools
from agno.models.openai import OpenAIChat
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings


#Verify the env variables
settings = Settings()
settings.validate()
    
agent = Agent(
    model=OpenAIChat(id="gpt-4o", api_key=settings.openai_api_key),
    tools=[YFinanceTools(stock_price=True)],
    markdown=True,
)
agent.print_response("What is the population of Morocco?", stream=True)