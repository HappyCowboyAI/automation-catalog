# 05 — Forecast Coach

## Overview

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Workflow ID**| 05-forecast-coach                                  |
| **Status**     | Off                                                |
| **Trigger**    | Schedule — Weekly (Monday)                         |
| **Node Count** | 19                                                 |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), SMTP |

## Description

Provides AI-powered coaching insights for sales leaders by analyzing their team's open pipeline each week. Every Monday, the workflow pulls each leader's team pipeline from People.ai, filters for active deals, and uses the LLM to assess deal health — looking at engagement recency, stakeholder coverage, stage velocity, and risk indicators. The result is a per-leader coaching report delivered via email, highlighting deals that need attention and suggesting specific coaching actions.

## Node Flow

1. **Schedule Trigger** — Fires every Monday morning.
2. **Pull Team Pipeline** — Fetches open opportunities for each sales leader's team via People.ai MCP and filters for active, in-progress deals.
3. **AI Deal Health Analysis** — AI Agent evaluates each deal across multiple dimensions (engagement, momentum, stakeholder mapping, competitive signals) and generates coaching-ready insights.
4. **Compile Leader Reports** — Aggregates deal-level insights into a per-leader coaching summary with prioritized action items.
5. **Deliver via Email** — Sends each sales leader their personalized coaching report via SMTP.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly Monday trigger                     |
| `httpRequest`         | Fetches pipeline and team data            |
| `code`                | Pipeline analysis and report formatting   |
| `filter`              | Selects active deals for review           |
| `splitInBatches`      | Iterates over leaders and deals           |
| `set`                 | Variable and parameter configuration      |
| `agent`               | Orchestrates AI coaching analysis         |
| `lmChat`              | LLM language model                        |
| `mcpClientTool`       | People.ai MCP integration                 |
| `emailSend`           | SMTP email delivery                       |

## Credentials Required

- **People.ai MCP** — Pipeline data and engagement metrics
- **LLM API (Claude, OpenAI, Gemini, etc.)** — LLM for deal health analysis
- **SMTP** — Email delivery for coaching reports

## Sample Output

<!--mockup:slack-->
<!--bot:Coach-->
<!--bot-app:true-->

🏈 **Weekly Forecast Coaching Report** — @manager.jen's Team | Week of Mar 3

📊 **PIPELINE SUMMARY:**
- Team pipeline: ===$2.1M=== across 12 active deals
- Forecast commit: ===$890,000=== | Best case: ===$1.4M===
- 3 deals need coaching intervention this week

🔴 **NEEDS ATTENTION:**
- **ACME Corp** ===$425,000=== | @sarah.chen | Stage: Negotiation
- Single-threaded to technical champion only — no executive sponsor engaged
- Close date is Mar 28 but legal review hasn't started
- 💬 Coach: Ask Sarah who the economic buyer is and why they haven't been engaged yet
- **Globex Industries** ===$180,000=== | @james.park | Stage: Discovery
- 4 meetings completed but all with same contact (Director level)
- No upward access despite 6 weeks in pipeline
- 💬 Coach: Help James build a multi-threading plan — target VP Engineering via LinkedIn warm intro

🟡 **MONITOR:**
- **Initech** ===$92,000=== | @david.kim | Stage: POC
- POC running 1 week behind schedule — customer delayed test environment setup
- Engagement still strong (3 meetings this week) but timeline risk emerging
- 💬 Coach: Discuss contingency plan if POC extends past Mar 21 deadline

🟢 **ON TRACK:** 9 deals progressing normally — no coaching needed

---
*Powered by People.ai MCP — 12 deals analyzed across 4 reps*
