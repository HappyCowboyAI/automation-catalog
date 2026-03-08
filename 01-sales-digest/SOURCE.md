# 01 — Sales Digest

## Overview

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Workflow ID**| 01-sales-digest                                    |
| **Status**     | Active                                             |
| **Trigger**    | Schedule — 6:00 AM weekdays                        |
| **Node Count** | 23                                                 |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email), User Configuration Store (built-in JSON, Supabase, Airtable, or any database) |

## Description

Generates a personalized daily sales digest for each enrolled user. At 6 AM on weekdays, the workflow retrieves the list of digest subscribers from the User Config Store, queries People.ai via MCP for each user's relevant account and opportunity activity, then passes the data to the LLM to compose a concise, actionable summary. The finished digest is delivered via Messaging (Slack, Teams, or Email) to each user.

## Node Flow

1. **Schedule Trigger** — Fires at 6:00 AM on weekdays.
2. **Fetch Digest Users** — Reads the subscriber list from the Config Store and splits into individual batches.
3. **Gather Account Activity** — For each user, calls People.ai MCP to pull overnight account updates, engagement signals, and deal movements.
4. **AI Summarization** — AI Agent (via LLM + `agent`) synthesizes raw data into a personalized narrative with key takeaways and recommended actions.
5. **Deliver via Messaging** — Sends the formatted digest via Slack, Teams, or Email to the user.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Cron-based weekday 6 AM trigger           |
| `configStore`         | Reads digest subscriber list              |
| `splitInBatches`      | Iterates over each subscriber             |
| `code`                | Data transformation and formatting        |
| `httpRequest`         | API calls for supplemental data           |
| `agent`               | Orchestrates AI reasoning chain           |
| `lmChat`              | LLM language model                        |
| `mcpClientTool`       | People.ai MCP integration                 |

## Credentials Required

- **People.ai MCP** — Account activity and engagement data
- **LLM API (Claude, OpenAI, Gemini, etc.)** — LLM for digest generation
- **Messaging (Slack, Teams, Email)** — Delivers digests to subscribers
- **User Configuration Store (built-in JSON, Supabase, Airtable, or any database)** — Subscriber list storage
