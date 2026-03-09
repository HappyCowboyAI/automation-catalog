# 07 — Churn Risk Scorecard

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 07-churn-risk-scorecard                              |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly Monday 7:00 AM                     |
| **Node Count** | 28                                                   |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email), CRM (Salesforce, HubSpot, etc.) |

## Category
customer-success

## Description

Generates a weekly churn risk scorecard for the customer success team. The workflow pulls engagement trends, support ticket volumes, champion contact activity, and product usage signals from People.ai and the CRM. An AI agent scores each account on a 1-10 churn risk scale, identifies the top risk drivers, and suggests specific save plays. The scorecard is delivered to CS managers via Messaging with accounts ranked by risk severity.

## Node Flow

1. **Schedule Trigger** — Fires weekly on Monday at 7:00 AM.
2. **Fetch Active Accounts** — Queries CRM for all active customer accounts assigned to the CS team.
3. **Enrich with Engagement Data** — For each account, pulls People.ai engagement trends, contact activity changes, and meeting frequency from MCP.
4. **AI Risk Scoring** — AI Agent analyzes engagement drop-offs, support ticket spikes, champion departures, and usage patterns to assign a 1-10 churn risk score with top risk drivers.
5. **Compile Scorecard** — Aggregates scored accounts into a ranked scorecard with risk tiers (Critical / Watch / Healthy) and suggested save plays.
6. **Deliver to CS Managers** — Sends the formatted scorecard via Messaging to each CS manager for their portfolio.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly Monday 7 AM trigger                |
| `crmQuery`            | Fetches active customer accounts          |
| `splitInBatches`      | Iterates over each account                |
| `mcpClientTool`       | People.ai engagement data retrieval       |
| `agent`               | AI risk scoring and save play generation  |
| `lmChat`              | LLM language model                        |
| `code`                | Score aggregation and tier classification |
| `outputParserStructured` | Enforces typed risk score output       |

## Credentials Required

- **People.ai MCP** — Engagement trends and contact activity
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI risk scoring and analysis
- **CRM (Salesforce, HubSpot, etc.)** — Active account list and support data
- **Messaging (Slack, Teams, Email)** — Delivers scorecard to CS managers
