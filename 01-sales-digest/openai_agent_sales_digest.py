"""
Sales Digest — OpenAI Agents SDK Implementation

Generates a personalized daily sales digest for each enrolled user by
pulling account activity from People.ai via MCP and summarizing with an LLM.

Requirements:
    pip install openai-agents slack-sdk

Environment variables:
    OPENAI_API_KEY       — OpenAI API key
    SLACK_BOT_TOKEN      — Slack bot token for delivering digests
    PEOPLEAI_MCP_URL     — People.ai MCP server URL
    SUBSCRIBER_STORE     — Path to JSON subscriber list (or DB connection)
"""
from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerSse

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WEEKDAYS_ONLY = True

SYSTEM_PROMPT = """You are a sales intelligence assistant that generates
personalized daily digests for sales reps.

You have access to People.ai via MCP tools to pull account activity data,
and local tools to manage subscribers and deliver messages.

For each subscriber, generate a digest in this format:
- Greeting with rep name and today's date
- Section 1: PIPELINE MOVEMENT (3-5 bullets on deal changes)
- Section 2: ENGAGEMENT HIGHLIGHTS (3-5 notable interactions)
- Section 3: RECOMMENDED ACTIONS (3-5 prioritized items)
- Footer with account count summary

Use emoji section headers. Be specific with names, amounts, dates."""


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@function_tool
def get_subscribers() -> list[dict]:
    """Retrieve the list of digest subscribers from the config store.

    Returns a list of subscriber objects with name, slack_id, and accounts.
    """
    store_path = os.environ.get("SUBSCRIBER_STORE", "subscribers.json")
    path = Path(store_path)
    if path.exists():
        return json.loads(path.read_text())
    return []


@function_tool
def get_today_info() -> dict:
    """Get today's date info and whether digests should run."""
    now = datetime.utcnow()
    return {
        "date": now.strftime("%A, %b %d"),
        "is_weekday": now.weekday() < 5,
        "should_run": not WEEKDAYS_ONLY or now.weekday() < 5,
    }


@function_tool
async def send_slack_dm(slack_user_id: str, message: str) -> str:
    """Send a direct message to a Slack user.

    Args:
        slack_user_id: The Slack user ID to message.
        message: The formatted digest content.
    """
    from slack_sdk.web.async_client import AsyncWebClient

    client = AsyncWebClient(token=os.environ["SLACK_BOT_TOKEN"])
    result = await client.chat_postMessage(
        channel=slack_user_id,
        text=message,
        unfurl_links=False,
    )
    return f"Delivered to {slack_user_id}: {result['ts']}"


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

async def create_agent() -> Agent:
    """Create the Sales Digest agent with People.ai MCP + local tools."""
    peopleai_mcp = MCPServerSse(
        name="peopleai",
        url=os.environ["PEOPLEAI_MCP_URL"],
    )

    agent = Agent(
        name="Sales Digest",
        instructions=SYSTEM_PROMPT,
        tools=[get_subscribers, get_today_info, send_slack_dm],
        mcp_servers=[peopleai_mcp],
    )
    return agent


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

async def run_digest():
    """Execute the daily sales digest workflow."""
    agent = await create_agent()

    result = await Runner.run(
        agent,
        """Run the Sales Digest workflow:
1. Check get_today_info() — if it's not a weekday and weekday-only is set, skip
2. Get the subscriber list using get_subscribers()
3. For each subscriber:
   a. Query People.ai MCP for recent activity on their accounts (last 24 hours)
   b. Generate a personalized daily digest
   c. Deliver via send_slack_dm() using their slack_id
4. Report how many digests were delivered""",
    )

    print(f"[{datetime.utcnow().isoformat()}] {result.final_output}")


if __name__ == "__main__":
    asyncio.run(run_digest())
