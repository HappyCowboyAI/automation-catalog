# 15 — QBR Auto-Prep

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 15-qbr-auto-prep                                     |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly (configurable to quarterly cadence) |
| **Node Count** | 30                                                   |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Calendar (Google Calendar, Outlook), Messaging (Slack, Teams, Email) |

## Category
strategic-intelligence

## Description

Automatically prepares quarterly business review materials for every account on an upcoming QBR agenda. The workflow scans the calendar for meetings tagged as QBRs (or matching configurable title patterns), then for each account on the agenda, pulls the full quarter's engagement data from People.ai: meeting frequency, email volume, contacts engaged, key relationship changes, and deal progression. An AI agent generates a structured QBR prep document with executive summary, engagement trends, wins/risks, and talking points. Delivered to the account team 48 hours before the QBR.

## Node Flow

1. **Schedule Trigger** — Fires on a configurable schedule to check for upcoming QBRs within the next 48 hours.
2. **Find Upcoming QBRs** — Scans calendar for meetings matching QBR title patterns, extracts the associated account names.
3. **Pull Quarterly Engagement** — For each QBR account, queries People.ai for the full quarter's engagement data: meetings, emails, contact maps, and activity trends.
4. **AI QBR Document Generation** — AI Agent produces a structured QBR prep document with executive summary, quarter-over-quarter trends, key wins, risk areas, and recommended talking points.
5. **Deliver Prep Materials** — Sends the QBR prep document to the account team via Messaging 48 hours before the meeting.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Configurable cadence trigger              |
| `calendarQuery`       | Finds upcoming QBR meetings               |
| `mcpClientTool`       | People.ai quarterly engagement data       |
| `agent`               | AI QBR document generation                |
| `lmChat`              | LLM language model                        |
| `outputParserStructured` | Enforces typed QBR document output     |
| `code`                | Quarter date range calculation            |

## Credentials Required

- **People.ai MCP** — Quarterly engagement data and relationship maps
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI document generation
- **CRM (Salesforce, HubSpot, etc.)** — Account and opportunity context
- **Calendar (Google Calendar, Outlook)** — QBR meeting detection
- **Messaging (Slack, Teams, Email)** — Delivers prep materials to account teams
