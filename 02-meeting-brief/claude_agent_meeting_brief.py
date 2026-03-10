"""
Meeting Brief — Claude Agent SDK Implementation

Generates AI-powered meeting briefings by pulling account context from
People.ai via MCP and delivering to the meeting owner before each call.

Requirements:
    pip install claude-agent-sdk anthropic slack-sdk

Environment variables:
    ANTHROPIC_API_KEY    — Claude API key
    SLACK_BOT_TOKEN      — Slack bot token
    PEOPLEAI_MCP_URL     — People.ai MCP server URL
    CALENDAR_API_URL     — Calendar API endpoint
"""
from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime, timedelta
from urllib.request import Request, urlopen

import anthropic
from claude_agent_sdk import Agent, tool

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a sales intelligence assistant that generates
pre-meeting briefing documents for sales reps.

You have access to People.ai via MCP tools to pull account context, and
local tools to check calendars and deliver briefs.

For each upcoming meeting, generate a brief with:
- Meeting header (account, time, type)
- ATTENDEES with roles, history, new attendees flagged
- ACCOUNT CONTEXT with deal info, recent activity, competitor intel
- TALKING POINTS (3-5 prioritized)
- WATCH FOR section with risks
- Footer with engagement history depth

Use emoji section headers. Be specific with names, amounts, dates."""


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@tool
def get_upcoming_meetings(minutes_ahead: int = 30) -> list[dict]:
    """Check calendar for meetings starting within the given window.

    Args:
        minutes_ahead: Number of minutes to look ahead (default 30).
    """
    calendar_url = os.environ.get("CALENDAR_API_URL", "")
    if not calendar_url:
        return []

    now = datetime.utcnow()
    window_end = now + timedelta(minutes=minutes_ahead)
    req = Request(
        f"{calendar_url}/events?timeMin={now.isoformat()}&timeMax={window_end.isoformat()}"
    )
    with urlopen(req) as resp:
        return json.loads(resp.read())


@tool
async def send_slack_dm(slack_user_id: str, message: str) -> str:
    """Send a direct message to a Slack user.

    Args:
        slack_user_id: The Slack user ID to message.
        message: The formatted brief content.
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

def create_agent() -> Agent:
    """Create the Meeting Brief agent with People.ai MCP + local tools."""
    client = anthropic.Anthropic()

    agent = Agent(
        client=client,
        model="claude-sonnet-4-20250514",
        system=SYSTEM_PROMPT,
        tools=[get_upcoming_meetings, send_slack_dm],
        mcp_servers=[
            {
                "name": "peopleai",
                "url": os.environ["PEOPLEAI_MCP_URL"],
            }
        ],
    )
    return agent


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

async def run_meeting_brief():
    """Execute the meeting brief workflow."""
    agent = create_agent()

    result = await agent.run(
        """Run the Meeting Brief workflow:
1. Check get_upcoming_meetings() for meetings in the next 30 minutes
2. For each meeting:
   a. Identify the account associated with the meeting
   b. Query People.ai MCP for account context (recent activity, engagement, contacts, deals)
   c. Generate a structured meeting brief
   d. Deliver via send_slack_dm() to the meeting owner
3. Report how many briefs were delivered"""
    )

    print(f"[{datetime.utcnow().isoformat()}] {result}")


if __name__ == "__main__":
    asyncio.run(run_meeting_brief())
