from textwrap import dedent

from agno.agent import Agent
from agno.tools.youtube import YouTubeTools
import os

from agno.models.openai import OpenAIChat
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings


#Verify the env variables
settings = Settings()
settings.validate()


youtube_agent = Agent(
    name="YouTube Video Content Analyst",
    model=OpenAIChat(id="gpt-4o", api_key=settings.openai_api_key),
    tools=[YouTubeTools()],
    show_tool_calls=True,
    instructions=dedent("""\
        You are a seasoned YouTube content expert specializing in in-depth video analysis 🎥🔍

        Approach each video with this workflow:

        1) General Overview
           - Summarize video length and key metadata
           - Categorize the video format (tutorial, review, lecture, vlog, etc.)
           - Outline the overall content flow

        2) Timestamp Generation
           - Craft accurate, informative timestamps
           - Emphasize significant topic shifts and highlights
           - Format timestamps as [start_time - end_time]: detailed summary

        3) Content Structuring
           - Cluster related topics and segments
           - Identify primary themes and subtopics
           - Map how topics evolve throughout the video

        Analysis Style Guidelines:
        - Start with a concise summary of the video
        - Use descriptive and engaging segment titles
        - Add fitting emojis based on content type:
          📘 Learning
          🖥️ Tech & Software
          🎲 Gaming
          📦 Product Reviews
          🎨 Arts & Crafts
        - Highlight educational takeaways and practical demos
        - Mark important citations or references

        Accuracy & Quality:
        - Ensure timestamps reflect real video content precisely
        - Avoid fabricating sections or timestamps
        - Maintain thorough and even detail coverage
        - Focus on segments that add real value for viewers
    """),
    add_datetime_to_instructions=True,
    markdown=True,
)

# Example queries for testing and demo

youtube_agent.print_response(
    "Perform a detailed breakdown of this tutorial video: https://www.youtube.com/watch?v=nLkBNnnA8Ac",
    stream=True,
)

youtube_agent.print_response(
    dedent("""\
    Provide a structured timestamp overview for this tech product review:
    - Focus on feature demonstrations and pros/cons
    - Summarize technical specs and user impressions
    """),
    stream=True,
)

youtube_agent.print_response(
    dedent("""\
    Analyze this creative arts video:
    - Outline major project steps
    - Highlight key techniques and materials used
    - Include practical tips and tricks timestamps
    """),
    stream=True,
)

# Additional example prompts for exploration
"""
Tutorials:
1. "Summarize key code examples with timestamps from this Python lesson"
2. "Outline the learning modules in this web design series"
3. "Extract hands-on exercises from this programming walkthrough"
4. "Highlight main concepts and demos in this software tutorial"

Educational Videos:
1. "Create a timestamped study guide for this physics lecture"
2. "Identify major theories and examples in this biology talk"
3. "Break down this documentary into chronological events"
4. "Summarize the key arguments from this academic presentation"

Tech Reviews:
1. "List product features with timestamps from this smartphone review"
2. "Compare pros and cons mentioned in this gadget overview"
3. "Extract benchmark results and specifications"
4. "Highlight comparison points and final verdicts"

Creative & DIY:
1. "Detail techniques demonstrated in this painting tutorial"
2. "Outline project stages in this home improvement video"
3. "List tools and materials mentioned with timestamps"
4. "Extract useful tips with their demonstrations"
"""
