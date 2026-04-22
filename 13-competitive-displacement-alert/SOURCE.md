# 13 — Competitive Displacement Alert

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 13-competitive-displacement-alert                    |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Daily 7:00 AM                             |
| **Node Count** | 26                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
strategic-intelligence

## Description

Monitors customer accounts for early signs of competitive displacement. The workflow scans Backstory engagement data for accounts where internal engagement has suddenly dropped while simultaneously checking for competitor mentions in email subjects, meeting titles, or CRM notes. An AI agent evaluates the combined signals to assess displacement risk and recommends defensive actions. High-risk alerts are sent immediately to the account owner and their manager via Messaging.

## Node Flow

1. **Schedule Trigger** — Fires daily at 7:00 AM.
2. **Scan Engagement Drops** — Queries Backstory for accounts with significant week-over-week engagement declines (meetings, emails, response times).
3. **Check Competitor Signals** — For flagged accounts, searches CRM notes, email subjects, and meeting titles for competitor name mentions or evaluation-related keywords.
4. **AI Displacement Assessment** — AI Agent correlates engagement drops with competitor signals, assigns a displacement risk level, and generates a defensive action plan.
5. **Alert Account Team** — Sends high-priority alerts to the account owner and manager via Messaging with risk assessment and recommended defensive plays.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Daily 7 AM trigger                        |
| `mcpClientTool`       | Backstory engagement trend analysis       |
| `crmQuery`            | Competitor signal search in CRM           |
| `code`                | Signal correlation and threshold logic    |
| `agent`               | AI displacement risk assessment           |
| `lmChat`              | LLM language model                        |
| `if`                  | Filters for high-risk accounts only       |

## Credentials Required

- **Backstory MCP** — Engagement trend data and drop detection
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI displacement analysis
- **CRM (Salesforce, HubSpot, etc.)** — Competitor signal search
- **Messaging (Slack, Teams, Email)** — High-priority alerts to account teams

## Sample Output

<!--mockup:slack-->
<!--bot:Shield-->
<!--bot-app:true-->

🚨 **Competitive Displacement Alert** — 2 accounts at risk

🔴 **HIGH RISK — Immediate Defensive Action Required:**
- **Stark Industries** | ===$185,000=== ARR | Customer since 2024
- Engagement drop: -74% week-over-week (meetings: 2→0, emails: 15→4)
- Competitor signal: "Vendara demo" found in CRM meeting title for Mar 12
- IT Director posted on LinkedIn about "evaluating modern alternatives" on Tuesday
- Champion @lisa.wong response time went from <2hr to 24hr+
- 👉 @emily.ross + @sarah.chen: Request emergency exec check-in. Prep competitive battlecard. Offer exclusive roadmap preview for Q3 features they requested
- 👉 @sales.leadership: Approve discount authority up to 15% if needed for retention

🟡 **ELEVATED RISK — Monitor Closely:**
- **Umbrella Corp** | ===$94,000=== ARR | Customer since 2025
- Engagement drop: -45% week-over-week (meetings on track, but email responses slowing)
- Competitor signal: Procurement team downloaded comparison matrix from competitor G2 page
- No direct competitor engagement detected yet — early warning stage
- Champion still responsive in meetings but less forthcoming with timeline info
- 👉 @david.kim: Proactively share customer success metrics and ROI report. Schedule value review before they reach evaluation stage

🟢 **ALL CLEAR:** 38 accounts show no displacement signals

---
*Powered by Backstory MCP — 40 accounts monitored, 2 flagged*
