"""
Opportunity Discovery — Claude Agent SDK Implementation

Surfaces hidden revenue opportunities by cross-referencing engagement
signals from People.ai against the CRM pipeline.

Requirements:
    pip install claude-agent-sdk anthropic slack-sdk

Environment variables:
    ANTHROPIC_API_KEY    — Claude API key
    SLACK_BOT_TOKEN      — Slack bot token
    PEOPLEAI_MCP_URL     — People.ai MCP server URL
    DISCOVERY_SLACK_CHANNEL — Slack channel for discovery results
"""
from __future__ import annotations

import asyncio
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import anthropic
from claude_agent_sdk import Agent, tool

SYSTEM_PROMPT = """You are a sales intelligence assistant that discovers hidden
revenue opportunities.

You have access to People.ai via MCP tools to pull engagement data and pipeline
info, and local tools to deliver results.

Your workflow:
1. Query People.ai for accounts with recent engagement activity (last 30 days)
2. Query People.ai for all open opportunities in the pipeline
3. Cross-reference to find accounts with engagement but no open deal
4. For each gap, analyze signal strength and recommend action
5. Generate a prioritized report grouped by confidence (High/Moderate)
6. Deliver via Slack and email

Be specific with meeting counts, contact seniority, engagement recency,
estimated deal sizes, and recommended next steps."""


@tool
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


@tool
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


def create_agent() -> Agent:
    client = anthropic.Anthropic()
    return Agent(
        client=client,
        model="claude-sonnet-4-20250514",
        system=SYSTEM_PROMPT,
        tools=[post_to_slack, send_email],
        mcp_servers=[
            {"name": "peopleai", "url": os.environ["PEOPLEAI_MCP_URL"]}
        ],
    )


async def run_opportunity_discovery():
    agent = create_agent()
    slack_channel = os.environ.get("DISCOVERY_SLACK_CHANNEL", "")
    email_recipients = os.environ.get("DISCOVERY_EMAIL_RECIPIENTS", "")

    result = await agent.run(
        f"""Run the Opportunity Discovery workflow:
1. Query People.ai MCP for all accounts with engagement activity in the last 30 days
2. Query People.ai MCP for all open opportunities in the pipeline
3. Cross-reference: find accounts with engagement signals but no open opportunity
4. For each unmatched account, analyze:
   - Signal strength (meeting count, email activity, content downloads, contact seniority)
   - Prior relationship (churned customer? net new?)
   - ICP fit
5. Generate a prioritized report grouped by confidence (High 🟢 / Moderate 🟡)
6. Post to Slack via post_to_slack(channel='{slack_channel}', ...)
7. Send via email to '{email_recipients}' with subject 'Weekly Opportunity Discovery'
8. Report total accounts scanned and opportunities surfaced"""
    )
    print(f"[{datetime.utcnow().isoformat()}] {result}")


if __name__ == "__main__":
    asyncio.run(run_opportunity_discovery())
