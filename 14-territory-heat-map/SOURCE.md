# 14 — Territory Heat Map

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 14-territory-heat-map                                |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly Monday 6:30 AM                     |
| **Node Count** | 24                                                   |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email) |

## Category
strategic-intelligence

## Description

Generates a weekly territory heat map digest for each rep, showing which accounts in their territory are heating up (increased inbound, new contacts engaging, meeting frequency rising) versus cooling down (declining engagement, unresponsive contacts). The workflow pulls People.ai engagement data across all accounts in each rep's territory, calculates week-over-week momentum scores, and uses an AI agent to summarize trends and recommend where to focus time. Delivered every Monday to help reps prioritize their week.

## Node Flow

1. **Schedule Trigger** — Fires weekly on Monday at 6:30 AM.
2. **Fetch Territory Assignments** — Pulls each rep's assigned accounts from CRM or People.ai territory data.
3. **Calculate Account Momentum** — For each account, queries People.ai for week-over-week engagement changes and calculates a momentum score (heating up / steady / cooling down).
4. **AI Territory Summary** — AI Agent analyzes the momentum map, identifies the hottest opportunities and coldest risks, and recommends a prioritized focus list for the week.
5. **Deliver Heat Map Digest** — Sends a per-rep territory digest via Messaging with accounts color-coded by momentum.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly Monday 6:30 AM trigger             |
| `mcpClientTool`       | People.ai territory engagement data       |
| `code`                | Momentum score calculation                |
| `agent`               | AI territory analysis and prioritization  |
| `lmChat`              | LLM language model                        |
| `splitInBatches`      | Iterates over reps                        |

## Credentials Required

- **People.ai MCP** — Account engagement data across territories
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI territory analysis
- **Messaging (Slack, Teams, Email)** — Delivers heat map digests to reps
