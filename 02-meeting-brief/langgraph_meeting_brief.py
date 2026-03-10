"""
Meeting Brief — LangGraph Implementation

Generates AI-powered meeting briefings by pulling account context from
People.ai via MCP and delivering to the meeting owner before each call.

Requirements:
    pip install langgraph langchain-anthropic langchain-core

Environment variables:
    ANTHROPIC_API_KEY    — Claude API key
    SLACK_BOT_TOKEN      — Slack bot token
    PEOPLEAI_MCP_URL     — People.ai MCP server URL
    CALENDAR_API_URL     — Calendar API endpoint (Google, Outlook)
"""
from __future__ import annotations

import asyncio
import os
from datetime import datetime, timedelta
from typing import TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

class MeetingBriefState(TypedDict):
    meetings: list[dict]          # upcoming meetings from calendar
    current_meeting: dict         # meeting being processed
    account_context: dict         # People.ai data for the account
    brief: str                    # generated brief
    delivery_results: list[str]   # delivery confirmations

# ---------------------------------------------------------------------------
# MCP Adapter
# ---------------------------------------------------------------------------

async def get_peopleai_tools():
    """Load People.ai MCP tools via adapter."""
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
        client = MultiServerMCPClient({
            "peopleai": {
                "url": os.environ["PEOPLEAI_MCP_URL"],
                "transport": "sse",
            }
        })
        return await client.get_tools()
    except ImportError:
        return []

# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a sales intelligence assistant that generates
pre-meeting briefing documents for sales reps.

You have access to People.ai via MCP tools. For each meeting, generate:
- Meeting header (account, time, type)
- ATTENDEES section with roles, history, and new attendees flagged
- ACCOUNT CONTEXT with deal info, recent activity, competitor intel
- TALKING POINTS (3-5 prioritized items based on context)
- WATCH FOR section with risks or items needing attention
- Footer with engagement history depth

Be specific with names, amounts, dates. Use emoji section headers."""


async def check_calendar(state: MeetingBriefState) -> dict:
    """Check calendar for meetings in the next 30 minutes."""
    # In production, this calls Google Calendar or Outlook API
    # For now, returns meetings passed in or fetched from calendar API
    import json
    from urllib.request import Request, urlopen

    calendar_url = os.environ.get("CALENDAR_API_URL", "")
    if calendar_url:
        now = datetime.utcnow()
        window_end = now + timedelta(minutes=30)
        req = Request(f"{calendar_url}/events?timeMin={now.isoformat()}&timeMax={window_end.isoformat()}")
        with urlopen(req) as resp:
            meetings = json.loads(resp.read())
    else:
        meetings = state.get("meetings", [])

    return {"meetings": meetings}


async def fetch_meeting_context(state: MeetingBriefState) -> dict:
    """Fetch account context from People.ai for the current meeting."""
    meeting = state["meetings"][0] if state["meetings"] else {}
    tools = await get_peopleai_tools()
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)

    if tools:
        llm_with_tools = llm.bind_tools(tools)
        account_name = meeting.get("account", "Unknown")
        response = await llm_with_tools.ainvoke([
            SystemMessage(content="Extract account context for a meeting brief."),
            HumanMessage(content=f"Get recent activity, engagement history, key contacts, "
                        f"and deal status for account: {account_name}"),
        ])
        return {"current_meeting": meeting, "account_context": {"raw": response.content}}

    return {"current_meeting": meeting, "account_context": {}}


async def generate_brief(state: MeetingBriefState) -> dict:
    """Generate the meeting brief using LLM."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)
    meeting = state["current_meeting"]
    context = state["account_context"]

    response = await llm.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Generate a meeting brief.\n\n"
                    f"Meeting: {meeting}\n\n"
                    f"Account Context: {context}"),
    ])
    return {"brief": response.content}


async def deliver_brief(state: MeetingBriefState) -> dict:
    """Deliver the brief via Slack DM to the meeting owner."""
    from slack_sdk.web.async_client import AsyncWebClient

    client = AsyncWebClient(token=os.environ["SLACK_BOT_TOKEN"])
    owner_id = state["current_meeting"].get("owner_slack_id", "")

    if owner_id and state["brief"]:
        result = await client.chat_postMessage(
            channel=owner_id,
            text=state["brief"],
            unfurl_links=False,
        )
        return {"delivery_results": [f"Delivered to {owner_id}: {result['ts']}"]}

    return {"delivery_results": ["No delivery — missing owner or brief"]}


def should_continue(state: MeetingBriefState) -> str:
    """Check if there are more meetings to process."""
    if len(state.get("meetings", [])) > 1:
        return "fetch_meeting_context"
    return END

# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------

def build_graph():
    graph = StateGraph(MeetingBriefState)

    graph.add_node("check_calendar", check_calendar)
    graph.add_node("fetch_meeting_context", fetch_meeting_context)
    graph.add_node("generate_brief", generate_brief)
    graph.add_node("deliver_brief", deliver_brief)

    graph.set_entry_point("check_calendar")
    graph.add_edge("check_calendar", "fetch_meeting_context")
    graph.add_edge("fetch_meeting_context", "generate_brief")
    graph.add_edge("generate_brief", "deliver_brief")
    graph.add_conditional_edges("deliver_brief", should_continue)

    return graph.compile()


async def main():
    app = build_graph()
    result = await app.ainvoke({"meetings": [], "delivery_results": []})
    print(f"[{datetime.utcnow().isoformat()}] Briefs delivered: {len(result.get('delivery_results', []))}")


if __name__ == "__main__":
    asyncio.run(main())
