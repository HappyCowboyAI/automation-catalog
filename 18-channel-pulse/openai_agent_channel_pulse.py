"""
Channel Pulse — OpenAI Agents SDK Implementation

Sends scannable account updates to internal customer channels by pulling
engagement data from People.ai via MCP and summarizing with an LLM.

Requirements:
    pip install openai-agents slack-sdk

Environment variables:
    OPENAI_API_KEY       — OpenAI API key
    SLACK_BOT_TOKEN      — Slack bot token for posting updates
    PEOPLEAI_MCP_URL     — People.ai MCP server URL
"""
from __future__ import annotations

import asyncio
import os
from datetime import datetime, timedelta

from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerSse

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LOOKBACK_DAYS = 7
UPDATE_INTERVAL_SECONDS = 60
CHANNEL_MAP: dict[str, str] = {
    # account_name -> slack_channel_id
    # Configure per deployment
}

SYSTEM_PROMPT = """You are a sales intelligence assistant that generates
scannable account updates for internal customer channels.

You have access to People.ai via MCP tools to pull account activity data.
For each active account, generate an update in this format:

- Lead with account name, deal value, close date, and health indicator
- Section 1: THIS WEEK'S KEY DEVELOPMENTS (3-5 bullets)
- Section 2: RISKS & OPPORTUNITIES (3-5 bullets)
- Section 3: NEXT WEEK'S ACTIONS (3-5 bullets with @owner tags)
- Footer: "Powered by People.ai MCP: please thread comments"

Use emoji section headers. Keep each bullet to one line. Be specific."""


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@function_tool
async def post_to_slack(channel_id: str, message: str) -> str:
    """Post a formatted message to a Slack channel.

    Args:
        channel_id: The Slack channel ID to post to.
        message: The formatted message content.
    """
    from slack_sdk.web.async_client import AsyncWebClient

    client = AsyncWebClient(token=os.environ["SLACK_BOT_TOKEN"])
    result = await client.chat_postMessage(
        channel=channel_id,
        text=message,
        unfurl_links=False,
    )
    return f"Posted to {channel_id}: {result['ts']}"


@function_tool
def get_channel_for_account(account_name: str) -> str:
    """Look up the Slack channel ID for a given account.

    Args:
        account_name: The account name to look up.
    """
    channel = CHANNEL_MAP.get(
        account_name, os.environ.get("DEFAULT_CHANNEL", "")
    )
    return channel or "No channel mapped for this account"


@function_tool
def get_lookback_date() -> str:
    """Get the ISO date string for the start of the lookback window."""
    since = datetime.utcnow() - timedelta(days=LOOKBACK_DAYS)
    return since.isoformat()


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

async def create_agent() -> Agent:
    """Create the Channel Pulse agent with People.ai MCP + local tools."""
    peopleai_mcp = MCPServerSse(
        name="peopleai",
        url=os.environ["PEOPLEAI_MCP_URL"],
    )

    agent = Agent(
        name="Channel Pulse",
        instructions=SYSTEM_PROMPT,
        tools=[post_to_slack, get_channel_for_account, get_lookback_date],
        mcp_servers=[peopleai_mcp],
    )
    return agent


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

async def run_channel_pulse():
    """Execute one cycle of channel pulse updates."""
    agent = await create_agent()

    result = await Runner.run(
        agent,
        """Run the Channel Pulse workflow:
1. Use get_lookback_date() to determine the activity window
2. Query People.ai MCP to find accounts with recent activity
3. For each active account:
   a. Pull detailed engagement data from People.ai
   b. Generate a scannable channel update
   c. Look up the correct Slack channel with get_channel_for_account()
   d. Post the update using post_to_slack()
4. Report how many accounts were updated""",
    )

    print(f"[{datetime.utcnow().isoformat()}] {result.final_output}")


async def main():
    while True:
        await run_channel_pulse()
        await asyncio.sleep(UPDATE_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())
