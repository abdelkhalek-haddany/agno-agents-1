from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings


# Verify the env variables
settings = Settings()
settings.validate()

api_key = settings.openai_api_key

# Agents for travel planning
destination_agent = Agent(
    name="Destination Finder",
    role="Find top travel destinations based on user preferences",
    model=OpenAIChat(id="gpt-4o-mini", api_key=api_key),
    tools=[DuckDuckGoTools()],
    instructions="Provide a list of destinations with brief descriptions and sources.",
    add_datetime_to_instructions=True,
)

itinerary_agent = Agent(
    name="Itinerary Planner",
    role="Create detailed travel itineraries",
    model=OpenAIChat(id="gpt-4o-mini", api_key=api_key),
    tools=[ReasoningTools(add_instructions=True)],
    instructions="Suggest a 3-day itinerary with activities and estimated costs.",
    add_datetime_to_instructions=True,
)

travel_team = Team(
    name="Travel Planning Team",
    mode="coordinate",
    model=OpenAIChat(id="gpt-4o-mini", api_key=api_key),
    members=[destination_agent, itinerary_agent],
    tools=[ReasoningTools(add_instructions=True)],
    instructions=[
        "Provide clear, actionable travel advice.",
        "Only respond with the final answer, no other text.",
    ],
    markdown=True,
    show_members_responses=True,
    enable_agentic_context=True,
    add_datetime_to_instructions=True,
    success_criteria="The team has successfully created a travel plan.",
)

task = """\
Plan a 3-day trip to Japan for a family with two kids. Suggest the best destinations, daily activities, and estimated costs."""

# Agent instructions
travel_team.print_response(
    task,
    stream=True,
    stream_intermediate_steps=True,
    show_full_reasoning=True,
)