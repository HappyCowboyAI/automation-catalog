"""
Forecast Coach — LangGraph Implementation

Provides AI-powered coaching insights for sales leaders by analyzing
their team's open pipeline each week.

Requirements:
    pip install langgraph langchain-anthropic langchain-core

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
from typing import TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph


class ForecastCoachState(TypedDict):
    leaders: list[dict]
    current_leader: dict
    pipeline_data: list[dict]
    deal_assessments: list[dict]
    coaching_report: str
    delivery_results: list[str]


SYSTEM_PROMPT = """You are an AI sales coaching assistant that helps sales leaders
improve their team's pipeline execution.

You have access to People.ai via MCP tools. For each leader's team pipeline:

Analyze each deal across these dimensions:
- Engagement recency: when was last meaningful contact?
- Stakeholder coverage: single-threaded or multi-threaded?
- Stage velocity: is the deal progressing at normal pace?
- Competitive signals: any competitor activity detected?
- Risk indicators: pushed close dates, stalled stages, champion changes

Generate a coaching report with:
- PIPELINE SUMMARY with total value, forecast commit, best case
- NEEDS ATTENTION (🔴) deals with specific coaching conversation starters
- MONITOR (🟡) deals with emerging risks
- ON TRACK (🟢) summary count
- Each deal gets a "💬 Coach:" line with what to ask the rep

Be specific with deal names, amounts, rep names, and dates."""


async def get_peopleai_tools():
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
        client = MultiServerMCPClient({
            "peopleai": {"url": os.environ["PEOPLEAI_MCP_URL"], "transport": "sse"}
        })
        return await client.get_tools()
    except ImportError:
        return []


async def fetch_leaders(state: ForecastCoachState) -> dict:
    """Fetch sales leaders and their team assignments."""
    tools = await get_peopleai_tools()
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)

    if tools:
        llm_with_tools = llm.bind_tools(tools)
        response = await llm_with_tools.ainvoke([
            SystemMessage(content="Retrieve sales leader roster with team assignments."),
            HumanMessage(content="Get all sales leaders and their team members."),
        ])
        return {"leaders": [{"raw": response.content}]}
    return {"leaders": []}


async def pull_pipeline(state: ForecastCoachState) -> dict:
    """Pull pipeline data for the current leader's team."""
    tools = await get_peopleai_tools()
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)
    leader = state["leaders"][0] if state["leaders"] else {}

    if tools:
        llm_with_tools = llm.bind_tools(tools)
        response = await llm_with_tools.ainvoke([
            SystemMessage(content="Retrieve open pipeline for a sales team."),
            HumanMessage(content=f"Get all open, active opportunities for this leader's "
                        f"team: {leader}. Include deal stage, amount, close date, "
                        f"engagement metrics, and stakeholder map."),
        ])
        return {"current_leader": leader, "pipeline_data": [{"raw": response.content}]}
    return {"current_leader": leader, "pipeline_data": []}


async def assess_deals(state: ForecastCoachState) -> dict:
    """AI assessment of deal health across multiple dimensions."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)

    response = await llm.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Analyze this leader's team pipeline and generate a "
                    f"coaching report:\n\nLeader: {state['current_leader']}\n\n"
                    f"Pipeline: {state['pipeline_data']}"),
    ])
    return {
        "deal_assessments": [{"report": response.content}],
        "coaching_report": response.content,
    }


async def deliver_report(state: ForecastCoachState) -> dict:
    """Deliver coaching report via email."""
    results = []
    leader = state.get("current_leader", {})
    email = leader.get("email", os.environ.get("COACH_REPORT_EMAIL", ""))

    if email and state["coaching_report"]:
        try:
            msg = MIMEText(state["coaching_report"])
            msg["Subject"] = f"Weekly Forecast Coaching — {datetime.utcnow().strftime('%b %d, %Y')}"
            msg["From"] = os.environ.get("SMTP_USER", "")
            msg["To"] = email

            with smtplib.SMTP(os.environ["SMTP_HOST"], 587) as server:
                server.starttls()
                server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
                server.send_message(msg)
            results.append(f"Email sent to {email}")
        except Exception as e:
            results.append(f"Email error: {e}")

    return {"delivery_results": results}


def build_graph():
    graph = StateGraph(ForecastCoachState)
    graph.add_node("fetch_leaders", fetch_leaders)
    graph.add_node("pull_pipeline", pull_pipeline)
    graph.add_node("assess_deals", assess_deals)
    graph.add_node("deliver_report", deliver_report)

    graph.set_entry_point("fetch_leaders")
    graph.add_edge("fetch_leaders", "pull_pipeline")
    graph.add_edge("pull_pipeline", "assess_deals")
    graph.add_edge("assess_deals", "deliver_report")
    graph.add_edge("deliver_report", END)

    return graph.compile()


async def main():
    app = build_graph()
    result = await app.ainvoke({
        "leaders": [], "current_leader": {}, "pipeline_data": [],
        "deal_assessments": [], "coaching_report": "", "delivery_results": [],
    })
    print(f"[{datetime.utcnow().isoformat()}] {result.get('delivery_results', [])}")


if __name__ == "__main__":
    asyncio.run(main())
