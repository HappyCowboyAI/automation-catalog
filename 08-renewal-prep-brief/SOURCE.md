# 08 — Renewal Prep Brief

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 08-renewal-prep-brief                                |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Daily 7:00 AM                             |
| **Node Count** | 25                                                   |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
customer-success

## Description

Automatically generates renewal preparation briefs at 60, 30, and 15 days before each account's renewal date. The workflow queries the CRM for upcoming renewals, enriches each account with People.ai engagement trends, support history, expansion signals, and key contact activity. An AI agent produces a structured brief covering account health, risk factors, expansion opportunities, and a recommended renewal strategy. Briefs are delivered to the assigned CSM and account executive via Messaging.

## Node Flow

1. **Schedule Trigger** — Fires daily at 7:00 AM.
2. **Find Upcoming Renewals** — Queries CRM for accounts with renewals in 60, 30, or 15 days, filtering out those already briefed at this milestone.
3. **Enrich with Account Health** — For each renewal account, pulls People.ai engagement trends, support ticket history, champion activity, and expansion signals from MCP.
4. **AI Brief Generation** — AI Agent synthesizes engagement data into a structured renewal brief with health score, risk factors, expansion opportunities, and recommended strategy.
5. **Deliver to Account Team** — Sends the brief to the assigned CSM and AE via Messaging with the renewal date and urgency tier highlighted.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Daily 7 AM trigger                        |
| `crmQuery`            | Fetches accounts approaching renewal      |
| `if`                  | Filters by 60/30/15-day milestones        |
| `mcpClientTool`       | People.ai engagement and health data      |
| `agent`               | AI brief generation with structured output|
| `lmChat`              | LLM language model                        |
| `outputParserStructured` | Enforces typed brief output            |

## Credentials Required

- **People.ai MCP** — Engagement trends and relationship health
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI brief generation
- **CRM (Salesforce, HubSpot, etc.)** — Renewal dates and account data
- **Messaging (Slack, Teams, Email)** — Delivers briefs to account teams

## Sample Output

<!--mockup:slack-->
<!--bot:Renew-->
<!--bot-app:true-->

🔄 **Renewal Prep Brief** — Globex Industries | ⏰ 30 Days to Renewal

📊 **ACCOUNT SNAPSHOT:**
- ARR: ===$340,000=== | Renewal Date: Apr 8, 2026
- Health Score: 6/10 (down from 8 at last QBR)
- CSM: @emily.ross | AE: @sarah.chen

🟢 **STRENGTHS:**
- Product adoption: 87% feature utilization (above 75% benchmark)
- Champion Lisa Wong remains actively engaged — 3 meetings in last 2 weeks
- Expanded usage to 2 new departments since last renewal (Engineering + Marketing)
- No competitive mentions detected in any communications

⚠️ **RISK FACTORS:**
- Executive sponsor (VP Ops) has not engaged in 45 days — previously monthly cadence
- 3 open support tickets (1 P1 unresolved for 14 days) — CSAT trending down
- Finance team asked about multi-year discount options — could signal price sensitivity
- Champion mentioned "evaluating options" in passing during Feb 22 check-in

💡 **EXPANSION SIGNALS:**
- Marketing team requesting API access for additional integrations
- Lisa Wong asked about enterprise tier features in last meeting
- Potential upsell: ===$85,000=== if API + enterprise tier added

📋 **RECOMMENDED STRATEGY:**
- Re-engage VP Ops with exec business review showing ROI metrics
- Resolve P1 ticket before renewal conversation starts
- Lead with expansion offer (API + enterprise) to anchor on value, not price
- Prepare 3-year proposal with graduated discount to address price sensitivity

---
*Powered by People.ai MCP — 12 months of engagement history analyzed*
