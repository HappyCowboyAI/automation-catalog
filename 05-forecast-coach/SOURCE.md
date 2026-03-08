# 05 — Forecast Coach

## Overview

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Workflow ID**| 05-forecast-coach                                  |
| **Status**     | Off                                                |
| **Trigger**    | Schedule — Weekly (Monday)                         |
| **Node Count** | 19                                                 |
| **Credentials**| People.ai MCP, Anthropic, SMTP                     |

## Description

Provides AI-powered coaching insights for sales leaders by analyzing their team's open pipeline each week. Every Monday, the workflow pulls each leader's team pipeline from People.ai, filters for active deals, and uses Claude to assess deal health — looking at engagement recency, stakeholder coverage, stage velocity, and risk indicators. The result is a per-leader coaching report delivered via email, highlighting deals that need attention and suggesting specific coaching actions.

## Node Flow

1. **Schedule Trigger** — Fires every Monday morning.
2. **Pull Team Pipeline** — Fetches open opportunities for each sales leader's team via People.ai MCP and filters for active, in-progress deals.
3. **AI Deal Health Analysis** — Claude evaluates each deal across multiple dimensions (engagement, momentum, stakeholder mapping, competitive signals) and generates coaching-ready insights.
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
| `lmChatAnthropic`     | Claude language model                     |
| `mcpClientTool`       | People.ai MCP integration                 |
| `emailSend`           | SMTP email delivery                       |

## Credentials Required

- **People.ai MCP** — Pipeline data and engagement metrics
- **Anthropic** — Claude LLM for deal health analysis
- **SMTP** — Email delivery for coaching reports
