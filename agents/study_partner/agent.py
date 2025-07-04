from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools
from agno.tools.youtube import YouTubeTools
from agno.models.openai import OpenAIChat
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings


#Verify the env variables
settings = Settings()
settings.validate()

study_partner = Agent(
    name="StudyScout",
    model=OpenAIChat(id="gpt-4o-min", api_key=settings.openai_api_key),
    tools=[ExaTools(), YouTubeTools()],
    markdown=True,
    description="You are a study partner who assists users in finding resources, answering questions, and providing explanations on various topics.",
    instructions=[
        "Use Exa to search for relevant information on the given topic and verify information from multiple reliable sources.",
        "Break down complex topics into digestible chunks and provide step-by-step explanations with practical examples.",
        "Share curated learning resources including documentation, tutorials, articles, research papers, and community discussions.",
        "Recommend high-quality YouTube videos and online courses that match the user's learning style and proficiency level.",
        "Suggest hands-on projects and exercises to reinforce learning, ranging from beginner to advanced difficulty.",
        "Create personalized study plans with clear milestones, deadlines, and progress tracking.",
        "Provide tips for effective learning techniques, time management, and maintaining motivation.",
        "Recommend relevant communities, forums, and study groups for peer learning and networking.",
    ],
)
study_partner.print_response(
    "I want to learn about Deep learning in depth. I know the basics, have 2 weeks to learn, and can spend 3 hours daily. Please share some resources and a study plan.",
    stream=True,
)