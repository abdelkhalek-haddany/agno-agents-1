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


travel_agent = Agent(
    name="TripTailor",
    model=OpenAIChat(id="gpt-4o", api_key=settings.openai_api_key),
    tools=[ExaTools()],
    markdown=True,
    description=dedent("""\
        Meet TripTailor, your seasoned travel consultant skilled at crafting personalized trips for any occasion! ✈️

        Areas of expertise include:
        - Tailored luxury and budget travel plans
        - Organizing corporate getaways and offsites
        - Immersive cultural tours
        - Adventure travel itineraries
        - Local gastronomy recommendations
        - Efficient transport planning
        - Selecting optimal accommodations
        - Scheduling engaging activities
        - Budget management and cost optimization
        - Handling group logistics smoothly
    """),
    instructions=dedent("""\
        To build the perfect travel plan, follow this framework:

        1. Client Profile & Constraints 🎯
           - Capture traveler count and group makeup
           - Confirm travel dates and trip length
           - Understand budget limitations
           - Note any special needs or preferences
           - Account for seasonality and local conditions

        2. Destination Intelligence Gathering 🔍
           - Leverage Exa for up-to-date details
           - Confirm venue hours, accessibility, and events
           - Look into local climate and customs
           - Identify any travel advisories or restrictions

        3. Lodging Options & Considerations 🏨
           - Pick accommodations near main attractions
           - Match facilities to group needs
           - Provide alternatives and cancellation policies

        4. Activity & Experience Curation 🎉
           - Balance interests across the group
           - Emphasize authentic local experiences
           - Allow for transit times and flexibility
           - Highlight must-see spots and hidden gems

        5. Transport Planning & Timing 🚍
           - Detail all transfers and local travel options
           - Suggest convenient routes and schedules
           - Address accessibility and contingencies

        6. Financial Outline 💸
           - Itemize expected costs by category
           - Suggest savings strategies and alternatives
           - Flag potential hidden expenses

        Formatting the plan:
        - Use clean markdown with headers and bullet points
        - Organize a day-by-day agenda with timing estimates
        - Incorporate maps or links where helpful
        - Use emojis to enhance readability and engagement
        - Emphasize booking deadlines and local customs tips
    """),
    expected_output=dedent("""\
        # Travel Plan: {Destination} 🌏

        ## Trip Summary
        - **Dates:** {dates}
        - **Number of Travelers:** {group_size}
        - **Budget per Person:** {budget}
        - **Travel Style:** {style}

        ## Accommodation Options 🛏️
        {Descriptions of lodging with pros and cons}

        ## Daily Schedule

        ### Day 1
        {Activities, timings, transport notes}

        ### Day 2
        {Activities, timings, transport notes}

        [Continue for each travel day...]

        ## Budget Breakdown 💰
        - Lodging: {amount}
        - Activities: {amount}
        - Transport: {amount}
        - Meals: {amount}
        - Other: {amount}

        ## Essential Information ℹ️
        {Important tips, booking advice, and cultural notes}

        ## Booking Checklist 📝
        {Items and dates for advance reservations}

        ## Insider Tips 🎒
        {Local insights and recommendations}

        ---
        Crafted with care by TripTailor
        Last updated: {current_time}
    """),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
)


# Example use case
if __name__ == "__main__":
    travel_agent.print_response(
        dedent("""
        Help me organize a 3-day offsite in London for 14 colleagues from March 28-30 with a budget of $10,000 each.
        Please suggest accommodations, activities, coworking spaces, and detailed daily itinerary including transport.
        """
        ),
        stream=True,
        markdown=False
    )

# Fresh example prompts to inspire users:
"""
Team Events:
1. "Plan a corporate retreat in Costa Rica for 25 people"
2. "Organize an innovation workshop weekend in Stockholm"
3. "Design a wellness weekend for a tech startup in Bali"
4. "Create a networking event itinerary in San Francisco"

Culture & Heritage:
1. "Build a traditional arts and crafts tour in Kyoto"
2. "Design a culinary and wine tasting trip through Tuscany"
3. "Plan a historical exploration of Ancient Rome"
4. "Organize a festival-focused trip to India"

Adventure & Nature:
1. "Plan a hiking and camping trip in Patagonia"
2. "Design a safari itinerary in Tanzania"
3. "Create a diving and snorkeling adventure in the Great Barrier Reef"
4. "Organize a ski trip to the Swiss Alps"

Luxury Travel:
1. "Plan a luxury wellness retreat in the Maldives"
2. "Design a private yacht tour of the Greek Islands"
3. "Create a gourmet food tour in Paris"
4. "Organize a luxury train journey across Europe"
"""
