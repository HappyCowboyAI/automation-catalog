# 03 — Silence & Contract Monitor

## Overview

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Workflow ID**| 03-silence-contract-monitor                        |
| **Status**     | Active                                             |
| **Trigger**    | Schedule — 6:30 AM daily                           |
| **Node Count** | 16                                                 |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email), User Configuration Store (built-in JSON, Supabase, Airtable, or any database) |

## Category
account-monitoring

## Description

Monitors accounts for engagement gaps that may signal churn risk. Every morning at 6:30 AM, the workflow pulls accounts and checks for those that have "gone silent" — no meaningful engagement activity within a configured lookback window. For flagged accounts, it uses the LLM to assess the severity of the silence, considering deal stage, contract dates, and historical patterns. Accounts deemed concerning are surfaced via Alert (Slack, Teams, or Email) so the owning rep or CSM can re-engage.

## Node Flow

1. **Schedule Trigger** — Fires daily at 6:30 AM.
2. **Identify Silent Accounts** — Queries People.ai MCP and the Config Store to find accounts with no recent engagement activity, then splits results into batches for processing.
3. **AI Risk Assessment** — For each silent account, the AI Agent evaluates the engagement gap against deal context, contract timelines, and historical norms to determine risk level.
4. **Filter & Route** — Conditional logic (`if` node) separates high-concern accounts from benign silences (e.g., post-close quiet periods).
5. **Alert via Messaging** — Sends targeted Alert (Slack, Teams, or Email) for accounts that warrant attention, including AI-generated context and suggested next steps.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Daily 6:30 AM trigger                     |
| `httpRequest`         | Fetches account and engagement data       |
| `code`                | Silence detection logic and formatting    |
| `splitInBatches`      | Iterates over flagged accounts            |
| `agent`               | Orchestrates AI risk analysis             |
| `lmChat`              | LLM language model                        |
| `mcpClientTool`       | People.ai MCP integration                 |
| `if`                  | Routes based on risk severity             |

## Credentials Required

- **People.ai MCP** — Engagement activity and account data
- **LLM API (Claude, OpenAI, Gemini, etc.)** — LLM for risk assessment
- **Messaging (Slack, Teams, Email)** — Alert delivery
- **User Configuration Store (built-in JSON, Supabase, Airtable, or any database)** — Account metadata and configuration
