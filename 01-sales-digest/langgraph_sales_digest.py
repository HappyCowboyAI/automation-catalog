"""
Sales Digest — LangGraph Implementation

Generates a personalized daily sales digest for each enrolled user by
pulling account activity from People.ai via MCP and summarizing with an LLM.

Requirements:
    pip install langgraph langchain-anthropic langchain-mcp-adapters slack-sdk

Environment variables:
    ANTHROPIC_API_KEY    — Claude API key
    SLACK_BOT_TOKEN      — Slack bot token for delivering digests
    PEOPLEAI_MCP_URL     — People.ai MCP server URL
    SUBSCRIBER_STORE     — Path to JSON subscriber list (or DB connection)
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated, TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCHEDULE_HOUR = 6  # 6 AM
WEEKDAYS_ONLY = True

SYSTEM_PROMPT = """You are a sales intelligence assistant generating a
personalized daily digest for a sales rep. Given raw account activity data
from People.ai, produce a concise morning briefing.

Format:
- Greeting with rep name and date
- Section 1: PIPELINE MOVEMENT (3-5 bullets on deal stage changes, new activity)
- Section 2: ENGAGEMENT HIGHLIGHTS (3-5 bullets on notable contact interactions)
- Section 3: RECOMMENDED ACTIONS (3-5 prioritized action items)
- Footer with account count summary

Use emoji section headers. Be specific with names, dollar amounts, dates.
Personalize to the rep — reference their deals and contacts by name."""


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

class SalesDigestState(TypedDict):
    messages: Annotated[list, add_messages]
    subscribers: list[dict]
    current_user: dict | None
    account_activity: str
    digest: str


# ---------------------------------------------------------------------------
# Subscriber Store
# ---------------------------------------------------------------------------

def load_subscribers() -> list[dict]:
    """Load digest subscribers from config store.

    Default: JSON file. Replace with DB query for production.
    Expected format: [{"name": "Sarah Chen", "slack_id": "U123", "accounts": [...]}]
    """
    store_path = os.environ.get("SUBSCRIBER_STORE", "subscribers.json")
    path = Path(store_path)
    if path.exists():
        return json.loads(path.read_text())
    return []


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------

async def fetch_subscribers(state: SalesDigestState) -> dict:
    """Read the subscriber list from the config store."""
    subscribers = load_subscribers()
    return {"subscribers": subscribers}


async def gather_account_activity(state: SalesDigestState) -> dict:
    """For the current user, pull overnight account activity from People.ai."""
    user = state["subscribers"][0]
    since = (datetime.utcnow() - timedelta(days=1)).isoformat()

    async with MultiServerMCPClient(
        {"peopleai": {"url": os.environ["PEOPLEAI_MCP_URL"]}}
    ) as mcp:
        tools = mcp.get_tools()

        # Pull activity for each of the user's accounts
        all_activity = []
        for account_name in user.get("accounts", []):
            activity = await tools[
                "peopleai__get_recent_account_activity"
            ].ainvoke({"account_name": account_name, "since": since})
            all_activity.append(
                f"Account: {account_name}\n{activity}"
            )

    return {
        "current_user": user,
        "account_activity": "\n\n---\n\n".join(all_activity),
        "subscribers": state["subscribers"][1:],  # pop processed
    }


async def ai_summarization(state: SalesDigestState) -> dict:
    """Use Claude to compose the personalized digest."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", max_tokens=1024)
    user = state["current_user"]

    response = await llm.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""Rep: {user['name']}
Date: {datetime.utcnow().strftime('%A, %b %d')}

Raw account activity from People.ai:
{state['account_activity']}

Generate the personalized daily digest."""),
    ])

    return {"digest": response.content}


async def deliver_digest(state: SalesDigestState) -> dict:
    """Send the formatted digest to the user via Slack."""
    from slack_sdk.web.async_client import AsyncWebClient

    client = AsyncWebClient(token=os.environ["SLACK_BOT_TOKEN"])
    user = state["current_user"]

    if user.get("slack_id"):
        await client.chat_postMessage(
            channel=user["slack_id"],
            text=state["digest"],
            unfurl_links=False,
        )
    return {}


def should_continue(state: SalesDigestState) -> str:
    """Check if there are more subscribers to process."""
    if state["subscribers"]:
        return "gather_activity"
    return END


# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------

def build_graph() -> StateGraph:
    graph = StateGraph(SalesDigestState)

    graph.add_node("fetch_subscribers", fetch_subscribers)
    graph.add_node("gather_activity", gather_account_activity)
    graph.add_node("summarize", ai_summarization)
    graph.add_node("deliver", deliver_digest)

    graph.set_entry_point("fetch_subscribers")
    graph.add_edge("fetch_subscribers", "gather_activity")
    graph.add_edge("gather_activity", "summarize")
    graph.add_edge("summarize", "deliver")
    graph.add_conditional_edges("deliver", should_continue)

    return graph.compile()


# ---------------------------------------------------------------------------
# Runner (schedule externally via cron, or use built-in loop)
# ---------------------------------------------------------------------------

async def run_digest():
    """Execute one digest cycle for all subscribers."""
    now = datetime.utcnow()
    if WEEKDAYS_ONLY and now.weekday() >= 5:
        print(f"[{now.isoformat()}] Weekend — skipping digest")
        return

    app = build_graph()
    result = await app.ainvoke({"messages": [], "subscribers": []})
    print(f"[{now.isoformat()}] Digest cycle complete")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_digest())
