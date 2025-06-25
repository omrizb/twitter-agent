from typing import Literal, Optional
from datetime import datetime, timezone
from pydantic import BaseModel
from agents import Runner, RunContextWrapper, function_tool
from ai_agents.content_creator_agent import create_content_creator_agent

from utils.agent_utils import AgentContext
from utils.shared_types import ToolResponse


class ContentCreatorInput(BaseModel):
    topic: str
    platform: Literal["twitter", "instagram", "email"]
    content_type: Literal["tweet", "reply", "dm", "email", "story", "post"]
    content_max_length: Optional[int] = None
    tone: Optional[str] = None
    context: Optional[str] = None
    require_variations: Optional[bool] = False


@function_tool
async def create_social_content(context: RunContextWrapper[AgentContext], input: ContentCreatorInput) -> ToolResponse:
    """
    Generate branded social media content using the content creator agent.

    Args:
        input (ContentCreatorInput): The content creation request containing:
            - topic (str): The main subject or theme for the content.
            - platform (Literal["twitter", "instagram", "email"]): Target platform for the content.
            - content_type (Literal["tweet", "reply", "dm", "email", "story", "post"]): Type of content to generate.
            - content_max_length (Optional[int]): Maximum character limit for the content.
            - tone (Optional[str]): Desired tone or style (e.g., "professional", "casual", "friendly").
            - context (Optional[str]): Additional context or background information (e.g. conversation snippet, related news article, etc.).
            - require_variations (Optional[bool]): Whether to include alternative versions (default: False).

    Returns:
        ToolResponse: On success, `data` contains:
            - content (str): The primary generated content text.
            - platform (str): The target platform for the content.
            - content_type (str): The type of content generated.
            - alternative_versions (Optional[List[str]]): Alternative content versions if requested.
            - created_at (str): ISO 8601 UTC timestamp of content creation.
    """
    try:
        agent = create_content_creator_agent()

        # Build the mission prompt
        mission = (
            f"Generate a {input.content_type} for {input.platform} about {input.topic}."
        )
        if input.content_max_length:
            mission += (
                f" Content must be {input.content_max_length} characters or less."
            )
        if input.tone:
            mission += f" Use a {input.tone} tone."
        if input.context:
            mission += f" Context: {input.context}"
        if input.require_variations:
            mission += " Include 2-3 alternative versions."

        character_file = context.context.character_file

        # Run agent
        result = await Runner.run(
            agent,
            mission,
            context=AgentContext(character_file=character_file),
        )

        return ToolResponse(
            success=True,
            data={
                "content": result.final_output.primary_content,
                "platform": result.final_output.platform,
                "content_type": result.final_output.content_type,
                "alternative_versions": result.final_output.alternative_versions,
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as e:
        return ToolResponse(success=False, error=str(e))
