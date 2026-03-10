"""
Forecast Coach — Claude Agent SDK Implementation

Provides AI-powered coaching insights for sales leaders by analyzing
their team's open pipeline each week.

Requirements:
    pip install claude-agent-sdk anthropic

Environment variables:
    ANTHROPIC_API_KEY    — Claude API key
    PEOPLEAI_MCP_URL     — People.ai MCP server URL
    SMTP_HOST            — SMTP server
    SMTP_USER            — SMTP username
    SMTP_PASS            — SMTP password
"""
from __future__ import annotations

import asyncio
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import anthropic
from claude_agent_sdk import Agent, tool

SYSTEM_PROMPT = """You are an AI sales coaching assistant that helps sales leaders
improve their team's pipeline execution.

You have access to People.ai via MCP tools to pull pipeline and engagement data,
and local tools to deliver coaching reports via email.

For each leader's team, analyze every open deal across:
- Engagement recency, stakeholder coverage, stage velocity
- Competitive signals, risk indicators (pushed dates, stalled stages)

Generate a coaching report with:
- PIPELINE SUMMARY (total value, forecast, best case)
- NEEDS ATTENTION (🔴) with coaching conversation starters
- MONITOR (🟡) with emerging risks
- ON TRACK (🟢) summary count

Each flagged deal gets a "💬 Coach:" line with what to ask the rep.
Be specific with deal names, amounts, rep names, dates."""


@tool
def send_coaching_email(recipient: str, report: str) -> str:
    """Send a coaching report via email.

    Args:
        recipient: Email address of the sales leader.
        report: Formatted coaching report content.
    """
    msg = MIMEText(report)
    msg["Subject"] = f"Weekly Forecast Coaching — {datetime.utcnow().strftime('%b %d, %Y')}"
    msg["From"] = os.environ.get("SMTP_USER", "")
    msg["To"] = recipient

    with smtplib.SMTP(os.environ["SMTP_HOST"], 587) as server:
        server.starttls()
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        server.send_message(msg)
    return f"Coaching report sent to {recipient}"


def create_agent() -> Agent:
    client = anthropic.Anthropic()
    return Agent(
        client=client,
        model="claude-sonnet-4-20250514",
        system=SYSTEM_PROMPT,
        tools=[send_coaching_email],
        mcp_servers=[
            {"name": "peopleai", "url": os.environ["PEOPLEAI_MCP_URL"]}
        ],
    )


async def run_forecast_coach():
    agent = create_agent()

    result = await agent.run(
        """Run the Forecast Coach workflow:
1. Query People.ai MCP for all sales leaders and their team assignments
2. For each leader:
   a. Pull their team's open pipeline (active deals only)
   b. For each deal, assess health across dimensions:
      - Engagement recency (last meaningful contact)
      - Stakeholder coverage (single vs multi-threaded)
      - Stage velocity (on pace or stalled?)
      - Competitive signals
      - Risk indicators (pushed dates, champion changes)
   c. Generate a coaching report with:
      - Pipeline summary (total, commit, best case)
      - Needs Attention deals with coaching conversation starters
      - Monitor deals with emerging risks
      - On Track count
   d. Send via send_coaching_email() to the leader
3. Report how many coaching reports were delivered"""
    )
    print(f"[{datetime.utcnow().isoformat()}] {result}")


if __name__ == "__main__":
    asyncio.run(run_forecast_coach())
