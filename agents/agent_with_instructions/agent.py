from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

from config.settings import Settings

# Verify the env variables
settings = Settings()
settings.validate()

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini", api_key=settings.openai_api_key),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Answer programming questions using up-to-date web search results.",
        "Only output the answer in a markdown code block, no other text.",
    ],
    markdown=True,
)

agent.print_response("How do I reverse a list in Python?", stream=True)