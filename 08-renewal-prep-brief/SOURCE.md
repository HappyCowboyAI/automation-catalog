# 08 — Renewal Prep Brief

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 08-renewal-prep-brief                                |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Daily 7:00 AM                             |
| **Node Count** | 25                                                   |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
customer-success

## Description

Automatically generates renewal preparation briefs at 60, 30, and 15 days before each account's renewal date. The workflow queries the CRM for upcoming renewals, enriches each account with People.ai engagement trends, support history, expansion signals, and key contact activity. An AI agent produces a structured brief covering account health, risk factors, expansion opportunities, and a recommended renewal strategy. Briefs are delivered to the assigned CSM and account executive via Messaging.

## Node Flow

1. **Schedule Trigger** — Fires daily at 7:00 AM.
2. **Find Upcoming Renewals** — Queries CRM for accounts with renewals in 60, 30, or 15 days, filtering out those already briefed at this milestone.
3. **Enrich with Account Health** — For each renewal account, pulls People.ai engagement trends, support ticket history, champion activity, and expansion signals from MCP.
4. **AI Brief Generation** — AI Agent synthesizes engagement data into a structured renewal brief with health score, risk factors, expansion opportunities, and recommended strategy.
5. **Deliver to Account Team** — Sends the brief to the assigned CSM and AE via Messaging with the renewal date and urgency tier highlighted.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Daily 7 AM trigger                        |
| `crmQuery`            | Fetches accounts approaching renewal      |
| `if`                  | Filters by 60/30/15-day milestones        |
| `mcpClientTool`       | People.ai engagement and health data      |
| `agent`               | AI brief generation with structured output|
| `lmChat`              | LLM language model                        |
| `outputParserStructured` | Enforces typed brief output            |

## Credentials Required

- **People.ai MCP** — Engagement trends and relationship health
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI brief generation
- **CRM (Salesforce, HubSpot, etc.)** — Renewal dates and account data
- **Messaging (Slack, Teams, Email)** — Delivers briefs to account teams
