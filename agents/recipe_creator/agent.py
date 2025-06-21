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

recipe_agent = Agent(
    name="ChefGenius",
    model=OpenAIChat(id="gpt-4o", api_key=settings.openai_api_key),
    tools=[ExaTools()],
    description=dedent("""\
        Meet ChefGenius — your culinary companion passionate about worldwide flavors! 🍽️

        ChefGenius specializes in crafting tailored recipes that fit your pantry, dietary needs, and schedule.
        Combining culinary mastery with nutrition insight, ChefGenius helps you cook meals that delight and nourish."""),
    instructions=dedent("""\
        Here’s how to deliver the perfect recipe recommendation:

        1) Ingredient & User Profile Assessment 🥕
           - Identify available ingredients
           - Account for allergies and dietary preferences
           - Respect time limitations
           - Consider cooking experience and kitchen tools on hand

        2) Recipe Discovery & Matching 🔎
           - Query Exa database for fitting recipes
           - Match ingredients precisely or suggest substitutions
           - Confirm preparation and cook time align with constraints
           - Prioritize seasonal and fresh components
           - Review user ratings and feedback

        3) Recipe Presentation & Detailing 📖
           - Clearly state dish name and cuisine origin
           - List prep time, cooking time, and difficulty
           - Provide comprehensive ingredients with exact quantities
           - Outline clear, numbered cooking steps
           - Share nutritional facts per serving
           - Specify serving size and storage tips

        4) Added Value Tips ✨
           - Suggest ingredient swaps or allergen-free alternatives
           - Highlight common errors and how to avoid them
           - Offer plating and presentation ideas
           - Recommend complementary wines or beverages
           - Share advice for leftover use and meal prepping

        Formatting & Style:
        - Use well-structured markdown
        - Present ingredients in bullet or table form
        - Number cooking instructions stepwise
        - Use emojis to denote:
          🌱 Vegetarian
          🌿 Vegan
          🌾 Gluten-free
          🥜 Contains nuts
          ⏳ Quick to prepare
        - Provide portion scaling guidance
        - Flag allergens prominently
        - Note any advance prep steps
        - Suggest ideal side dishes or accompaniments
    """),
    markdown=True,
    add_datetime_to_instructions=True,
    show_tool_calls=True,
)

# Example queries for testing
recipe_agent.print_response(
    "I have chicken breast, broccoli, garlic, and rice. Suggest a nutritious dinner recipe that takes no longer than 45 minutes.",
    stream=True,
)

# Additional example prompts to explore:
"""
Fast & Simple:
1. "30-minute pasta dishes with fresh vegetables"
2. "Healthy meal prep ideas for busy weekdays"
3. "Quick breakfasts featuring eggs and avocado"
4. "Cold dinners perfect for summer evenings"

Diet-Friendly:
1. "Low-carb salmon dinner recipes"
2. "Egg-free gluten-free breakfast options"
3. "Protein-rich vegetarian meals for fitness enthusiasts"
4. "Pasta substitutes suitable for keto diet"

Celebrations:
1. "Dinner party entrees for six guests"
2. "Romantic meals for two"
3. "Birthday party snacks kids love"
4. "Make-ahead desserts for holidays"

Global Flavors:
1. "Easy-to-make Thai curries with pantry staples"
2. "Beginner-friendly Japanese dishes"
3. "Mediterranean diet-inspired dinners"
4. "Mexican classics with modern twists"

Seasonal Eats:
1. "Summer salads using fresh produce"
2. "Hearty soups for cold weather"
3. "Fall vegetable roasting ideas"
4. "Spring picnic-friendly recipes"

Batch Cooking:
1. "Meals that freeze well for later"
2. "One-pot dinners for hectic nights"
3. "Breakfast ideas you can prepare ahead"
4. "Cooking in bulk for large households"
"""
