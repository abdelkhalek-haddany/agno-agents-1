from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.github import GithubTools
from agno.tools.local_file_system import LocalFileSystemTools
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings

# Verify the env variables
settings = Settings()
settings.validate()

project_summary_agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini", api_key=settings.openai_api_key),
    name="Project Summary Agent",
    tools=[GithubTools(), LocalFileSystemTools()],
    markdown=True,
    debug_mode=True,
    instructions=[
        "You are a project summary agent.",
        "You will be given a GitHub repository URL or name.",
        "Use the `get_repository` tool to fetch repository details.",
        "Summarize the repository's purpose, main features, and usage in a concise markdown file.",
        "Write the summary to the local filesystem as PROJECT_SUMMARY.md.",
        "Do not include language statistics or badges.",
    ],
)

project_summary_agent.print_response(
    "Summarize https://github.com/agno-agi/agno and save as PROJECT_SUMMARY.md", markdown=True
)