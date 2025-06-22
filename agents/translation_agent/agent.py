# aa
import asyncio
import json
import os
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.cartesia import CartesiaTools
from agno.utils.media import save_audio
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings

# Verify the env variables
settings = Settings()
settings.validate()

agent_instructions = dedent(
    """\
    1. Identify the text and target language from the user request.
    2. Translate the text to the target language.
    3. Analyze the emotion of the translated text.
    4. Select a Cartesia voice matching the language and emotion.
    5. Generate a localized voice using the selected voice.
    6. Synthesize the translated text as a voice note (audio file) with the localized voice.
    7. Output only the result and audio file, no extra commentary.
    """
)

agent = Agent(
    name="Emotion-Aware Translator Agent",
    description="Translates text, detects emotion, and generates a localized voice note using Cartesia TTS tools.",
    instructions=agent_instructions,
    model=OpenAIChat(id="gpt-4o-mini", api_key=settings.openai_api_key),
    tools=[CartesiaTools(voice_localize_enabled=True)],
    show_tool_calls=True,
)

agent.print_response(
    "Translate 'Good morning! I hope you have a wonderful day.' to Spanish and create a voice note."
)
response = agent.run_response

print("\nChecking for Audio Artifacts on Agent...")
if response.audio:
    save_audio(
        base64_data=response.audio[0].base64_audio, output_path="tmp/greeting.mp3"
    )