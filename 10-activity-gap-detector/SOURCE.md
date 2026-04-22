# 10 — Activity Gap Detector

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 10-activity-gap-detector                             |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly Friday 8:00 AM                     |
| **Node Count** | 24                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email) |

## Category
coaching-enablement

## Description

Compares each rep's weekly activity patterns against team benchmarks and top performer profiles using Backstory activity data. Identifies reps with low outbound activity, thin multi-threading on key deals, or single-threaded opportunities missing executive engagement. An AI agent generates personalized coaching nudges for sales managers, highlighting specific gaps and suggesting actionable improvement areas. Delivered weekly to frontline managers via Messaging.

## Node Flow

1. **Schedule Trigger** — Fires weekly on Friday at 8:00 AM.
2. **Fetch Team Activity** — Pulls Backstory activity data for all reps on the team: emails sent, meetings held, contacts engaged, accounts touched.
3. **Benchmark Analysis** — Code node calculates team averages and top-performer baselines, then flags reps falling below thresholds.
4. **AI Coaching Insights** — AI Agent analyzes each flagged rep's patterns, identifies specific gaps (e.g., low multi-threading, no exec outreach), and generates coaching recommendations.
5. **Deliver to Managers** — Sends a per-manager coaching digest via Messaging, listing their reps' gaps with suggested conversation starters.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly Friday 8 AM trigger                |
| `mcpClientTool`       | Backstory team activity data              |
| `code`                | Benchmark calculation and gap detection   |
| `agent`               | AI coaching insight generation            |
| `lmChat`              | LLM language model                        |
| `splitInBatches`      | Iterates over managers                    |

## Credentials Required

- **Backstory MCP** — Rep activity and engagement data
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI coaching analysis
- **Messaging (Slack, Teams, Email)** — Delivers coaching digests to managers

## Sample Output

<!--mockup:slack-->
<!--bot:Tempo-->
<!--bot-app:true-->

📉 **Weekly Activity Gap Report** — @manager.jen's Team | Week of Mar 3

📊 **TEAM BENCHMARKS:**
- Avg emails/week: 47 | Top performer: 72 (@sarah.chen)
- Avg meetings/week: 8 | Top performer: 12 (@james.park)
- Avg accounts touched: 11 | Top performer: 16 (@sarah.chen)

🔴 **SIGNIFICANT GAPS:**
- **@david.kim** — 3 gaps identified
- Emails: 18/week (62% below team avg of 47)
- Multi-threading: 4 of 6 active deals are single-threaded (team avg: 1.5 single-threaded)
- No executive outreach on ===$180,000=== Globex deal despite 5 weeks in pipeline
- 💬 Suggested coaching: "David, I noticed your Globex deal is single-threaded to a Director. What's your plan to get VP-level access? Sarah had success on ACME using the mutual connection approach."

🟡 **MODERATE GAPS:**
- **@mike.torres** — 1 gap identified
- Meetings: 4/week (50% below team avg of 8) — 3 cancellations by prospects this week
- Email and multi-threading metrics are strong
- 💬 Suggested coaching: "Mike, looks like a few meetings fell through this week. Want to brainstorm ways to reduce cancellation rates? James uses calendar holds that work well."

🟢 **NO GAPS:** @sarah.chen, @james.park — both at or above benchmarks across all dimensions

---
*Powered by Backstory MCP — 4 reps analyzed, 2 with coaching opportunities*
