# 11 — Deal Hygiene Audit

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 11-deal-hygiene-audit                                |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly Monday 7:30 AM                     |
| **Node Count** | 27                                                   |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
coaching-enablement

## Description

Performs a weekly pipeline hygiene audit by scanning all open opportunities in the CRM and cross-referencing with People.ai engagement data. Flags deals with stale close dates, no recent activity, missing next steps, single-threaded contacts, or no executive engagement. An AI agent prioritizes the issues and generates a per-rep action list with specific cleanup tasks. Delivered to reps and their managers via Messaging every Monday morning.

## Node Flow

1. **Schedule Trigger** — Fires weekly on Monday at 7:30 AM.
2. **Pull Open Pipeline** — Queries CRM for all open opportunities with their stages, close dates, and assigned reps.
3. **Check Deal Engagement** — For each deal, pulls People.ai data on last activity date, contacts engaged, meeting recency, and email thread status.
4. **AI Hygiene Assessment** — AI Agent identifies hygiene issues per deal (stale, single-threaded, no exec, past close date) and prioritizes by deal value and stage.
5. **Deliver Action Lists** — Sends a per-rep cleanup checklist via Messaging, CC'ing their manager, with specific actions for each flagged deal.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly Monday 7:30 AM trigger             |
| `crmQuery`            | Fetches open pipeline opportunities       |
| `mcpClientTool`       | People.ai deal engagement data            |
| `code`                | Hygiene rule evaluation and flagging      |
| `agent`               | AI prioritization and action generation   |
| `lmChat`              | LLM language model                        |

## Credentials Required

- **People.ai MCP** — Deal engagement and activity data
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI hygiene assessment
- **CRM (Salesforce, HubSpot, etc.)** — Open pipeline data
- **Messaging (Slack, Teams, Email)** — Delivers action lists to reps and managers
