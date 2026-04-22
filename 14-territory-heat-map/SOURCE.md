# 14 — Territory Heat Map

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 14-territory-heat-map                                |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly Monday 6:30 AM                     |
| **Node Count** | 24                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email) |

## Category
strategic-intelligence

## Description

Generates a weekly territory heat map digest for each rep, showing which accounts in their territory are heating up (increased inbound, new contacts engaging, meeting frequency rising) versus cooling down (declining engagement, unresponsive contacts). The workflow pulls Backstory engagement data across all accounts in each rep's territory, calculates week-over-week momentum scores, and uses an AI agent to summarize trends and recommend where to focus time. Delivered every Monday to help reps prioritize their week.

## Node Flow

1. **Schedule Trigger** — Fires weekly on Monday at 6:30 AM.
2. **Fetch Territory Assignments** — Pulls each rep's assigned accounts from CRM or Backstory territory data.
3. **Calculate Account Momentum** — For each account, queries Backstory for week-over-week engagement changes and calculates a momentum score (heating up / steady / cooling down).
4. **AI Territory Summary** — AI Agent analyzes the momentum map, identifies the hottest opportunities and coldest risks, and recommends a prioritized focus list for the week.
5. **Deliver Heat Map Digest** — Sends a per-rep territory digest via Messaging with accounts color-coded by momentum.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly Monday 6:30 AM trigger             |
| `mcpClientTool`       | Backstory territory engagement data       |
| `code`                | Momentum score calculation                |
| `agent`               | AI territory analysis and prioritization  |
| `lmChat`              | LLM language model                        |
| `splitInBatches`      | Iterates over reps                        |

## Credentials Required

- **Backstory MCP** — Account engagement data across territories
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI territory analysis
- **Messaging (Slack, Teams, Email)** — Delivers heat map digests to reps

## Sample Output

<!--mockup:slack-->
<!--bot:Atlas-->
<!--bot-app:true-->

🗺️ **Territory Heat Map** — @james.park | Week of Mar 3

🔥 **HEATING UP:**
- **NovaTech** ===$275,000=== | ↑↑↑ Momentum: +340%
- 5 new contacts engaged this week (was 1/week average)
- VP Product requested pricing for enterprise tier — first executive outreach
- Inbound demo request from Director of Engineering
- **Contoso Ltd** ===$150,000=== | ↑↑ Momentum: +180%
- Champion reopened evaluation after 6 weeks dormant
- Downloaded 3 technical docs + attended webinar Tuesday
- Budget cycle starting Q2 — timing aligns with buying window

➡️ **STEADY:**
- **Acme Corp** ===$425,000=== — On track, weekly cadence maintained
- **Initrode** ===$88,000=== — POC in progress, normal engagement pattern
- 6 other accounts — no significant changes

❄️ **COOLING DOWN:**
- **Globex Industries** ===$180,000=== | ↓↓ Momentum: -65%
- Champion response time went from <1hr to 3+ days this week
- Missed scheduled check-in Thursday — no reschedule
- ⚡ Action: Send a low-pressure value-add (industry report or case study) to re-engage
- **Dunder Mifflin** ===$92,000=== | ↓ Momentum: -40%
- Went from 3 meetings/week to 0 this week — possible internal priority shift
- ⚡ Action: Reach out to secondary contact for intel on internal dynamics

---
*Powered by Backstory MCP — 14 accounts analyzed, 2 hot, 2 cold*
