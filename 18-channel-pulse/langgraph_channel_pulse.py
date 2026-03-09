"""
Channel Pulse — LangGraph Implementation

Sends scannable account updates to internal customer channels by pulling
engagement data from People.ai via MCP and summarizing with an LLM.

Requirements:
    pip install langgraph langchain-anthropic langchain-mcp-adapters slack-sdk

Environment variables:
    ANTHROPIC_API_KEY    — Claude API key
    SLACK_BOT_TOKEN      — Slack bot token for posting updates
    PEOPLEAI_MCP_URL     — People.ai MCP server URL
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Annotated, TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LOOKBACK_DAYS = 7
UPDATE_INTERVAL_SECONDS = 60
CHANNEL_MAP: dict[str, str] = {
    # account_name -> slack_channel_id
    # Configure per deployment
}

SYSTEM_PROMPT = """You are a sales intelligence assistant. Given raw account
activity data from People.ai, produce a concise, scannable channel update.

Format:
- Lead with account name, deal value, close date, and health indicator
- Section 1: THIS WEEK'S KEY DEVELOPMENTS (3-5 bullets)
- Section 2: RISKS & OPPORTUNITIES (3-5 bullets)
- Section 3: NEXT WEEK'S ACTIONS (3-5 bullets with @owner tags)
- Footer: "Powered by People.ai MCP: please thread comments"

Use emoji section headers. Keep each bullet to one line. Be specific with
names, dates, and numbers — no vague summaries."""


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

class ChannelPulseState(TypedDict):
    messages: Annotated[list, add_messages]
    active_accounts: list[dict]
    current_account: dict | None
    account_context: str
    summary: str
    channel_id: str


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------

async def identify_active_accounts(state: ChannelPulseState) -> dict:
    """Query People.ai MCP for accounts with recent activity."""
    since = (datetime.utcnow() - timedelta(days=LOOKBACK_DAYS)).isoformat()

    async with MultiServerMCPClient(
        {"peopleai": {"url": os.environ["PEOPLEAI_MCP_URL"]}}
    ) as mcp:
        tools = mcp.get_tools()
        # Use the account activity tool to find active accounts
        result = await tools["peopleai__get_recent_account_activity"].ainvoke(
            {"since": since}
        )
        accounts = result if isinstance(result, list) else []

    return {"active_accounts": accounts}


async def gather_account_context(state: ChannelPulseState) -> dict:
    """For the current account, pull detailed engagement data from People.ai."""
    account = state["active_accounts"][0]  # process one at a time

    async with MultiServerMCPClient(
        {"peopleai": {"url": os.environ["PEOPLEAI_MCP_URL"]}}
    ) as mcp:
        tools = mcp.get_tools()
        context = await tools["peopleai__ask_sales_ai_about_account"].ainvoke(
            {"account_name": account["name"]}
        )

    return {
        "current_account": account,
        "account_context": str(context),
        "active_accounts": state["active_accounts"][1:],  # pop processed
    }


async def ai_summarization(state: ChannelPulseState) -> dict:
    """Use Claude to synthesize raw activity into a scannable update."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", max_tokens=1024)

    response = await llm.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""Account: {state['current_account']['name']}
Raw activity data:
{state['account_context']}

Generate the channel update."""),
    ])

    return {"summary": response.content}


async def route_to_channel(state: ChannelPulseState) -> dict:
    """Determine the correct Slack channel for this account."""
    account_name = state["current_account"]["name"]
    channel_id = CHANNEL_MAP.get(account_name, os.environ.get("DEFAULT_CHANNEL", ""))
    return {"channel_id": channel_id}


async def deliver_update(state: ChannelPulseState) -> dict:
    """Post the formatted update to Slack."""
    from slack_sdk.web.async_client import AsyncWebClient

    client = AsyncWebClient(token=os.environ["SLACK_BOT_TOKEN"])
    if state["channel_id"]:
        await client.chat_postMessage(
            channel=state["channel_id"],
            text=state["summary"],
            unfurl_links=False,
        )
    return {}


def should_continue(state: ChannelPulseState) -> str:
    """Check if there are more accounts to process."""
    if state["active_accounts"]:
        return "gather_context"
    return END


# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------

def build_graph() -> StateGraph:
    graph = StateGraph(ChannelPulseState)

    graph.add_node("identify_accounts", identify_active_accounts)
    graph.add_node("gather_context", gather_account_context)
    graph.add_node("summarize", ai_summarization)
    graph.add_node("route", route_to_channel)
    graph.add_node("deliver", deliver_update)

    graph.set_entry_point("identify_accounts")
    graph.add_edge("identify_accounts", "gather_context")
    graph.add_edge("gather_context", "summarize")
    graph.add_edge("summarize", "route")
    graph.add_edge("route", "deliver")
    graph.add_conditional_edges("deliver", should_continue)

    return graph.compile()


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

async def main():
    import asyncio

    app = build_graph()
    while True:
        result = await app.ainvoke({"messages": [], "active_accounts": []})
        print(f"[{datetime.utcnow().isoformat()}] Processed accounts")
        await asyncio.sleep(UPDATE_INTERVAL_SECONDS)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
