from typing import Optional, Literal
from pydantic import BaseModel, model_validator
from agents import Agent, ModelSettings
from utils.common_utils import read_file


class TwitterAgentOutput(BaseModel):
    action_type: Literal[
        "tweet",
        "reply",
        "retweet",
        "like",
        "dm",
        "follow",
        "unfollow",
        "search",
        "quote",
        "schedule",
        "analyze",
    ]
    tweet_content: Optional[str] = None
    in_reply_to_id: Optional[str] = None
    recipient_user_id: Optional[str] = None
    target_user_id: Optional[str] = None
    tweet_id: Optional[str] = None
    reasoning: str

    @model_validator(mode="after")
    def validate_required_fields(self):
        action = self.action_type

        def required(attr):
            if not getattr(self, attr):
                raise ValueError(f"`{attr}` is required for action '{action}'")

        if action in {"tweet", "quote", "schedule"}:
            required("tweet_content")

        if action == "reply":
            required("tweet_content")
            required("in_reply_to_id")

        if action == "dm":
            required("tweet_content")
            required("recipient_user_id")

        if action in {"like", "retweet", "quote"}:
            required("tweet_id")

        if action in {"follow", "unfollow"}:
            required("target_user_id")

        return self


def create_twitter_agent(character_file: str = "fresh_harvest.md") -> Agent:
    """Create a Twitter agent with specified character profile."""

    instructions = read_file("ai_agents/twitter_agent_instructions.md") + read_file(
        f"characters/{character_file}"
    )

    return Agent(
        name="Twitter Agent",
        instructions=instructions,
        tools=[],
        model_settings=ModelSettings(temperature=0.7),
        output_type=TwitterAgentOutput,
    )
