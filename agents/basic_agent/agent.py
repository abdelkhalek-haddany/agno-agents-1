from agno.agent import Agent
from agno.models.openai import OpenAIChat
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings


#Verify the env variables
settings = Settings()
settings.validate()
agent = Agent(model=OpenAIChat(id="gpt-4o-mini", api_key=settings.openai_api_key), markdown=True)
agent.print_response("What's the problems that morocco is facing as a country?", stream=True)