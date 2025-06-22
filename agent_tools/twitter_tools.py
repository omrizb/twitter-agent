import os
import tweepy
from agents import function_tool
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, timezone


class ToolResponse(BaseModel):
    """
    Standardized response format used by all Twitter agent tool functions.

    Attributes:
        success (bool): Whether the operation was successful.
        data (Optional[dict]): Function-specific data payload if successful.
        error (Optional[str]): Error message if the operation failed.
    """

    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class TwitterAPI:
    """Twitter API wrapper using Tweepy for posting tweets and handling media uploads"""

    def __init__(self):
        """Initialize Twitter API clients with OAuth 1.0a credentials from environment variables"""
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET_KEY")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

        if not all(
            [self.api_key, self.api_secret, self.access_token, self.access_token_secret]
        ):
            raise ValueError("Missing required Twitter OAuth 1.0a credentials")

        # Initialize v1.1 API (required for media uploads and some tweet functionality)
        auth_v1 = tweepy.OAuth1UserHandler(
            self.api_key, self.api_secret, self.access_token, self.access_token_secret
        )
        self.api_v1 = tweepy.API(auth_v1, wait_on_rate_limit=True)

        # Initialize v2 Client with user context (for tweet creation, reading, etc.)
        self.client_v2 = tweepy.Client(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            wait_on_rate_limit=True,
        )

    def _format_tweet_data(self, tweet) -> Dict[str, Any]:
        """Format tweet data for consistent output"""
        return {
            "id": tweet.id,
            "text": tweet.text,
            "created_at": tweet.created_at.isoformat() if tweet.created_at else None,
            "author_id": tweet.author_id,
            "public_metrics": getattr(tweet, "public_metrics", {}),
            "conversation_id": getattr(tweet, "conversation_id", None),
            "in_reply_to_user_id": getattr(tweet, "in_reply_to_user_id", None),
        }


# Initialize global Twitter API instance
_twitter_api = None


def _get_twitter_api() -> Optional[TwitterAPI]:
    global _twitter_api
    if _twitter_api is None:
        try:
            _twitter_api = TwitterAPI()
        except ValueError as e:
            print(f"Warning: {e}")
            return None
    return _twitter_api


@function_tool
def post_tweet(
    content: str, in_reply_to_tweet_id: Optional[str] = None
) -> ToolResponse:
    """
    Post a tweet using the authenticated user's Twitter account.

    Args:
        content (str): The tweet content (must be 280 characters or fewer).
        in_reply_to_tweet_id (Optional[str]): Optional tweet ID to reply to.

    Returns:
        ToolResponse: On success, `data` contains:
            - tweet_id (str): ID of the created tweet.
            - content (str): The tweet text.
            - created_at (str): ISO 8601 UTC timestamp.
            - in_reply_to (Optional[str]): Replied tweet ID, if applicable.
    """
    twitter_api = _get_twitter_api()
    if not twitter_api:
        return ToolResponse(success=False, error="Twitter API not initialized")

    if len(content) > 280:
        return ToolResponse(
            success=False, error=f"Tweet too long: {len(content)} characters (max 280)"
        )

    try:
        response = twitter_api.client_v2.create_tweet(
            text=content, in_reply_to_tweet_id=in_reply_to_tweet_id
        )

        return ToolResponse(
            success=True,
            data={
                "tweet_id": response.data["id"],
                "content": content,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "in_reply_to": in_reply_to_tweet_id,
            },
        )

    except Exception as e:
        return ToolResponse(success=False, error=str(e))


@function_tool
def delete_tweet(tweet_id: str) -> ToolResponse:
    """
    Delete a tweet using the authenticated user's Twitter account.

    Args:
        tweet_id (str): The ID of the tweet to delete.

    Returns:
        ToolResponse: On success, `data` contains:
            - tweet_id (str): ID of the deleted tweet.
            - deleted (bool): Confirmation that the tweet was deleted.
            - deleted_at (str): ISO 8601 UTC timestamp of deletion.
    """
    twitter_api = _get_twitter_api()
    if not twitter_api:
        return ToolResponse(success=False, error="Twitter API not initialized")

    try:
        response = twitter_api.client_v2.delete_tweet(tweet_id)
        return ToolResponse(
            success=True,
            data={
                "tweet_id": tweet_id,
                "deleted": True,
                "deleted_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as e:
        return ToolResponse(success=False, error=str(e))


@function_tool
def like_tweet(tweet_id: str) -> ToolResponse:
    """
    Like a tweet using the authenticated user's Twitter account.

    Args:
        tweet_id (str): The ID of the tweet to like.

    Returns:
        ToolResponse: On success, `data` contains:
            - tweet_id (str): ID of the liked tweet.
            - liked (bool): Confirmation that the tweet was liked.
            - liked_at (str): ISO 8601 UTC timestamp of the like action.
    """
    twitter_api = _get_twitter_api()
    if not twitter_api:
        return ToolResponse(success=False, error="Twitter API not initialized")

    try:
        response = twitter_api.client_v2.like(tweet_id)
        return ToolResponse(
            success=True,
            data={
                "tweet_id": tweet_id,
                "liked": response.data["liked"],
                "liked_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as e:
        return ToolResponse(success=False, error=str(e))


@function_tool
def unlike_tweet(tweet_id: str) -> ToolResponse:
    """
    Unlike a tweet using the authenticated user's Twitter account.

    Args:
        tweet_id (str): The ID of the tweet to unlike.

    Returns:
        ToolResponse: On success, `data` contains:
            - tweet_id (str): ID of the unliked tweet.
            - liked (bool): Confirmation that the tweet was unliked (should be False).
            - unliked_at (str): ISO 8601 UTC timestamp of the unlike action.
    """
    twitter_api = _get_twitter_api()
    if not twitter_api:
        return ToolResponse(success=False, error="Twitter API not initialized")

    try:
        response = twitter_api.client_v2.unlike(tweet_id)
        return ToolResponse(
            success=True,
            data={
                "tweet_id": tweet_id,
                "liked": response.data["liked"],
                "unliked_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as e:
        return ToolResponse(success=False, error=str(e))


@function_tool
def retweet(tweet_id: str) -> ToolResponse:
    """
    Retweet a tweet using the authenticated user's Twitter account.

    Args:
        tweet_id (str): The ID of the tweet to retweet.

    Returns:
        ToolResponse: On success, `data` contains:
            - tweet_id (str): ID of the original tweet.
            - retweet_id (str): ID of the new retweet.
            - retweeted (bool): Confirmation that the tweet was retweeted.
            - retweeted_at (str): ISO 8601 UTC timestamp of the retweet action.
    """
    twitter_api = _get_twitter_api()
    if not twitter_api:
        return ToolResponse(success=False, error="Twitter API not initialized")

    try:
        response = twitter_api.client_v2.retweet(tweet_id)
        return ToolResponse(
            success=True,
            data={
                "tweet_id": tweet_id,
                "retweet_id": response.data["id"],
                "retweeted": response.data["retweeted"],
                "retweeted_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as e:
        return ToolResponse(success=False, error=str(e))


@function_tool
def unretweet(tweet_id: str) -> ToolResponse:
    """
    Unretweet a tweet using the authenticated user's Twitter account.

    Args:
        tweet_id (str): The ID of the tweet to unretweet.

    Returns:
        ToolResponse: On success, `data` contains:
            - tweet_id (str): ID of the original tweet.
            - retweeted (bool): Confirmation that the tweet was unretweeted (should be False).
            - unretweeted_at (str): ISO 8601 UTC timestamp of the unretweet action.
    """
    twitter_api = _get_twitter_api()
    if not twitter_api:
        return ToolResponse(success=False, error="Twitter API not initialized")

    try:
        response = twitter_api.client_v2.unretweet(tweet_id)
        return ToolResponse(
            success=True,
            data={
                "tweet_id": tweet_id,
                "retweeted": response.data["retweeted"],
                "unretweeted_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as e:
        return ToolResponse(success=False, error=str(e))


@function_tool
def follow_user(username: str) -> ToolResponse:
    """
    Follow a user using the authenticated user's Twitter account.

    Args:
        username (str): The username (without @) of the user to follow.

    Returns:
        ToolResponse: On success, `data` contains:
            - username (str): The username that was followed.
            - user_id (str): The user ID of the followed user.
            - following (bool): Confirmation that the user is now being followed.
            - followed_at (str): ISO 8601 UTC timestamp of the follow action.
    """
    twitter_api = _get_twitter_api()
    if not twitter_api:
        return ToolResponse(success=False, error="Twitter API not initialized")

    try:
        # First get the user ID from username
        user = twitter_api.client_v2.get_user(username=username)
        if not user.data:
            return ToolResponse(success=False, error=f"User '{username}' not found")

        user_id = user.data.id
        response = twitter_api.client_v2.follow_user(user_id)

        return ToolResponse(
            success=True,
            data={
                "username": username,
                "user_id": str(user_id),
                "following": response.data["following"],
                "followed_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as e:
        return ToolResponse(success=False, error=str(e))


@function_tool
def unfollow_user(username: str) -> ToolResponse:
    """
    Unfollow a user using the authenticated user's Twitter account.

    Args:
        username (str): The username (without @) of the user to unfollow.

    Returns:
        ToolResponse: On success, `data` contains:
            - username (str): The username that was unfollowed.
            - user_id (str): The user ID of the unfollowed user.
            - following (bool): Confirmation that the user is no longer being followed (should be False).
            - unfollowed_at (str): ISO 8601 UTC timestamp of the unfollow action.
    """
    twitter_api = _get_twitter_api()
    if not twitter_api:
        return ToolResponse(success=False, error="Twitter API not initialized")

    try:
        # First get the user ID from username
        user = twitter_api.client_v2.get_user(username=username)
        if not user.data:
            return ToolResponse(success=False, error=f"User '{username}' not found")

        user_id = user.data.id
        response = twitter_api.client_v2.unfollow_user(user_id)

        return ToolResponse(
            success=True,
            data={
                "username": username,
                "user_id": str(user_id),
                "following": response.data["following"],
                "unfollowed_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as e:
        return ToolResponse(success=False, error=str(e))


@function_tool
def search_tweets(query: str, max_results: int = 10) -> ToolResponse:
    """
    Search for tweets using the Twitter API.

    Args:
        query (str): The search query string.
        max_results (int): Maximum number of results to return (default: 10, max: 100).

    Returns:
        ToolResponse: On success, `data` contains:
            - tweets (list): List of tweet objects with tweet data.
            - count (int): Number of tweets returned.
            - query (str): The original search query.
            - searched_at (str): ISO 8601 UTC timestamp of the search.
    """
    twitter_api = _get_twitter_api()
    if not twitter_api:
        return ToolResponse(success=False, error="Twitter API not initialized")

    if max_results > 100:
        max_results = 100

    try:
        response = twitter_api.client_v2.search_recent_tweets(
            query=query, max_results=max_results
        )

        tweets = []
        if response.data:
            for tweet in response.data:
                tweets.append(twitter_api._format_tweet_data(tweet))

        return ToolResponse(
            success=True,
            data={
                "tweets": tweets,
                "count": len(tweets),
                "query": query,
                "searched_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as e:
        return ToolResponse(success=False, error=str(e))


@function_tool
def get_tweet_by_id(tweet_id: str) -> ToolResponse:
    """
    Get a specific tweet by its ID using the Twitter API.

    Args:
        tweet_id (str): The ID of the tweet to retrieve.

    Returns:
        ToolResponse: On success, `data` contains:
            - tweet (dict): The tweet object with all available data.
            - retrieved_at (str): ISO 8601 UTC timestamp of the retrieval.
    """
    twitter_api = _get_twitter_api()
    if not twitter_api:
        return ToolResponse(success=False, error="Twitter API not initialized")

    try:
        response = twitter_api.client_v2.get_tweet(tweet_id)

        if not response.data:
            return ToolResponse(
                success=False, error=f"Tweet with ID '{tweet_id}' not found"
            )

        tweet_data = twitter_api._format_tweet_data(response.data)

        return ToolResponse(
            success=True,
            data={
                "tweet": tweet_data,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as e:
        return ToolResponse(success=False, error=str(e))


@function_tool
def get_user_tweets(username: str, max_results: int = 10) -> ToolResponse:
    """
    Get tweets from a specific user using the Twitter API.

    Args:
        username (str): The username (without @) of the user whose tweets to retrieve.
        max_results (int): Maximum number of tweets to return (default: 10, max: 100).

    Returns:
        ToolResponse: On success, `data` contains:
            - tweets (list): List of tweet objects from the user.
            - count (int): Number of tweets returned.
            - username (str): The username whose tweets were retrieved.
            - user_id (str): The user ID of the account.
            - retrieved_at (str): ISO 8601 UTC timestamp of the retrieval.
    """
    twitter_api = _get_twitter_api()
    if not twitter_api:
        return ToolResponse(success=False, error="Twitter API not initialized")

    if max_results > 100:
        max_results = 100

    try:
        # First get the user ID from username
        user = twitter_api.client_v2.get_user(username=username)
        if not user.data:
            return ToolResponse(success=False, error=f"User '{username}' not found")

        user_id = user.data.id

        # Get user's tweets
        response = twitter_api.client_v2.get_users_tweets(
            user_id, max_results=max_results
        )

        tweets = []
        if response.data:
            for tweet in response.data:
                tweets.append(twitter_api._format_tweet_data(tweet))

        return ToolResponse(
            success=True,
            data={
                "tweets": tweets,
                "count": len(tweets),
                "username": username,
                "user_id": str(user_id),
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as e:
        return ToolResponse(success=False, error=str(e))


@function_tool
def get_my_profile() -> ToolResponse:
    """
    Get the authenticated user's profile information using the Twitter API.

    Returns:
        ToolResponse: On success, `data` contains:
            - profile (dict): The user's profile information including:
                - id (str): User ID.
                - username (str): Username (without @).
                - name (str): Display name.
                - description (str): Bio/description.
                - followers_count (int): Number of followers.
                - following_count (int): Number of users being followed.
                - tweet_count (int): Number of tweets.
                - created_at (str): Account creation date.
            - retrieved_at (str): ISO 8601 UTC timestamp of the retrieval.
    """
    twitter_api = _get_twitter_api()
    if not twitter_api:
        return ToolResponse(success=False, error="Twitter API not initialized")

    try:
        response = twitter_api.client_v2.get_me()

        if not response.data:
            return ToolResponse(
                success=False, error="Could not retrieve profile information"
            )

        user = response.data
        profile = {
            "id": str(user.id),
            "username": user.username,
            "name": user.name,
            "description": user.description,
            "followers_count": user.public_metrics["followers_count"],
            "following_count": user.public_metrics["following_count"],
            "tweet_count": user.public_metrics["tweet_count"],
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }

        return ToolResponse(
            success=True,
            data={
                "profile": profile,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except Exception as e:
        return ToolResponse(success=False, error=str(e))


@function_tool
def analyze_trending_topics(location_id: int = 1) -> ToolResponse:
    """
    Analyze trending topics using the Twitter API.

    Args:
        location_id (int): The location ID for trending topics (default: 1 for worldwide).

    Returns:
        ToolResponse: On success, `data` contains:
            - trends (list): List of trending topics with:
                - name (str): Topic name.
                - query (str): Search query for the topic.
                - tweet_volume (int): Number of tweets about this topic.
                - url (str): Twitter URL for the topic.
            - count (int): Number of trending topics returned.
            - location_id (int): The location ID used for the search.
            - analyzed_at (str): ISO 8601 UTC timestamp of the analysis.
    """
    twitter_api = _get_twitter_api()
    if not twitter_api:
        return ToolResponse(success=False, error="Twitter API not initialized")

    try:
        # Note: Twitter API v2 doesn't have trending topics endpoint
        # This would require using v1.1 API or a different approach
        # For now, returning a placeholder response
        return ToolResponse(
            success=False,
            error="Trending topics analysis not available with current API setup",
        )
    except Exception as e:
        return ToolResponse(success=False, error=str(e))


@function_tool
def generate_tweet_content(
    topic: str, style: str = "engaging", max_length: int = 280
) -> str:
    """
    Generate tweet content based on a topic and style.

    Args:
        topic (str): The topic or subject for the tweet.
        style (str): The style of the tweet (default: "engaging").
        max_length (int): Maximum length of the tweet (default: 280).

    Returns:
        str: Generated tweet content.
    """
    # This is a placeholder function - in a real implementation,
    # you would integrate with an AI service like OpenAI
    return f"Generated tweet about {topic} in {style} style (max {max_length} chars)"


if __name__ == "__main__":
    print(post_tweet("Hello, world!"))
