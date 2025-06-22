"""🐍 Python Code Assistant - Your Interactive Python Helper!

This example shows how to create an AI assistant that helps users write, explain, and debug Python code interactively.

Key Features:
- Step-by-step code explanations
- Code generation and refactoring
- Error diagnosis and debugging
- Interactive session management

Example prompts to try:
- "How do I write a function to reverse a string in Python?"
- "Explain how list comprehensions work."
- "Why am I getting a TypeError in my code?"
- "Refactor this code for better readability."
- "Show me how to use classes in Python."

Run `pip install openai agno inquirer typer rich` to install dependencies.
"""

from pathlib import Path
from textwrap import dedent
from typing import List, Optional

import inquirer
import typer
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.python import PythonTools
from agno.storage.agent.sqlite import SqliteAgentStorage
from rich import print
from rich.console import Console
from rich.table import Table
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings

# Verify the env variables
settings = Settings()
settings.validate()

# Setup Paths
cwd = Path(__file__).parent
tmp_dir = cwd.joinpath("tmp")
tmp_dir.mkdir(parents=True, exist_ok=True)

def get_agent_storage():
    """Return agent storage for session management"""
    return SqliteAgentStorage(
        table_name="python_assist_sessions", db_file="tmp/agents.db"
    )

def create_agent(session_id: Optional[str] = None) -> Agent:
    """Create and return a configured Python Code Assistant agent."""
    agent_storage = get_agent_storage()

    return Agent(
        name="PythonCodeAssist",
        session_id=session_id,
        model=OpenAIChat(id="gpt-4o-mini", api_key=settings.openai_api_key),
        description=dedent("""\
        You are PythonCodeAssist, an advanced AI Agent specialized in Python programming.
        Your goal is to help users write, understand, and debug Python code interactively.
        You can generate, explain, refactor, and troubleshoot code, providing step-by-step guidance.
        """),
        instructions=dedent("""\
        Your mission is to provide comprehensive, hands-on support for Python developers.

        For every query:
        1. Analyze the user's question or code.
        2. If code is provided, explain what it does and identify any issues.
        3. If the user asks for code, generate a complete, runnable example.
        4. Offer suggestions for improvement, refactoring, or debugging.
        5. Use the PythonTools to execute code snippets and show results.
        6. Always provide clear explanations and best practices.
        7. Use markdown formatting for code and output.
        """),
        tools=[PythonTools(base_dir=tmp_dir.joinpath("python_assist"), read_files=True)],
        storage=agent_storage,
        add_history_to_messages=True,
        num_history_responses=3,
        show_tool_calls=True,
        read_chat_history=True,
        markdown=True,
    )

def get_example_topics() -> List[str]:
    """Return a list of example topics for the agent."""
    return [
        "How do I write a function to reverse a string in Python?",
        "Explain how list comprehensions work.",
        "Why am I getting a TypeError in my code?",
        "Refactor this code for better readability.",
        "Show me how to use classes in Python.",
    ]

def handle_session_selection() -> Optional[str]:
    """Handle session selection and return the selected session ID."""
    agent_storage = get_agent_storage()

    new = typer.confirm("Do you want to start a new session?", default=True)
    if new:
        return None

    existing_sessions: List[str] = agent_storage.get_all_session_ids()
    if not existing_sessions:
        print("No existing sessions found. Starting a new session.")
        return None

    print("\nExisting sessions:")
    for i, session in enumerate(existing_sessions, 1):
        print(f"{i}. {session}")

    session_idx = typer.prompt(
        "Choose a session number to continue (or press Enter for most recent)",
        default=1,
    )

    try:
        return existing_sessions[int(session_idx) - 1]
    except (ValueError, IndexError):
        return existing_sessions[0]

def run_interactive_loop(agent: Agent, show_topics: bool = True):
    """Run the interactive question-answering loop.

    Args:
        agent: Agent instance to use for responses
        show_topics: Whether to show example topics or continue chat-like interaction
    """
    example_topics = get_example_topics()
    first_interaction = True

    while True:
        if show_topics and first_interaction:
            choices = [f"{i + 1}. {topic}" for i, topic in enumerate(example_topics)]
            choices.extend(["Enter custom question...", "Exit"])

            questions = [
                inquirer.List(
                    "topic",
                    message="Select a topic or ask a different question:",
                    choices=choices,
                )
            ]
            answer = inquirer.prompt(questions)

            if answer is None or answer["topic"] == "Exit":
                break

            if answer["topic"] == "Enter custom question...":
                questions = [inquirer.Text("custom", message="Enter your question:")]
                custom_answer = inquirer.prompt(questions)
                topic = custom_answer["custom"]
            else:
                topic = example_topics[int(answer["topic"].split(".")[0]) - 1]
            first_interaction = False
        else:
            # Chat-like interaction
            question = typer.prompt("\n", prompt_suffix="> ")
            if question.lower() in ("exit", "quit", "bye"):
                break
            topic = question

        agent.print_response(topic, stream=True)

def python_code_assistant():
    """Main function to run the Python Code Assistant agent."""
    session_id = handle_session_selection()
    agent = create_agent(session_id)

    # Create and display welcome table
    console = Console()
    table = Table(show_header=False, style="cyan")
    table.add_column(justify="center", min_width=40)
    table.add_row("🐍 Welcome to [bold green]PythonCodeAssist[/bold green]")
    table.add_row("Your Interactive Python Helper")
    console.print(table)

    if session_id is None:
        session_id = agent.session_id
        if session_id is not None:
            print(
                "[bold green]📝 Started New Session: [white]{}[/white][/bold green]\n".format(
                    session_id
                )
            )
        else:
            print("[bold green]📝 Started New Session[/bold green]\n")
        show_topics = True
    else:
        print(
            "[bold blue]🔄 Continuing Previous Session: [white]{}[/white][/bold blue]\n".format(
                session_id
            )
        )
        show_topics = False

    run_interactive_loop(agent, show_topics)

if __name__ == "__main__":
    typer.run(python_code_assistant)