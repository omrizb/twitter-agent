from typing import List, Optional, Literal
from pydantic import BaseModel
from agents import Agent, ModelSettings

from utils.agent_utils import custom_instructions


class ContentCreatorAgentOutput(BaseModel):
    primary_content: str
    platform: Literal["twitter", "instagram", "email"]
    content_type: Literal["tweet", "reply", "dm", "email", "story", "post"]
    alternative_versions: Optional[List[str]] = None


def create_content_creator_agent() -> Agent:
    """Create a content creator agent with specified character profile."""

    return Agent(
        name="Content Creator Agent",
        instructions=custom_instructions,
        model_settings=ModelSettings(temperature=0.7),
        output_type=ContentCreatorAgentOutput,
    )
