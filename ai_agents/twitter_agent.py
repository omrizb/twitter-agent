from typing import Optional, Literal
from pydantic import BaseModel, model_validator
from agents import Agent, ModelSettings

from utils.agent_utils import custom_instructions
from agent_tools.content_tools import create_social_content
from agent_tools.twitter_tools import (
    post_tweet,
    delete_tweet,
    like_tweet,
    unlike_tweet,
    retweet,
    unretweet,
    follow_user,
    unfollow_user,
    search_tweets,
    get_tweet_by_id,
    get_user_tweets,
    get_my_profile,
    analyze_trending_topics,
)


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


def create_twitter_agent() -> Agent:
    """Create a Twitter agent with specified character profile."""

    return Agent(
        name="Twitter Agent",
        instructions=custom_instructions,
        tools=[
            create_social_content,
            post_tweet,
            # delete_tweet,
            # like_tweet,
            # unlike_tweet,
            # retweet,
            # unretweet,
            # follow_user,
            # unfollow_user,
            # search_tweets,
            # get_tweet_by_id,
            # get_user_tweets,
            # get_my_profile,
            # analyze_trending_topics,
        ],
        model_settings=ModelSettings(temperature=0),
        handoff_description="A twitter agent that can fully execute actions on twitter",
        output_type=TwitterAgentOutput,
    )
