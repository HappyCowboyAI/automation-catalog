# 04 — Opportunity Discovery

## Overview

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Workflow ID**| 04-opportunity-discovery                           |
| **Status**     | Active                                             |
| **Trigger**    | Schedule — Weekly                                  |
| **Node Count** | 30                                                 |
| **Credentials**| People.ai MCP, Anthropic, Slack Bot, SMTP          |

## Description

Surfaces hidden revenue opportunities by identifying accounts with recent engagement activity but no corresponding open opportunities in the pipeline. On a weekly cadence, the workflow cross-references People.ai activity data against the CRM pipeline, flags accounts showing buying signals without active deals, and uses Claude to analyze the strength of those signals. Findings are posted to Slack and optionally emailed, giving reps a curated list of accounts worth pursuing.

## Node Flow

1. **Schedule Trigger** — Fires on a weekly cadence.
2. **Gather Activity & Pipeline Data** — Pulls recent account engagement from People.ai MCP and current open opportunities, then merges the datasets to identify gaps.
3. **Identify Unmatched Accounts** — Code and set nodes cross-reference activity against pipeline to find accounts with engagement signals but no open opportunity.
4. **AI Signal Analysis** — Claude evaluates each flagged account's activity patterns, contact seniority, and engagement intensity to score opportunity likelihood and recommend next steps.
5. **Notify via Slack & Email** — Posts a prioritized list of discovered opportunities to Slack and sends email summaries to relevant stakeholders via SMTP.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly trigger                            |
| `set`                 | Variable configuration                    |
| `httpRequest`         | API calls for activity and pipeline data  |
| `code`                | Cross-referencing and gap detection       |
| `agent`               | Orchestrates AI signal analysis           |
| `lmChatAnthropic`     | Claude language model                     |
| `mcpClientTool`       | People.ai MCP integration                 |
| `merge`               | Combines activity and pipeline datasets   |
| `emailSend`           | SMTP email delivery                       |

## Credentials Required

- **People.ai MCP** — Account engagement and activity signals
- **Anthropic** — Claude LLM for opportunity scoring
- **Slack Bot** — Posts discovery results to channel
- **SMTP** — Email delivery for stakeholder summaries
