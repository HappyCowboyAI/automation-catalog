"""
Forecast Coach — OpenAI Agents SDK Implementation

Provides AI-powered coaching insights for sales leaders by analyzing
their team's open pipeline each week.

Requirements:
    pip install openai-agents

Environment variables:
    OPENAI_API_KEY       — OpenAI API key
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

from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerSse

SYSTEM_PROMPT = """You are an AI sales coaching assistant that helps sales leaders
improve their team's pipeline execution.

You have access to People.ai via MCP tools and local email delivery.

Analyze each deal across: engagement recency, stakeholder coverage, stage velocity,
competitive signals, risk indicators.

Generate coaching reports with pipeline summary, needs attention (🔴),
monitor (🟡), on track (🟢), and specific coaching conversation starters.

Be specific with deal names, amounts, rep names, dates."""


@function_tool
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


async def create_agent() -> Agent:
    peopleai_mcp = MCPServerSse(
        name="peopleai", url=os.environ["PEOPLEAI_MCP_URL"],
    )
    return Agent(
        name="Forecast Coach",
        instructions=SYSTEM_PROMPT,
        tools=[send_coaching_email],
        mcp_servers=[peopleai_mcp],
    )


async def run_forecast_coach():
    agent = await create_agent()

    result = await Runner.run(
        agent,
        """Run the Forecast Coach workflow:
1. Query People.ai MCP for sales leaders and team assignments
2. For each leader:
   a. Pull team's open pipeline (active deals)
   b. Assess each deal: engagement, stakeholders, velocity, competition, risks
   c. Generate coaching report with pipeline summary and prioritized actions
   d. Send via send_coaching_email()
3. Report coaching reports delivered""",
    )
    print(f"[{datetime.utcnow().isoformat()}] {result.final_output}")


if __name__ == "__main__":
    asyncio.run(run_forecast_coach())
