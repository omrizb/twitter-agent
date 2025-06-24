import os
import asyncio
from dotenv import load_dotenv
from agents import Runner

from ai_agents.twitter_agent import create_twitter_agent
from utils.agent_utils import AgentContext
from utils.common_utils import handle_stream_events


load_dotenv()

async def main():
    """Main function to run the Twitter AI agent."""

    # Check if OpenAI and Twitter credentials are configured
    if not all(
        [
            os.getenv("OPENAI_API_KEY"),
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET_KEY"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        ]
    ):
        print("❌ API credentials not found in .env file")
        print("Please configure the following environment variables:")
        print("- OPENAI_API_KEY")
        print("- TWITTER_API_KEY")
        print("- TWITTER_API_SECRET_KEY")
        print("- TWITTER_ACCESS_TOKEN")
        print("- TWITTER_ACCESS_TOKEN_SECRET")
        return

    print("Twitter Agent Starting...")

    # Create the Twitter agent (you can specify different character files)
    twitter_agent = create_twitter_agent()

    # Get request from user
    request = input("Request: ").strip()
    print(f"\n📝 Processing request: {request}")
    print()

    # Run the agent
    result = Runner.run_streamed(
        starting_agent=twitter_agent,
        input=request,
        context=AgentContext(character_file="fresh_harvest.md"),
    )

    # Handle stream events
    await handle_stream_events(result)

    print()
    print("--- Twitter Agent Output ---")
    print(f"Action: {result.final_output.action_type}")
    print(f"Reasoning: {result.final_output.reasoning}")
    if result.final_output.tweet_content:
        print(f"Content: {result.final_output.tweet_content}")
    print()


if __name__ == "__main__":
    asyncio.run(main())
