#!/usr/bin/env python3
"""
Agno Unified Agent Project - Main Orchestrator
Interactive CLI for running and managing multiple AI agents
"""

import os
import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from dotenv import load_dotenv
import importlib # Added import for dynamic loading
import inspect # Added import for dynamic loading
from typing import Dict, Any # Keep existing import
from textwrap import dedent

from agno.agent import Agent
# from agno.app.fastapi import FastAPIApp
from fastapi import FastAPI
from agno.memory.v2 import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.exa import ExaTools
from agno.tools.yfinance import YFinanceTools

# Load environment variables
load_dotenv()

# Removed hardcoded agent imports
# from agents.finance_agent.agent import finance_agent
# from agents.youtube_agent.agent import youtube_agent
# from agents.research_agent.agent import research_agent
# from agents.movie_recommender.agent import movie_agent
# from agents.books_recommender.agent import book_agent
# from agents.travel_agent.agent import travel_agent

from utils.logging_config import setup_logging
from config.settings import Settings


# Initialize console and logging
console = Console()
logger = setup_logging()

agent_storage_file = "tmp/agents.db"
memory_storage_file = "tmp/memory.db"

memory_db = SqliteMemoryDb(table_name="memory", db_file=memory_storage_file)
memory = Memory(db=memory_db)

simple_agent = Agent(
    name="Simple Agent",
    role="Answer basic questions",
    agent_id="simple-agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    storage=SqliteStorage(
        table_name="simple_agent", db_file=agent_storage_file, auto_upgrade_schema=True
    ),
    memory=memory,
    enable_user_memories=True,
    add_history_to_messages=True,
    num_history_responses=5,
    add_datetime_to_instructions=True,
    markdown=True,
)

web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    agent_id="web-agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Break down the users request into 2-3 different searches.",
        "Always include sources",
    ],
    storage=SqliteStorage(
        table_name="web_agent", db_file=agent_storage_file, auto_upgrade_schema=True
    ),
    memory=memory,
    enable_user_memories=True,
    add_history_to_messages=True,
    num_history_responses=5,
    add_datetime_to_instructions=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    agent_id="finance-agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        )
    ],
    instructions=["Always use tables to display data"],
    storage=SqliteStorage(
        table_name="finance_agent", db_file=agent_storage_file, auto_upgrade_schema=True
    ),
    memory=memory,
    enable_user_memories=True,
    add_history_to_messages=True,
    num_history_responses=5,
    add_datetime_to_instructions=True,
    markdown=True,
)

research_agent = Agent(
    name="Research Agent",
    role="Research agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions=["You are a research agent"],
    tools=[DuckDuckGoTools(), ExaTools()],
    agent_id="research_agent",
    memory=memory,
    storage=SqliteStorage(
        table_name="research_agent",
        db_file=agent_storage_file,
        auto_upgrade_schema=True,
    ),
    enable_user_memories=True,
)

research_team = Team(
    name="Research Team",
    description="A team of agents that research the web",
    members=[research_agent, simple_agent],
    model=OpenAIChat(id="gpt-4o"),
    mode="coordinate",
    team_id="research-team",
    success_criteria=dedent("""
        A comprehensive research report with clear sections and data-driven insights.
    """),
    instructions=[
        "You are the lead researcher of a research team! 🔍",
    ],
    memory=memory,
    enable_user_memories=True,
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
    enable_agentic_context=True,
    storage=SqliteStorage(
        table_name="research_team",
        db_file=agent_storage_file,
        auto_upgrade_schema=True,
        mode="team",
    ),
)

from agents.agent_with_instructions.agent import agent as agent_with_instructions
from agents.youtube_agent.agent import youtube_agent
from agents.translation_agent.agent import agent as translation_agent
from agents.travel_agent.agent import travel_agent
from agents.thinking_finance_agent.agent import finance_agent as thinking_finance_agent
from agents.social_media_agent.agent import social_media_agent
from agents.study_partner.agent import study_partner
from agents.recipe_rag_image.agent import agent as recipe_rag_image_agent
from agents.research_agent.agent import research_agent
from agents.web_extraction_agent.agent import agent as web_extraction_agent

fastapi_app = FastAPI(
    agents=[
        simple_agent,
        web_agent,
        finance_agent,
        agent_with_instructions,
        youtube_agent,
        translation_agent,
        travel_agent,
        thinking_finance_agent,
        social_media_agent,
        study_partner,
        recipe_rag_image_agent,
        research_agent,
        web_extraction_agent,
    ],
    teams=[research_team],
    app_id="advanced-app",
    name="Advanced FastAPI App",
    description="A FastAPI app for advanced agents",
    version="0.0.1",
)
app = fastapi_app.get_app()


class AgentOrchestrator:
    """Orchestrates multiple Agno agents"""

    def __init__(self):
        self.settings = Settings()
        self.agents = {}
        self.initialize_agents()

    def initialize_agents(self):
        """Initialize all available agents by dynamically loading them"""
        agents_root_dir = os.path.join(os.path.dirname(__file__), 'agents')
        if not os.path.isdir(agents_root_dir):
            logger.error(f"Agents root directory not found: {agents_root_dir}")
            return

        # Add the project root to sys.path if not already there
        project_root = os.path.dirname(__file__) # Assuming main.py is at project root
        if project_root not in sys.path:
             sys.path.insert(0, project_root)

        # Emoji mapping for known agents (can be extended)
        emoji_map = {
            'finance_agent': '💰',
            'youtube_agent': '🎥',
            'research_agent': '🔬',
            'movie_recommendation': '🎬',
            'books_recommendation': '📚',
            'travel_agent': '🌍',
            'agent_team': '👥',
            'agent_with_instructions': '📝',
            'agent_with_knowledge': '🧠',
            'agent_with_memory': '💾',
            'agent_with_reasoning': '🤔',
            'agent_with_storage': '📦',
            'agent_with_tools': '🔧',
            'agno_assist': '✨',
            'agno_support_agent': '🤝',
            'airbnb_mcp': '🏠',
            'basic_agent': '👤',
            'competitor_analysis': '📊',
            'deep_knowledge': '📚',
            'deep_research_agent_exa': '🔍',
            'finance_agent_with_memory': '💾💰',
            'legal_consultant': '⚖️',
            'media_trend_analysis_agent': '📈',
            'meeting_summarizer_agent': '📝',
            'my_first_agents': '👶', # This folder contains subfolders, the key will be the subfolder name (level1, level2, etc.)
            'readme_generator': '📄',
            'reasoning_finance_agent': '🤔💰',
            'recipe_creator': '🍳',
            'recipe_rag_image': '🖼️🍳',
            'shopping_partner': '🛍️',
            'social_media_agent': '📱',
            'study_partner': '📖',
            'thinking_finance_agent': '🧠💰',
            'translation_agent': '🗣️',
            'web_extraction_agent': '🕸️',
            # Add emojis for nested agents if needed, e.g.,
            'level1': '1️⃣',
            'level2': '2️⃣',
            'level3': '3️⃣',
        }


        # Walk through the agents directory to find agent.py files
        for root, dirs, files in os.walk(agents_root_dir):
            if 'agent.py' in files and '__init__.py' in files:
                # Construct the module path
                # root will be something like c:\Users\NITRO\Documents\AI\Projects\Test1Agno\Test1Agno\agents\finance_agent
                # We need the path relative to the project root, then convert to module path
                relative_root = os.path.relpath(root, project_root) # e.g., agents\finance_agent
                module_path_parts = relative_root.split(os.sep) # e.g., ['agents', 'finance_agent']
                module_path = ".".join(module_path_parts) + ".agent" # e.g., agents.finance_agent.agent

                # Use the last part of the relative path as the agent key
                agent_key = module_path_parts[-1] # e.g., finance_agent

                try:
                    module = importlib.import_module(module_path)
                    logger.info(f"Attempting to load agent from module: {module_path}")

                    found_agent = None
                    agent_name = agent_key.replace('_', ' ').title() # Default name from folder
                    agent_description = "No description available" # Default description
                    emoji = emoji_map.get(agent_key, '❓') # Get emoji from map

                    # Find an Agent instance within the module
                    for name, obj in inspect.getmembers(module):
                        if isinstance(obj, Agent):
                            found_agent = obj
                            # Try to get name and description from the agent instance
                            if hasattr(obj, 'name') and obj.name:
                                 agent_name = obj.name
                            if hasattr(obj, 'description') and obj.description:
                                 agent_description = obj.description
                            # Found an agent instance, stop searching in this module
                            break

                    if found_agent:
                        # Handle potential key conflicts if multiple agent.py files are in folders with the same name
                        if agent_key in self.agents:
                             logger.warning(f"Duplicate agent key found: {agent_key}. Skipping module {module_path}")
                             console.print(f"[yellow]Warning: Skipping duplicate agent ID: {agent_key}[/yellow]")
                             continue

                        self.agents[agent_key] = {
                            'config': {
                                'name': agent_name,
                                'description': agent_description,
                                'emoji': emoji
                            },
                            'instance': found_agent # Store the instance directly
                        }
                        logger.info(f"Registered agent: {agent_name} (ID: {agent_key}) from {module_path}")
                    else:
                        logger.warning(f"No Agno Agent instance found in {module_path}")
                        console.print(f"[yellow]Warning: No Agno Agent found in {module_path}[/yellow]")

                except Exception as e:
                    logger.error(f"Failed to import or process agent module {module_path}: {e}")
                    console.print(f"[red]Warning: Could not load agent from {module_path}: {e}[/red]")

    def get_agent_instance(self, agent_key: str):
        """Get agent instance (already loaded during initialization)"""
        if agent_key not in self.agents:
            raise ValueError(f"Agent {agent_key} not found")

        # The instance is already loaded during initialization
        return self.agents[agent_key]['instance']

    def display_welcome(self):
        """Display welcome message and available agents"""
        console.print(Panel.fit(
            "[bold blue]🤖 Agno Unified Agent Project[/bold blue]\n"
            "[dim]Interactive AI Agent Orchestrator[/dim]",
            border_style="blue"
        ))

        # Create agents table
        table = Table(title="Available Agents", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="yellow")
        table.add_column("Description", style="green")
        # Removed Status column as all agents are loaded on startup now

        # Sort agents by key for consistent display
        sorted_agent_keys = sorted(self.agents.keys())

        for key in sorted_agent_keys:
            agent_info = self.agents[key]
            config = agent_info['config']
            table.add_row(
                f"{config['emoji']} {key}",
                config['name'],
                config['description']
            )

        console.print(table)
        console.print()

    def run_interactive_mode(self):
        """Run interactive mode for agent selection and queries"""
        self.display_welcome()

        while True:
            try:
                # Agent selection
                console.print("[bold]Available commands:[/bold]")
                # List available agent IDs dynamically
                agent_ids = ", ".join(sorted(self.agents.keys()))
                console.print(f"• Enter agent ID ({agent_ids})")
                console.print("• 'list' - Show available agents")
                console.print("• 'exit' - Quit the program")
                console.print()

                choice = Prompt.ask(
                    "[bold cyan]Select an agent or command[/bold cyan]",
                    default="list"
                ).lower().strip()

                if choice == 'exit':
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    break
                elif choice == 'list':
                    self.display_welcome()
                    continue
                elif choice in self.agents:
                    self.interact_with_agent(choice)
                else:
                    console.print(f"[red]Unknown agent or command: {choice}[/red]")

            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye! 👋[/yellow]")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                console.print(f"[red]Error: {e}[/red]")

    def interact_with_agent(self, agent_key: str):
        """Interact with a specific agent"""
        config = self.agents[agent_key]['config']
        console.print(f"\n[bold green]🚀 Activating {config['name']}[/bold green]")
        console.print(f"[dim]{config['description']}[/dim]\n")

        try:
            # Agent is already loaded during initialization
            agent = self.get_agent_instance(agent_key)

            console.print(f"[green]✅ {config['name']} is ready![/green]\n")

            # Agent interaction loop
            while True:
                console.print("[bold]Agent commands:[/bold]")
                console.print("• Enter your query")
                console.print("• 'back' - Return to main menu") # Removed 'examples'
                console.print()

                query = Prompt.ask(
                    f"[bold cyan]{config['emoji']} {config['name']}[/bold cyan]",
                    # Removed default="examples"
                )

                if query.lower() == 'back':
                    break
                # Removed elif query.lower() == 'examples':
                else:
                    self.process_agent_query(agent, query, config)

        except Exception as e:
            logger.error(f"Error interacting with agent {agent_key}: {e}")
            console.print(f"[red]Error interacting with agent: {e}[/red]") # Changed message slightly

    # Removed show_agent_examples method
    # def show_agent_examples(self, agent_key: str):
    #     """Show examples for a specific agent"""
    #     ...existing code...

    def process_agent_query(self, agent, query: str, config: Dict[str, Any]):
        """Process a query with the specified agent"""
        try:
            console.print(f"\n[bold blue]Processing with {config['name']}...[/bold blue]")

            # Run the agent query
            with console.status("[bold green]Thinking..."):
                # Assuming print_response returns the response object or string
                # If it prints directly and returns None, this needs adjustment
                # The original code had `response = agent.print_response(...)` which implies it returns something.
                response = agent.print_response(query, stream=False)

            console.print(f"\n[bold green]✅ Response from {config['name']}:[/bold green]")
            # Check if response is None or has a specific attribute to print
            if response is not None:
                 # Assuming the response object has a 'content' attribute or can be printed directly
                 # Based on previous examples, agent.print_response seems to handle printing directly when stream=True.
                 # When stream=False, it might return the final response object.
                 # Let's assume it returns a string or an object that prints nicely.
                 console.print(response)
            else:
                 # If print_response handles printing directly even with stream=False
                 pass # Nothing to print here, it was already printed by agent.print_response

            console.print("-" * 50)

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            console.print(f"[red]Error processing query: {e}[/red]")


@click.command()
@click.option('--agent', '-a', help='Run specific agent directly')
@click.option('--query', '-q', help='Query to run with the agent')
@click.option('--config', '-c', help='Configuration file path')
def main(agent: str = None, query: str = None, config: str = None):
    """
    Agno Unified Agent Project - Main CLI

    Run multiple AI agents for different tasks including finance,
    research, content analysis, and creative writing.
    """

    # Validate environment
    required_env_vars = ['OPENAI_API_KEY']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]

    if missing_vars:
        console.print(f"[red]Missing required environment variables: {', '.join(missing_vars)}[/red]")
        console.print("[yellow]Please set them in your .env file or environment[/yellow]")
        sys.exit(1)

    try:
        orchestrator = AgentOrchestrator()

        if agent and query:
            # Direct execution mode
            if agent not in orchestrator.agents:
                console.print(f"[red]Unknown agent: {agent}[/red]")
                console.print(f"Available agents: {list(orchestrator.agents.keys())}")
                sys.exit(1)

            agent_instance = orchestrator.get_agent_instance(agent)
            config = orchestrator.agents[agent]['config']
            orchestrator.process_agent_query(agent_instance, query, config)
        else:
            # Interactive mode
            orchestrator.run_interactive_mode()

    except Exception as e:
        logger.error(f"Application error: {e}")
        console.print(f"[red]Application error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    """
    Now you can reach your agents/teams with the following URLs:
    - http://localhost:8001/runs?agent_id=simple-agent
    - http://localhost:8001/runs?agent_id=web-agent
    - http://localhost:8001/runs?agent_id=finance-agent
    - http://localhost:8001/runs?team_id=research-team
    """
    fastapi_app.serve(app="advanced:app", port=8001, reload=True)
