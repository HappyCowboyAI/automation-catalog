# 07 — Churn Risk Scorecard

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 07-churn-risk-scorecard                              |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly Monday 7:00 AM                     |
| **Node Count** | 28                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email), CRM (Salesforce, HubSpot, etc.) |

## Category
customer-success

## Description

Generates a weekly churn risk scorecard for the customer success team. The workflow pulls engagement trends, support ticket volumes, champion contact activity, and product usage signals from Backstory and the CRM. An AI agent scores each account on a 1-10 churn risk scale, identifies the top risk drivers, and suggests specific save plays. The scorecard is delivered to CS managers via Messaging with accounts ranked by risk severity.

## Node Flow

1. **Schedule Trigger** — Fires weekly on Monday at 7:00 AM.
2. **Fetch Active Accounts** — Queries CRM for all active customer accounts assigned to the CS team.
3. **Enrich with Engagement Data** — For each account, pulls Backstory engagement trends, contact activity changes, and meeting frequency from MCP.
4. **AI Risk Scoring** — AI Agent analyzes engagement drop-offs, support ticket spikes, champion departures, and usage patterns to assign a 1-10 churn risk score with top risk drivers.
5. **Compile Scorecard** — Aggregates scored accounts into a ranked scorecard with risk tiers (Critical / Watch / Healthy) and suggested save plays.
6. **Deliver to CS Managers** — Sends the formatted scorecard via Messaging to each CS manager for their portfolio.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly Monday 7 AM trigger                |
| `crmQuery`            | Fetches active customer accounts          |
| `splitInBatches`      | Iterates over each account                |
| `mcpClientTool`       | Backstory engagement data retrieval       |
| `agent`               | AI risk scoring and save play generation  |
| `lmChat`              | LLM language model                        |
| `code`                | Score aggregation and tier classification |
| `outputParserStructured` | Enforces typed risk score output       |

## Credentials Required

- **Backstory MCP** — Engagement trends and contact activity
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI risk scoring and analysis
- **CRM (Salesforce, HubSpot, etc.)** — Active account list and support data
- **Messaging (Slack, Teams, Email)** — Delivers scorecard to CS managers

## Sample Output

<!--mockup:slack-->
<!--bot:Sentinel-->
<!--bot-app:true-->

📋 **Weekly Churn Risk Scorecard** — @emily.ross's Portfolio | Week of Mar 3

🔴 **CRITICAL (Score 8-10):**
- **Dunder Mifflin** | ===$210,000=== ARR | Score: **9/10** | ↑ from 6 last week
- Champion departed company 2 weeks ago, no new contact established
- Product logins down 62% month-over-month
- 3 unresolved P1 support tickets (oldest: 14 days)
- 💡 Save play: Emergency exec alignment — request warm intro to new VP from departing champion

🟡 **WATCH (Score 5-7):**
- **Stark Industries** | ===$185,000=== ARR | Score: **6/10** | → steady
- Meeting frequency dropped from weekly to biweekly over last month
- NPS survey response: 6 (down from 8 at last QBR)
- 💡 Save play: Schedule health check disguised as product roadmap preview
- **Umbrella Corp** | ===$94,000=== ARR | Score: **5/10** | ↓ from 7 — improving
- Re-engaged after CSM outreach last week — 2 meetings booked
- Still below usage benchmarks but trending positive
- 💡 Save play: Continue current re-engagement cadence, introduce new feature set

🟢 **HEALTHY (Score 1-4):** 11 accounts — no action needed

---
*Powered by Backstory MCP — 14 accounts scored, 1 critical, 2 watch*
