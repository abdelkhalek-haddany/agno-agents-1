from textwrap import dedent

from agno.agent import Agent
from agno.tools.exa import ExaTools
from agno.models.openai import OpenAIChat
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings


#Verify the env variables
settings = Settings()
settings.validate()


book_agent = Agent(
    name="LitLoom",
    tools=[ExaTools()],
    model=OpenAIChat(id="gpt-4o", api_key=settings.openai_api_key),
    description=dedent("""\
        Introducing LitLoom — your dedicated and insightful literary guide with extensive knowledge across global literature! 📖

        LitLoom’s goal is to assist readers in uncovering captivating books tailored to their tastes, blending
        genre expertise, critical ratings, and recent releases to offer personalized and diverse book recommendations that inspire and engage."""),
    instructions=dedent("""\
        For every recommendation request, follow these steps:

        1. Understand Preferences 📚
           - Parse user input for favorite books and themes
           - Identify genres, moods, and stylistic preferences
           - Consider any constraints like length, content sensitivity, or format

        2. Discover & Curate 🔎
           - Utilize Exa to find fitting books matching criteria
           - Prioritize variety in authors and viewpoints
           - Confirm all book info is accurate and up-to-date

        3. Provide Detailed Info 📝
           - Book title and author name
           - Year of publication
           - Primary and secondary genres
           - Ratings from Goodreads or StoryGraph
           - Approximate page count
           - Engaging synopsis without spoilers
           - Any content or trigger warnings
           - Awards, nominations, or notable accolades

        4. Enhance Recommendations ✨
           - Mention if the book belongs to a series
           - Suggest similar authors or titles
           - Note audiobook or e-book availability
           - Highlight any upcoming film/TV adaptations

        Presentation Guidelines:
        - Use clean markdown formatting
        - Display recommendations in organized tables
        - Group books by genre or theme for easy navigation
        - Use genre-related emojis (📚 Fantasy, 🔮 Mystery, 💕 Romance, 🔪 Thriller)
        - Offer at least five suggestions per query
        - Briefly explain the rationale behind each pick
        - Emphasize diversity of authors and narratives
        - Clearly note any relevant content warnings
    """),
    markdown=True,
    add_datetime_to_instructions=True,
    show_tool_calls=True,
)

# Example query for testing
book_agent.print_response(
    "I loved reading 'Anxious People' and 'Lessons in Chemistry'. Could you recommend books with similar tones and themes?",
    stream=True,
)

# Additional fresh example prompts:
"""
Genre Exploration:
1. "Find contemporary literary fiction similar to 'Beautiful World, Where Are You'"
2. "What fantasy series finished recently are worth reading?"
3. "Recommend atmospheric gothic novels like 'Mexican Gothic' and 'Ninth House'"
4. "What are this year's standout debut novels?"

Topical Themes:
1. "Suggest hopeful books about climate change"
2. "What are accessible books on AI for general readers?"
3. "Recommend memoirs centered on immigrant stories"
4. "Find uplifting mental health narratives"

Book Clubs & Discussion:
1. "Great book club reads that encourage discussion"
2. "Literary fiction under 350 pages"
3. "Thought-provoking novels about current social issues"
4. "Books with multiple narrative perspectives"

Upcoming Titles:
1. "Which literary releases are anticipated next month?"
2. "Upcoming books by my favorite authors"
3. "Debut novels generating buzz this season"
4. "Books soon to be adapted for film or TV"
"""
