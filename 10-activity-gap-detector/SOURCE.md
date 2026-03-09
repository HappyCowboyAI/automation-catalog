# 10 — Activity Gap Detector

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 10-activity-gap-detector                             |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly Friday 8:00 AM                     |
| **Node Count** | 24                                                   |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email) |

## Category
coaching-enablement

## Description

Compares each rep's weekly activity patterns against team benchmarks and top performer profiles using People.ai activity data. Identifies reps with low outbound activity, thin multi-threading on key deals, or single-threaded opportunities missing executive engagement. An AI agent generates personalized coaching nudges for sales managers, highlighting specific gaps and suggesting actionable improvement areas. Delivered weekly to frontline managers via Messaging.

## Node Flow

1. **Schedule Trigger** — Fires weekly on Friday at 8:00 AM.
2. **Fetch Team Activity** — Pulls People.ai activity data for all reps on the team: emails sent, meetings held, contacts engaged, accounts touched.
3. **Benchmark Analysis** — Code node calculates team averages and top-performer baselines, then flags reps falling below thresholds.
4. **AI Coaching Insights** — AI Agent analyzes each flagged rep's patterns, identifies specific gaps (e.g., low multi-threading, no exec outreach), and generates coaching recommendations.
5. **Deliver to Managers** — Sends a per-manager coaching digest via Messaging, listing their reps' gaps with suggested conversation starters.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly Friday 8 AM trigger                |
| `mcpClientTool`       | People.ai team activity data              |
| `code`                | Benchmark calculation and gap detection   |
| `agent`               | AI coaching insight generation            |
| `lmChat`              | LLM language model                        |
| `splitInBatches`      | Iterates over managers                    |

## Credentials Required

- **People.ai MCP** — Rep activity and engagement data
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI coaching analysis
- **Messaging (Slack, Teams, Email)** — Delivers coaching digests to managers
