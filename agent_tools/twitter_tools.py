# Twitter Tools for AVA

import os
import json
import time
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from agents import function_tool
import tweepy
from openai import OpenAI

# # Initialize OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Initialize Twitter API client
# def get_twitter_client():
#     """Initialize and return Twitter API client."""
#     auth = tweepy.OAuthHandler(
#         os.getenv("TWITTER_API_KEY"),
#         os.getenv("TWITTER_API_SECRET_KEY")
#     )
#     auth.set_access_token(
#         os.getenv("TWITTER_ACCESS_TOKEN"),
#         os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
#     )
#     return tweepy.API(auth)

# @function_tool
# def generate_tweet_content(topic: str, tone: str = "professional", max_length: int = 280) -> str:
#     """Generate tweet content based on a topic and tone.
    
#     Args:
#         topic (str): The topic or subject for the tweet
#         tone (str): The tone of the tweet (professional, casual, humorous, etc.)
#         max_length (int): Maximum length of the tweet (default 280)
    
#     Returns:
#         str: Generated tweet content
#     """
#     try:
#         prompt = f"""
#         Generate a tweet about: {topic}
        
#         Requirements:
#         - Tone: {tone}
#         - Maximum length: {max_length} characters
#         - Engaging and relevant
#         - Include appropriate hashtags if relevant
#         - Make it shareable and interesting
        
#         Tweet:
#         """
        
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a social media expert who creates engaging tweets."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=150,
#             temperature=0.7
#         )
        
#         tweet_content = response.choices[0].message.content.strip()
        
#         # Ensure it doesn't exceed character limit
#         if len(tweet_content) > max_length:
#             tweet_content = tweet_content[:max_length-3] + "..."
        
#         return tweet_content
        
#     except Exception as e:
#         return f"Error generating tweet: {str(e)}"

# @function_tool
# def analyze_trending_topics(category: str = "general") -> Dict[str, Any]:
#     """Analyze trending topics for tweet inspiration.
    
#     Args:
#         category (str): Category of topics to analyze (general, tech, business, etc.)
    
#     Returns:
#         dict: Trending topics with relevance scores
#     """
#     try:
#         # This is a simplified version - in a real implementation,
#         # you might use Twitter's trending topics API or other services
#         prompt = f"""
#         Analyze current trending topics in the {category} category.
#         Provide 5 trending topics with brief descriptions and relevance scores (1-10).
        
#         Format as JSON:
#         {{
#             "trending_topics": [
#                 {{
#                     "topic": "topic name",
#                     "description": "brief description",
#                     "relevance_score": 8,
#                     "hashtags": ["#hashtag1", "#hashtag2"]
#                 }}
#             ]
#         }}
#         """
        
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a social media trend analyst."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=300,
#             temperature=0.5
#         )
        
#         result = json.loads(response.choices[0].message.content)
#         return result
        
#     except Exception as e:
#         return {
#             "error": f"Error analyzing trends: {str(e)}",
#             "trending_topics": []
#         }

# @function_tool
# def post_tweet(tweet_content: str) -> Dict[str, Any]:
#     """Post a tweet using Twitter API.
    
#     Args:
#         tweet_content (str): The content of the tweet to post
    
#     Returns:
#         dict: Response with tweet details or error message
#     """
#     try:
#         api = get_twitter_client()
        
#         # Post the tweet
#         tweet = api.update_status(tweet_content)
        
#         return {
#             "success": True,
#             "tweet_id": tweet.id,
#             "tweet_text": tweet.text,
#             "created_at": tweet.created_at.isoformat(),
#             "user": tweet.user.screen_name
#         }
        
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e)
#         }

# @function_tool
# def schedule_tweet(tweet_content: str, scheduled_time: str) -> Dict[str, Any]:
#     """Schedule a tweet for later posting.
    
#     Args:
#         tweet_content (str): The content of the tweet
#         scheduled_time (str): When to post the tweet (ISO format)
    
#     Returns:
#         dict: Response with scheduling details
#     """
#     try:
#         # Parse the scheduled time
#         scheduled_datetime = datetime.fromisoformat(scheduled_time)
#         current_time = datetime.now()
        
#         if scheduled_datetime <= current_time:
#             return {
#                 "success": False,
#                 "error": "Scheduled time must be in the future"
#             }
        
#         # For now, we'll just save it to a file
#         # In a production environment, you'd use a proper scheduling service
#         scheduled_tweets_file = "scheduled_tweets.json"
        
#         # Load existing scheduled tweets
#         scheduled_tweets = []
#         if os.path.exists(scheduled_tweets_file):
#             with open(scheduled_tweets_file, 'r') as f:
#                 scheduled_tweets = json.load(f)
        
#         # Add new scheduled tweet
#         new_tweet = {
#             "id": int(time.time()),
#             "content": tweet_content,
#             "scheduled_time": scheduled_time,
#             "status": "pending"
#         }
        
#         scheduled_tweets.append(new_tweet)
        
#         # Save back to file
#         with open(scheduled_tweets_file, 'w') as f:
#             json.dump(scheduled_tweets, f, indent=2)
        
#         return {
#             "success": True,
#             "tweet_id": new_tweet["id"],
#             "scheduled_time": scheduled_time,
#             "message": f"Tweet scheduled for {scheduled_time}"
#         }
        
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e)
#         }

# @function_tool
# def get_tweet_analytics(tweet_id: str) -> Dict[str, Any]:
#     """Get analytics for a specific tweet.
    
#     Args:
#         tweet_id (str): The ID of the tweet to analyze
    
#     Returns:
#         dict: Analytics data for the tweet
#     """
#     try:
#         api = get_twitter_client()
        
#         # Get tweet details
#         tweet = api.get_status(tweet_id)
        
#         return {
#             "tweet_id": tweet_id,
#             "text": tweet.text,
#             "created_at": tweet.created_at.isoformat(),
#             "retweet_count": tweet.retweet_count,
#             "favorite_count": tweet.favorite_count,
#             "user": tweet.user.screen_name,
#             "engagement_rate": (tweet.retweet_count + tweet.favorite_count) / max(tweet.user.followers_count, 1)
#         }
        
#     except Exception as e:
#         return {
#             "error": f"Error getting analytics: {str(e)}"
#         }

# @function_tool
# def check_twitter_credentials() -> Dict[str, Any]:
#     """Check if Twitter API credentials are valid.
    
#     Returns:
#         dict: Status of Twitter credentials
#     """
#     try:
#         api = get_twitter_client()
#         user = api.verify_credentials()
        
#         return {
#             "valid": True,
#             "username": user.screen_name,
#             "followers_count": user.followers_count,
#             "following_count": user.friends_count
#         }
        
#     except Exception as e:
#         return {
#             "valid": False,
#             "error": str(e)
#         } 