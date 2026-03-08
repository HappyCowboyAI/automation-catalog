# 02 — Meeting Brief

## Overview

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Workflow ID**| 02-meeting-brief                                   |
| **Status**     | Active                                             |
| **Trigger**    | Sub-workflow (called by Meeting Prep Cron, every 15 min) |
| **Node Count** | 13                                                 |
| **Credentials**| People.ai MCP, Anthropic, Slack Bot, Supabase      |

## Description

Prepares an AI-generated briefing document before each upcoming meeting. A parent cron workflow fires every 15 minutes and invokes this sub-workflow for meetings approaching on the calendar. The workflow fetches account context from People.ai via MCP — recent activity, engagement history, key contacts — and passes it to Claude to produce a concise meeting brief. The brief is delivered to the meeting owner via Slack DM so they walk in fully prepared.

## Node Flow

1. **Sub-workflow Trigger** — Receives meeting details from the parent Meeting Prep Cron workflow.
2. **Enrich with Account Context** — Calls People.ai MCP to pull recent account activity, engagement timeline, and stakeholder map for the meeting's associated account.
3. **AI Brief Generation** — Claude analyzes the account context and composes a structured briefing with key talking points, recent interactions, and risk/opportunity signals.
4. **Deliver via Slack** — Sends the formatted meeting brief as a Slack DM to the meeting owner ahead of the call.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `executeWorkflowTrigger` | Entry point from parent cron workflow  |
| `httpRequest`         | API calls for meeting and account data    |
| `code`                | Data shaping and brief formatting         |
| `agent`               | Orchestrates AI reasoning chain           |
| `lmChatAnthropic`     | Claude language model                     |
| `mcpClientTool`       | People.ai MCP integration                 |

## Credentials Required

- **People.ai MCP** — Account activity and engagement context
- **Anthropic** — Claude LLM for brief generation
- **Slack Bot** — Delivers briefs via DM
- **Supabase** — Meeting and user metadata
