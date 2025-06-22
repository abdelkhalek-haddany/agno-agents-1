from agno.agent import Agent
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.models.openai import OpenAIChat
from rich.pretty import pprint
from agno.models.openai import OpenAIChat
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings


#Verify the env variables
settings = Settings()
settings.validate()

user_id = "haddany"
memory = Memory(
    db=SqliteMemoryDb(table_name="memory", db_file="agents_data_memory/memory.db"),
    model=OpenAIChat(id="gpt-4o-mini", api_key=settings.openai_api_key),
)
memory.clear()

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini", api_key=settings.openai_api_key),
    user_id=user_id,
    memory=memory,
    # Enable the Agent to dynamically create and manage user memories
    enable_agentic_memory=True,
    add_datetime_to_instructions=True,
    markdown=True,
)

if __name__ == "__main__":
    agent.print_response("My name is Abdelkhalek Haddany and I like to eat moroccain koskos.")
    memories = memory.get_user_memories(user_id=user_id)
    print(f"Memories about {user_id}:")
    pprint(memories)
    agent.print_response("What is my favorite food?")
    agent.print_response("My favorite language is python.")
    memories = memory.get_user_memories(user_id=user_id)
    print(f"Memories about {user_id}:")
    pprint(memories)
    agent.print_response("Recommend a good ai agent app, any framework i should use?")
    agent.print_response("What have we been talking about?")