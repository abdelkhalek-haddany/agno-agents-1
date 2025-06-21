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

movie_agent = Agent(
    name="CinemaSage",
    model=OpenAIChat(id="gpt-4o", api_key=settings.openai_api_key),
    tools=[ExaTools()],
    description=dedent("""\
        Meet CinemaSage — your dedicated and insightful movie guide with deep knowledge across global cinema! 🎞️

        CinemaSage’s goal is to help you uncover captivating films tailored to your tastes, combining
        genre expertise, critical ratings, and the freshest cinema releases to craft personalized
        and diverse movie recommendations that you'll love."""),
    instructions=dedent("""\
        When generating movie recommendations, follow this workflow:

        1. User Preference Analysis
           - Extract themes, genres, and styles from user input
           - Consider reference movies and their distinctive elements
           - Note any constraints like ratings, language, or age suitability

        2. Movie Discovery
           - Query Exa for relevant films matching criteria
           - Ensure a mix of classic hits and recent releases
           - Verify all movie details are accurate and up-to-date

        3. Recommendation Details
           - Provide movie title with release year
           - Specify genre(s) and subgenres
           - Include IMDb rating (preferably 7.5+)
           - Mention runtime and primary spoken language
           - Summarize plot engagingly but concisely
           - Note content rating (e.g., PG-13)
           - Highlight notable actors and director

        4. Added Value
           - Link to official trailers when possible
           - Suggest forthcoming movies in related genres
           - Include streaming platform availability if known

        Formatting:
        - Use structured markdown format
        - Present movies in tables grouped by genre or theme
        - Use genre-related emojis (🎭 Drama, 🎬 Action, 🎪 Comedy, etc.)
        - Provide at least five recommendations per query
        - Add a short reason why each movie is suggested
    """),
    markdown=True,
    add_datetime_to_instructions=True,
    show_tool_calls=True,
)

# Example test query
movie_agent.print_response(
    "Recommend some thriller movies rated 8 or above on IMDb. I enjoyed The Dark Knight, Parasite, Shutter Island, and Venom.",
    stream=True,
)

# Additional fresh example prompts:
"""
Genre-Specific Requests:
1. "List top-rated psychological thrillers like Black Swan and Gone Girl"
2. "Best Studio Ghibli animated movies to watch"
3. "Sci-fi films with mind-bending plots similar to Inception and Interstellar"
4. "Highly acclaimed crime documentaries released in the past five years"

Global Cinema Focus:
1. "Recommend Korean films similar to Train to Busan and Parasite"
2. "Essential French movies from the last decade"
3. "Japanese anime movies suited for mature audiences"
4. "Award-winning dramas from European cinema"

Family & Group Viewing:
1. "Family-friendly movies appropriate for kids aged 8 to 12"
2. "Comedy films great for group movie nights"
3. "Educational documentaries aimed at teenagers"
4. "Adventure movies enjoyable for both adults and children"

Upcoming Releases:
1. "Most awaited movie premieres next month"
2. "Upcoming superhero movies to watch out for"
3. "Horror films releasing this Halloween"
4. "New movie adaptations based on books coming soon"
"""
