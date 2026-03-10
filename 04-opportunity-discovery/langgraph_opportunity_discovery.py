"""
Opportunity Discovery — LangGraph Implementation

Surfaces hidden revenue opportunities by cross-referencing engagement
signals from People.ai against the CRM pipeline.

Requirements:
    pip install langgraph langchain-anthropic langchain-core

Environment variables:
    ANTHROPIC_API_KEY    — Claude API key
    SLACK_BOT_TOKEN      — Slack bot token
    PEOPLEAI_MCP_URL     — People.ai MCP server URL
    SMTP_HOST            — SMTP server for email delivery
    SMTP_USER            — SMTP username
    SMTP_PASS            — SMTP password
"""
from __future__ import annotations

import asyncio
import os
from datetime import datetime
from typing import TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph


class OpportunityDiscoveryState(TypedDict):
    active_accounts: list[dict]
    open_opportunities: list[dict]
    unmatched_accounts: list[dict]
    signal_analysis: list[dict]
    report: str
    delivery_results: list[str]


SYSTEM_PROMPT = """You are a sales intelligence assistant that discovers hidden
revenue opportunities.

You have access to People.ai via MCP tools. Your job is to find accounts with
strong engagement signals but no corresponding open opportunity in the pipeline.

For each discovered opportunity, provide:
- Account name and signal strength (High 🟢, Moderate 🟡)
- Evidence: meeting count, email activity, content engagement, contact seniority
- Context: prior relationship, ICP fit, competitive landscape
- Recommended action with specific next steps
- Estimated deal size based on signals and account profile

Group by confidence level. Be specific with numbers, names, and timeframes."""


async def get_peopleai_tools():
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
        client = MultiServerMCPClient({
            "peopleai": {"url": os.environ["PEOPLEAI_MCP_URL"], "transport": "sse"}
        })
        return await client.get_tools()
    except ImportError:
        return []


async def gather_data(state: OpportunityDiscoveryState) -> dict:
    """Fetch activity data and pipeline from People.ai."""
    tools = await get_peopleai_tools()
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)

    if tools:
        llm_with_tools = llm.bind_tools(tools)
        response = await llm_with_tools.ainvoke([
            SystemMessage(content="Retrieve account engagement data and open pipeline."),
            HumanMessage(content="Get all accounts with recent engagement activity in the "
                        "last 30 days, and separately get all open opportunities in the pipeline."),
        ])
        return {
            "active_accounts": [{"raw": response.content}],
            "open_opportunities": [],
        }
    return {"active_accounts": [], "open_opportunities": []}


async def identify_gaps(state: OpportunityDiscoveryState) -> dict:
    """Cross-reference activity against pipeline to find unmatched accounts."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)

    response = await llm.ainvoke([
        SystemMessage(content="Identify accounts with engagement but no open opportunity."),
        HumanMessage(content=f"Cross-reference these active accounts against the pipeline.\n\n"
                    f"Active accounts: {state['active_accounts']}\n\n"
                    f"Open opportunities: {state['open_opportunities']}\n\n"
                    f"List accounts with engagement signals but no open deal."),
    ])
    return {"unmatched_accounts": [{"analysis": response.content}]}


async def analyze_signals(state: OpportunityDiscoveryState) -> dict:
    """AI analysis of signal strength for each unmatched account."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)

    response = await llm.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Analyze these unmatched accounts and score opportunity "
                    f"likelihood. Generate a prioritized discovery report:\n\n"
                    f"{state['unmatched_accounts']}"),
    ])
    return {
        "signal_analysis": [{"report": response.content}],
        "report": response.content,
    }


async def deliver_report(state: OpportunityDiscoveryState) -> dict:
    """Deliver discovery report via Slack and email."""
    results = []

    # Slack delivery
    try:
        from slack_sdk.web.async_client import AsyncWebClient
        client = AsyncWebClient(token=os.environ["SLACK_BOT_TOKEN"])
        channel = os.environ.get("DISCOVERY_SLACK_CHANNEL", "")
        if channel and state["report"]:
            result = await client.chat_postMessage(
                channel=channel, text=state["report"], unfurl_links=False,
            )
            results.append(f"Slack: {result['ts']}")
    except Exception as e:
        results.append(f"Slack error: {e}")

    # Email delivery
    try:
        import smtplib
        from email.mime.text import MIMEText

        recipients = os.environ.get("DISCOVERY_EMAIL_RECIPIENTS", "").split(",")
        if recipients[0] and state["report"]:
            msg = MIMEText(state["report"])
            msg["Subject"] = f"Weekly Opportunity Discovery — {datetime.utcnow().strftime('%b %d')}"
            msg["From"] = os.environ.get("SMTP_USER", "")
            msg["To"] = ", ".join(recipients)

            with smtplib.SMTP(os.environ["SMTP_HOST"], 587) as server:
                server.starttls()
                server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
                server.send_message(msg)
            results.append(f"Email: sent to {len(recipients)} recipients")
    except Exception as e:
        results.append(f"Email error: {e}")

    return {"delivery_results": results}


def build_graph():
    graph = StateGraph(OpportunityDiscoveryState)
    graph.add_node("gather_data", gather_data)
    graph.add_node("identify_gaps", identify_gaps)
    graph.add_node("analyze_signals", analyze_signals)
    graph.add_node("deliver_report", deliver_report)

    graph.set_entry_point("gather_data")
    graph.add_edge("gather_data", "identify_gaps")
    graph.add_edge("identify_gaps", "analyze_signals")
    graph.add_edge("analyze_signals", "deliver_report")
    graph.add_edge("deliver_report", END)

    return graph.compile()


async def main():
    app = build_graph()
    result = await app.ainvoke({
        "active_accounts": [], "open_opportunities": [],
        "unmatched_accounts": [], "signal_analysis": [],
        "report": "", "delivery_results": [],
    })
    print(f"[{datetime.utcnow().isoformat()}] {result.get('delivery_results', [])}")


if __name__ == "__main__":
    asyncio.run(main())
