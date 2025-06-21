#!/usr/bin/env python3
"""
Agno Unified Agent Project - Main Orchestrator
Interactive CLI for running and managing multiple AI agents
"""

import os
import sys
from typing import Dict, Any
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import all agents you have
from agents.finance_agent.agent import finance_agent
from agents.youtube_agent.agent import youtube_agent
from agents.research_agent.agent import research_agent
from agents.movie_recommender.agent import movie_agent
from agents.books_recommender.agent import book_agent
from agents.travel_agent.agent import travel_agent

from utils.logging_config import setup_logging
from config.settings import Settings

# Initialize console and logging
console = Console()
logger = setup_logging()


class AgentOrchestrator:
    """Orchestrates multiple Agno agents"""

    def __init__(self):
        self.settings = Settings()
        self.agents = {}
        self.initialize_agents()

    def initialize_agents(self):
        """Initialize all available agents"""
        agent_configs = {
            'finance': {
                'name': 'Enhanced Finance Agent',
                'description': 'Advanced financial analysis with ESG factors and crypto support',
                'creator': finance_agent,
                'emoji': '💰'
            },
            'youtube': {
                'name': 'Advanced YouTube Agent',
                'description': 'Intelligent video analysis with multi-language support',
                'creator': youtube_agent,
                'emoji': '🎥'
            },
            'research': {
                'name': 'Enhanced Research Agent',
                'description': 'Academic research with fact-checking and citation formatting',
                'creator': research_agent,
                'emoji': '🔬'
            },
            'movie': {
                'name': 'Movie Recommendation Agent',
                'description': 'Personalized cinema recommendations',
                'creator': movie_agent,
                'emoji': '🎬'
            },
            'book': {
                'name': 'Book Recommendation Agent',
                'description': 'Personalized book recommendations',
                'creator': book_agent,
                'emoji': '📚'
            },
            'travel': {
                'name': 'Travel Planning Agent',
                'description': 'Expert travel itineraries and logistics',
                'creator': travel_agent,
                'emoji': '🌍'
            }
        }

        for key, config in agent_configs.items():
            try:
                self.agents[key] = {
                    'config': config,
                    'instance': None  # Lazy loading
                }
                logger.info(f"Registered agent: {config['name']}")
            except Exception as e:
                logger.error(f"Failed to register agent {key}: {e}")
                console.print(f"[red]Warning: Could not register {config['name']}[/red]")

    def get_agent_instance(self, agent_key: str):
        """Get or create agent instance (lazy loading)"""
        if agent_key not in self.agents:
            raise ValueError(f"Agent {agent_key} not found")

        if self.agents[agent_key]['instance'] is None:
            try:
                creator = self.agents[agent_key]['config']['creator']
                self.agents[agent_key]['instance'] = creator()
                logger.info(f"Created instance for {agent_key}")
            except Exception as e:
                logger.error(f"Failed to create agent {agent_key}: {e}")
                raise

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
        table.add_column("Status", justify="center")

        for key, agent_info in self.agents.items():
            config = agent_info['config']
            status = "🟢 Ready" if agent_info['instance'] is None else "🔵 Loaded"
            table.add_row(
                f"{config['emoji']} {key}",
                config['name'],
                config['description'],
                status
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
                console.print("• Enter agent ID (finance, youtube, research, movie, book, travel)")
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
            # Load agent
            with console.status(f"[bold green]Loading {config['name']}..."):
                agent = self.get_agent_instance(agent_key)

            console.print(f"[green]✅ {config['name']} is ready![/green]\n")

            # Agent interaction loop
            while True:
                console.print("[bold]Agent commands:[/bold]")
                console.print("• Enter your query")
                console.print("• 'examples' - Show example queries")
                console.print("• 'back' - Return to main menu")
                console.print()

                query = Prompt.ask(
                    f"[bold cyan]{config['emoji']} {config['name']}[/bold cyan]",
                    default="examples"
                )

                if query.lower() == 'back':
                    break
                elif query.lower() == 'examples':
                    self.show_agent_examples(agent_key)
                else:
                    self.process_agent_query(agent, query, config)

        except Exception as e:
            logger.error(f"Error interacting with agent {agent_key}: {e}")
            console.print(f"[red]Error loading agent: {e}[/red]")

    def show_agent_examples(self, agent_key: str):
        """Show examples for a specific agent"""
        examples = {
            'finance': [
                "What's the latest news and financial performance of Tesla (TSLA)?",
                "Analyze Apple's ESG performance and sustainability metrics",
                "Compare Bitcoin and Ethereum market trends this week"
            ],
            'youtube': [
                "Analyze this tech tutorial: https://www.youtube.com/watch?v=example",
                "Extract key learning points from this educational video",
                "Create timestamps for this programming course"
            ],
            'research': [
                "Research the latest developments in quantum computing",
                "Find and analyze recent papers on climate change solutions",
                "Compare different approaches to renewable energy storage"
            ],
            'movie': [
                "Suggest thriller movies similar to Inception and Shutter Island",
                "What are the top-rated comedy movies from the last 2 years?",
                "Find me Korean movies similar to Parasite and Oldboy"
            ],
            'book': [
                "I really enjoyed 'Anxious People' and 'Lessons in Chemistry', can you suggest similar books?",
                "Recommend contemporary literary fiction like 'Beautiful World, Where Are You'",
                "Suggest books about mental health with hopeful endings"
            ],
            'travel': [
                "Plan a corporate retreat in Bali for 20 people",
                "Create a 5-day cultural itinerary in Rome",
                "Suggest budget travel options in Southeast Asia"
            ]
        }

        if agent_key in examples:
            console.print(f"[bold magenta]Example queries for {agent_key}:[/bold magenta]")
            for i, example in enumerate(examples[agent_key], 1):
                console.print(f"  {i}. {example}")
            console.print()

    def process_agent_query(self, agent, query: str, config: Dict[str, Any]):
        """Process a query with the specified agent"""
        try:
            console.print(f"\n[bold blue]Processing with {config['name']}...[/bold blue]")

            # Run the agent query
            with console.status("[bold green]Thinking..."):
                response = agent.print_response(query, stream=False)

            console.print(f"\n[bold green]✅ Response from {config['name']}:[/bold green]")
            console.print(response)
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
    main()
