"""
Silence & Contract Monitor — OpenAI Agents SDK Implementation

Monitors accounts for engagement gaps and surfaces churn risk alerts
using People.ai MCP data and AI-powered risk assessment.

Requirements:
    pip install openai-agents slack-sdk

Environment variables:
    OPENAI_API_KEY       — OpenAI API key
    SLACK_BOT_TOKEN      — Slack bot token
    PEOPLEAI_MCP_URL     — People.ai MCP server URL
    ALERT_SLACK_CHANNEL  — Slack channel for alerts
"""
from __future__ import annotations

import asyncio
import os
from datetime import datetime

from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerSse

SILENCE_THRESHOLD_DAYS = 7

SYSTEM_PROMPT = """You are a sales intelligence assistant that monitors accounts
for concerning engagement gaps.

You have access to People.ai via MCP tools to check account engagement, and
local tools to deliver alerts.

Your workflow:
1. Query People.ai for all monitored accounts and their last engagement dates
2. Identify accounts silent beyond the threshold (7+ days)
3. Assess severity: 🔴 Critical, 🟡 Watch, 🟢 Benign
4. Generate alerts with context and recommended re-engagement actions

Be specific with days silent, normal cadence, contract dates, dollar amounts."""


@function_tool
def get_silence_config() -> dict:
    """Get silence detection configuration."""
    return {
        "threshold_days": SILENCE_THRESHOLD_DAYS,
        "check_time": "6:30 AM daily",
        "severity_levels": ["critical", "watch", "benign"],
    }


@function_tool
async def post_alert(channel: str, message: str) -> str:
    """Post a silence alert to a Slack channel.

    Args:
        channel: Slack channel ID for alerts.
        message: Formatted alert content.
    """
    from slack_sdk.web.async_client import AsyncWebClient

    client = AsyncWebClient(token=os.environ["SLACK_BOT_TOKEN"])
    result = await client.chat_postMessage(
        channel=channel, text=message, unfurl_links=False,
    )
    return f"Alert posted to {channel}: {result['ts']}"


async def create_agent() -> Agent:
    peopleai_mcp = MCPServerSse(
        name="peopleai", url=os.environ["PEOPLEAI_MCP_URL"],
    )
    return Agent(
        name="Silence Monitor",
        instructions=SYSTEM_PROMPT,
        tools=[get_silence_config, post_alert],
        mcp_servers=[peopleai_mcp],
    )


async def run_silence_monitor():
    agent = await create_agent()
    alert_channel = os.environ.get("ALERT_SLACK_CHANNEL", "")

    result = await Runner.run(
        agent,
        f"""Run the Silence & Contract Monitor:
1. Get config via get_silence_config()
2. Query People.ai MCP for all monitored accounts with engagement timestamps
3. Identify accounts silent {SILENCE_THRESHOLD_DAYS}+ days
4. Assess risk severity for each (Critical/Watch/Benign)
5. Generate consolidated alert grouped by severity
6. Post via post_alert() to channel '{alert_channel}'
7. Report accounts scanned and flagged""",
    )
    print(f"[{datetime.utcnow().isoformat()}] {result.final_output}")


if __name__ == "__main__":
    asyncio.run(run_silence_monitor())
