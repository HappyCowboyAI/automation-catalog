# 01 — Sales Digest

## Overview

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Workflow ID**| 01-sales-digest                                    |
| **Status**     | Active                                             |
| **Trigger**    | Schedule — 6:00 AM weekdays                        |
| **Node Count** | 23                                                 |
| **Credentials**| People.ai MCP, Anthropic, Slack Bot, Supabase      |

## Description

Generates a personalized daily sales digest for each enrolled user. At 6 AM on weekdays, the workflow retrieves the list of digest subscribers from Supabase, queries People.ai via MCP for each user's relevant account and opportunity activity, then passes the data to Claude (Anthropic) to compose a concise, actionable summary. The finished digest is delivered as a Slack DM to each user.

## Node Flow

1. **Schedule Trigger** — Fires at 6:00 AM on weekdays.
2. **Fetch Digest Users** — Reads the subscriber list from Supabase and splits into individual batches.
3. **Gather Account Activity** — For each user, calls People.ai MCP to pull overnight account updates, engagement signals, and deal movements.
4. **AI Summarization** — Claude (via `lmChatAnthropic` + `agent`) synthesizes raw data into a personalized narrative with key takeaways and recommended actions.
5. **Deliver via Slack** — Sends the formatted digest as a Slack direct message to the user.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Cron-based weekday 6 AM trigger           |
| `supabase`            | Reads digest subscriber list              |
| `splitInBatches`      | Iterates over each subscriber             |
| `code`                | Data transformation and formatting        |
| `httpRequest`         | API calls for supplemental data           |
| `agent`               | Orchestrates AI reasoning chain           |
| `lmChatAnthropic`     | Claude language model                     |
| `mcpClientTool`       | People.ai MCP integration                 |

## Credentials Required

- **People.ai MCP** — Account activity and engagement data
- **Anthropic** — Claude LLM for digest generation
- **Slack Bot** — Delivers DMs to subscribers
- **Supabase** — Subscriber list storage
