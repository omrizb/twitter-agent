from agents import Agent, RunContextWrapper
from dataclasses import dataclass
from utils.common_utils import read_file

@dataclass
class AgentContext:
    character_file: str

def custom_instructions(
    run_context: RunContextWrapper[AgentContext], agent: Agent[AgentContext]
) -> str:
    character_file = run_context.context.character_file
    instructions_file = ""

    if agent.name == "Twitter Agent":
        instructions_file = "twitter_agent_instructions.md"
    elif agent.name == "Content Creator Agent":
        instructions_file = "content_creator_agent_instructions.md"
    else:
        raise ValueError(f"Agent {agent.name} not found")

    return read_file(f"ai_agents/{instructions_file}") + read_file(
        f"characters/{character_file}"
    )