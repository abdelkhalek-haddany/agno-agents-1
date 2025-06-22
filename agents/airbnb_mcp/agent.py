"""🏠 MCP Airbnb Agent - Search for Airbnb listings!

This example shows how to create an agent that uses MCP and Llama 4 to search for Airbnb listings.

1. Run: `pip install groq mcp agno` to install the dependencies
2. Export your GROQ_API_KEY
3. Run: `python cookbook/examples/agents/airbnb_mcp.py` to run the agent
"""

import asyncio
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools
from agno.tools.thinking import ThinkingTools
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings


# Verify the env variables
settings = Settings()
settings.validate()

async def run_agent(message: str) -> None:
    async with MCPTools(
        "npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt"
    ) as mcp_tools:
        agent = Agent(
            model=OpenAIChat(id="gpt-4o-mini", api_key=settings.openai_api_key),
            tools=[ThinkingTools(), mcp_tools],
            instructions=dedent("""\
                ## Instructions
                - Use the think tool to plan and validate each step.
                - Present the top 5 Airbnb listings in a markdown table with price, location, and link.
                - Highlight any special amenities or features.
                - Only output the table and a brief summary, no extra commentary.
            """),
            add_datetime_to_instructions=True,
            show_tool_calls=True,
            markdown=True,
        )
        await agent.aprint_response(message, stream=True, markdown=True)


if __name__ == "__main__":
    task = dedent("""\
        I'm traveling to San Francisco from April 20th - May 8th. Can you find me the best deals for a 1 bedroom apartment?
        I'd like a dedicated workspace and close proximity to public transport.\
    """)
    asyncio.run(run_agent(task))