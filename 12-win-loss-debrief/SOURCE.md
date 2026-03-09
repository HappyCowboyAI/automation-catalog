# 12 — Win/Loss Debrief Generator

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 12-win-loss-debrief                                  |
| **Status**     | Active                                               |
| **Trigger**    | Webhook — CRM deal stage change to Closed Won/Lost   |
| **Node Count** | 22                                                   |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
coaching-enablement

## Description

Automatically generates a structured win/loss debrief when any deal closes (won or lost). Triggered by a CRM webhook on stage change, the workflow pulls the full engagement timeline from People.ai — every meeting, email, contact involved, and engagement cadence throughout the deal cycle. An AI agent analyzes the timeline to produce a structured debrief: what worked, where engagement dropped, key turning points, multi-threading effectiveness, and lessons learned. The debrief is delivered to the rep, their manager, and optionally a shared enablement channel.

## Node Flow

1. **Webhook Trigger** — Fires when a CRM opportunity moves to Closed Won or Closed Lost.
2. **Fetch Deal Timeline** — Pulls the complete People.ai engagement history for the deal: meetings, emails, contacts, activity cadence over the deal lifecycle.
3. **AI Debrief Analysis** — AI Agent analyzes the full timeline, identifies key moments (first exec meeting, proposal sent, competitor mention, engagement gaps), and generates a structured debrief.
4. **Deliver Debrief** — Formats the debrief as a rich message and delivers to the rep, their manager, and the team enablement channel via Messaging.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `webhookTrigger`      | CRM deal closed event                     |
| `mcpClientTool`       | People.ai full deal engagement timeline   |
| `agent`               | AI timeline analysis and debrief writing  |
| `lmChat`              | LLM language model                        |
| `outputParserStructured` | Enforces typed debrief output          |
| `switch`              | Routes Won vs Lost to different templates |

## Credentials Required

- **People.ai MCP** — Full deal engagement timeline
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI debrief generation
- **CRM (Salesforce, HubSpot, etc.)** — Deal close webhook and opportunity data
- **Messaging (Slack, Teams, Email)** — Delivers debriefs to rep, manager, and team
