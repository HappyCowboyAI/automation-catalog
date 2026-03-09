# 13 — Competitive Displacement Alert

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 13-competitive-displacement-alert                    |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Daily 7:00 AM                             |
| **Node Count** | 26                                                   |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
strategic-intelligence

## Description

Monitors customer accounts for early signs of competitive displacement. The workflow scans People.ai engagement data for accounts where internal engagement has suddenly dropped while simultaneously checking for competitor mentions in email subjects, meeting titles, or CRM notes. An AI agent evaluates the combined signals to assess displacement risk and recommends defensive actions. High-risk alerts are sent immediately to the account owner and their manager via Messaging.

## Node Flow

1. **Schedule Trigger** — Fires daily at 7:00 AM.
2. **Scan Engagement Drops** — Queries People.ai for accounts with significant week-over-week engagement declines (meetings, emails, response times).
3. **Check Competitor Signals** — For flagged accounts, searches CRM notes, email subjects, and meeting titles for competitor name mentions or evaluation-related keywords.
4. **AI Displacement Assessment** — AI Agent correlates engagement drops with competitor signals, assigns a displacement risk level, and generates a defensive action plan.
5. **Alert Account Team** — Sends high-priority alerts to the account owner and manager via Messaging with risk assessment and recommended defensive plays.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Daily 7 AM trigger                        |
| `mcpClientTool`       | People.ai engagement trend analysis       |
| `crmQuery`            | Competitor signal search in CRM           |
| `code`                | Signal correlation and threshold logic    |
| `agent`               | AI displacement risk assessment           |
| `lmChat`              | LLM language model                        |
| `if`                  | Filters for high-risk accounts only       |

## Credentials Required

- **People.ai MCP** — Engagement trend data and drop detection
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI displacement analysis
- **CRM (Salesforce, HubSpot, etc.)** — Competitor signal search
- **Messaging (Slack, Teams, Email)** — High-priority alerts to account teams
