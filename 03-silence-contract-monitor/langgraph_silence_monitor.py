"""
Silence & Contract Monitor — LangGraph Implementation

Monitors accounts for engagement gaps and surfaces churn risk alerts
using People.ai MCP data and AI-powered risk assessment.

Requirements:
    pip install langgraph langchain-anthropic langchain-core

Environment variables:
    ANTHROPIC_API_KEY    — Claude API key
    SLACK_BOT_TOKEN      — Slack bot token
    PEOPLEAI_MCP_URL     — People.ai MCP server URL
"""
from __future__ import annotations

import asyncio
import os
from datetime import datetime
from typing import TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode


class SilenceMonitorState(TypedDict):
    accounts: list[dict]
    silent_accounts: list[dict]
    risk_assessments: list[dict]
    alerts: list[dict]
    delivery_results: list[str]


SILENCE_THRESHOLD_DAYS = 7

SYSTEM_PROMPT = """You are a sales intelligence assistant that monitors accounts
for concerning engagement gaps.

You have access to People.ai via MCP tools. For each silent account, assess:
- Severity (Critical 🔴, Watch 🟡, Benign 🟢) based on silence duration vs normal cadence
- Context: deal stage, contract renewal date, historical engagement patterns
- Whether silence is explainable (PTO, holidays, post-close quiet period)
- Recommended re-engagement action with specific next steps

Format alerts with emoji severity indicators. Be specific with days silent,
normal cadence, contract dates, and dollar amounts."""


async def get_peopleai_tools():
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
        client = MultiServerMCPClient({
            "peopleai": {"url": os.environ["PEOPLEAI_MCP_URL"], "transport": "sse"}
        })
        return await client.get_tools()
    except ImportError:
        return []


async def fetch_accounts(state: SilenceMonitorState) -> dict:
    """Fetch monitored accounts from People.ai."""
    tools = await get_peopleai_tools()
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)

    if tools:
        llm_with_tools = llm.bind_tools(tools)
        response = await llm_with_tools.ainvoke([
            SystemMessage(content="Retrieve all monitored accounts with their last engagement dates."),
            HumanMessage(content="Get all active accounts with engagement timestamps and deal info."),
        ])
        return {"accounts": [{"raw": response.content}]}

    return {"accounts": []}


async def detect_silence(state: SilenceMonitorState) -> dict:
    """Identify accounts that have gone silent beyond threshold."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)

    response = await llm.ainvoke([
        SystemMessage(content="Identify accounts with engagement gaps exceeding normal patterns."),
        HumanMessage(content=f"From these accounts, identify which have gone silent "
                    f"(no meaningful engagement in {SILENCE_THRESHOLD_DAYS}+ days):\n\n"
                    f"{state['accounts']}"),
    ])
    return {"silent_accounts": [{"analysis": response.content}]}


async def assess_risk(state: SilenceMonitorState) -> dict:
    """AI-powered risk assessment for each silent account."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)

    response = await llm.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Assess the risk level for these silent accounts and generate "
                    f"alerts with severity, context, and recommended actions:\n\n"
                    f"{state['silent_accounts']}"),
    ])
    return {"risk_assessments": [{"report": response.content}],
            "alerts": [{"content": response.content}]}


async def deliver_alerts(state: SilenceMonitorState) -> dict:
    """Deliver silence alerts via Slack."""
    from slack_sdk.web.async_client import AsyncWebClient

    client = AsyncWebClient(token=os.environ["SLACK_BOT_TOKEN"])
    channel = os.environ.get("ALERT_SLACK_CHANNEL", "")
    results = []

    for alert in state.get("alerts", []):
        if channel and alert.get("content"):
            result = await client.chat_postMessage(
                channel=channel, text=alert["content"], unfurl_links=False,
            )
            results.append(f"Alert posted: {result['ts']}")

    return {"delivery_results": results}


def build_graph():
    graph = StateGraph(SilenceMonitorState)
    graph.add_node("fetch_accounts", fetch_accounts)
    graph.add_node("detect_silence", detect_silence)
    graph.add_node("assess_risk", assess_risk)
    graph.add_node("deliver_alerts", deliver_alerts)

    graph.set_entry_point("fetch_accounts")
    graph.add_edge("fetch_accounts", "detect_silence")
    graph.add_edge("detect_silence", "assess_risk")
    graph.add_edge("assess_risk", "deliver_alerts")
    graph.add_edge("deliver_alerts", END)

    return graph.compile()


async def main():
    app = build_graph()
    result = await app.ainvoke({
        "accounts": [], "silent_accounts": [], "risk_assessments": [],
        "alerts": [], "delivery_results": [],
    })
    print(f"[{datetime.utcnow().isoformat()}] Alerts: {len(result.get('delivery_results', []))}")


if __name__ == "__main__":
    asyncio.run(main())
