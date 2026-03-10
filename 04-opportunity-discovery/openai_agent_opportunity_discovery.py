"""
Opportunity Discovery — OpenAI Agents SDK Implementation

Surfaces hidden revenue opportunities by cross-referencing engagement
signals from People.ai against the CRM pipeline.

Requirements:
    pip install openai-agents slack-sdk

Environment variables:
    OPENAI_API_KEY       — OpenAI API key
    SLACK_BOT_TOKEN      — Slack bot token
    PEOPLEAI_MCP_URL     — People.ai MCP server URL
    DISCOVERY_SLACK_CHANNEL — Slack channel for results
"""
from __future__ import annotations

import asyncio
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerSse

SYSTEM_PROMPT = """You are a sales intelligence assistant that discovers hidden
revenue opportunities.

You have access to People.ai via MCP tools to pull engagement data and pipeline,
and local tools to deliver results.

Find accounts with engagement signals but no open opportunity. Analyze signal
strength and recommend next steps. Group by confidence level.

Be specific with meeting counts, contact seniority, deal sizes, and actions."""


@function_tool
async def post_to_slack(channel: str, message: str) -> str:
    """Post discovery report to a Slack channel.

    Args:
        channel: Slack channel ID.
        message: Formatted discovery report.
    """
    from slack_sdk.web.async_client import AsyncWebClient
    client = AsyncWebClient(token=os.environ["SLACK_BOT_TOKEN"])
    result = await client.chat_postMessage(
        channel=channel, text=message, unfurl_links=False,
    )
    return f"Posted to {channel}: {result['ts']}"


@function_tool
def send_email(recipients: str, subject: str, body: str) -> str:
    """Send discovery report via email.

    Args:
        recipients: Comma-separated email addresses.
        subject: Email subject line.
        body: Email body content.
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.environ.get("SMTP_USER", "")
    msg["To"] = recipients

    with smtplib.SMTP(os.environ["SMTP_HOST"], 587) as server:
        server.starttls()
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        server.send_message(msg)
    return f"Email sent to {recipients}"


async def create_agent() -> Agent:
    peopleai_mcp = MCPServerSse(
        name="peopleai", url=os.environ["PEOPLEAI_MCP_URL"],
    )
    return Agent(
        name="Opportunity Discovery",
        instructions=SYSTEM_PROMPT,
        tools=[post_to_slack, send_email],
        mcp_servers=[peopleai_mcp],
    )


async def run_opportunity_discovery():
    agent = await create_agent()
    slack_channel = os.environ.get("DISCOVERY_SLACK_CHANNEL", "")
    email_recipients = os.environ.get("DISCOVERY_EMAIL_RECIPIENTS", "")

    result = await Runner.run(
        agent,
        f"""Run the Opportunity Discovery workflow:
1. Query People.ai MCP for accounts with engagement in last 30 days
2. Query People.ai MCP for all open opportunities
3. Cross-reference to find accounts with signals but no open deal
4. Analyze signal strength for each (meetings, emails, content, seniority)
5. Generate prioritized report (High 🟢 / Moderate 🟡)
6. Post to Slack channel '{slack_channel}'
7. Email to '{email_recipients}'
8. Report accounts scanned and opportunities found""",
    )
    print(f"[{datetime.utcnow().isoformat()}] {result.final_output}")


if __name__ == "__main__":
    asyncio.run(run_opportunity_discovery())
