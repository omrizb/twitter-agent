# Twitter Agent

An AI-powered Twitter agent that can create and post social media content using OpenAI's Agents SDK. The agent generates branded content and manages Twitter interactions based on character profiles.

## Features

- 🤖 AI-powered content generation for tweets, replies, and DMs
- 🎭 Customizable character profiles for different brand voices
- 📱 Direct Twitter integration for posting content
- 🔄 Multi-agent workflow with content creation and posting capabilities

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/omrizb/twitter-agent.git
   cd twitter-agent
   ```

2. **Install dependencies with uv**
   ```bash
   uv sync
   ```

## Environment Setup

1. **Copy the environment template**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file with your API credentials**

```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Twitter API (OAuth 1.0a)
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET_KEY=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
```

### Getting Twitter API Credentials

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app or use an existing one
3. Generate OAuth 1.0a credentials (API Key, API Secret, Access Token, Access Token Secret)
4. Ensure your app has read and write permissions

## Running the Agent

```bash
uv run python main.py
```

The agent will prompt you for a request. Examples:
- "Post a tweet about fresh organic strawberries"
- "Reply to the customer who thanked us for avocado tips"
- "Create a friendly DM about order confirmation"

## Customizing Character Profiles

Edit character files in the `characters/` directory to change the agent's personality and brand voice. The default character is `fresh_harvest.md`.

## Project Structure

```
twitter-agent/
├── ai_agents/          # Agent definitions and instructions
├── agent_tools/        # Twitter API tools and content creation
├── characters/         # Brand character profiles
├── utils/             # Shared utilities and types
└── main.py           # Main entry point
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure
- Add `.env` to your `.gitignore` file
