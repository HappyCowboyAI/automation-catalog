# 16 — Executive Sponsor Tracker

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 16-executive-sponsor-tracker                         |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Daily 7:30 AM                             |
| **Node Count** | 25                                                   |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
strategic-intelligence

## Description

Monitors executive-level contact engagement across strategic deals to ensure champion and sponsor relationships stay active. The workflow identifies open opportunities above a configurable deal value threshold, checks People.ai for executive contact engagement (VP+ titles), and flags deals where executive sponsors have gone silent (no meetings or emails in the configured lookback window). An AI agent assesses the risk of each silent-sponsor situation and recommends re-engagement tactics. Alerts are sent to the deal owner and sales leadership via Messaging.

## Node Flow

1. **Schedule Trigger** — Fires daily at 7:30 AM.
2. **Find Strategic Deals** — Queries CRM for open opportunities above the deal value threshold with identified executive contacts.
3. **Check Executive Engagement** — For each deal, pulls People.ai engagement data for VP+ contacts to detect silent sponsors (no activity in lookback window).
4. **AI Risk & Re-engagement** — AI Agent evaluates the impact of sponsor silence on deal health and generates specific re-engagement tactics per deal.
5. **Alert Deal Owners** — Sends alerts to deal owners and sales leadership via Messaging for deals with silent executive sponsors.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Daily 7:30 AM trigger                     |
| `crmQuery`            | Strategic deal and executive contact data  |
| `mcpClientTool`       | People.ai executive engagement tracking   |
| `code`                | Silence detection logic                   |
| `agent`               | AI risk assessment and re-engagement tips |
| `lmChat`              | LLM language model                        |
| `if`                  | Filters for deals with silent sponsors    |

## Credentials Required

- **People.ai MCP** — Executive contact engagement data
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI risk and re-engagement analysis
- **CRM (Salesforce, HubSpot, etc.)** — Strategic deal and contact data
- **Messaging (Slack, Teams, Email)** — Alerts to deal owners and leadership
