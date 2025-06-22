from textwrap import dedent
from typing import Dict, List, Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.firecrawl import FirecrawlTools
from pydantic import BaseModel, Field
from rich.pretty import pprint
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings

# Verify the env variables
settings = Settings()
settings.validate()

class ContentSection(BaseModel):
    """Represents a section of content from the webpage."""
    heading: Optional[str] = Field(None, description="Section heading")
    content: str = Field(..., description="Section content text")

class PageInformation(BaseModel):
    """Structured representation of a webpage."""
    url: str = Field(..., description="URL of the page")
    title: str = Field(..., description="Title of the page")
    description: Optional[str] = Field(
        None, description="Meta description or summary of the page"
    )
    features: Optional[List[str]] = Field(None, description="Key feature list")
    content_sections: Optional[List[ContentSection]] = Field(
        None, description="Main content sections of the page"
    )
    links: Optional[Dict[str, str]] = Field(
        None, description="Important links found on the page with description"
    )
    contact_info: Optional[Dict[str, str]] = Field(
        None, description="Contact information if available"
    )
    metadata: Optional[Dict[str, str]] = Field(
        None, description="Important metadata from the page"
    )

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini", api_key=settings.openai_api_key),
    tools=[FirecrawlTools(scrape=True, crawl=True, api_key=settings.fire_crawl_api_key)],
    instructions=dedent("""
        You are a web content summarizer. Extract the main title, a short description, and the most important sections from the provided webpage.
        List any key features, important links, and available contact information. Be concise and focus on the most relevant details.
    """).strip(),
    response_model=PageInformation,
)

result = agent.run("Extract all information from https://www.agno.com")
pprint(result.content)