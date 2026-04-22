# 11 — Deal Hygiene Audit

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 11-deal-hygiene-audit                                |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly Monday 7:30 AM                     |
| **Node Count** | 27                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
coaching-enablement

## Description

Performs a weekly pipeline hygiene audit by scanning all open opportunities in the CRM and cross-referencing with Backstory engagement data. Flags deals with stale close dates, no recent activity, missing next steps, single-threaded contacts, or no executive engagement. An AI agent prioritizes the issues and generates a per-rep action list with specific cleanup tasks. Delivered to reps and their managers via Messaging every Monday morning.

## Node Flow

1. **Schedule Trigger** — Fires weekly on Monday at 7:30 AM.
2. **Pull Open Pipeline** — Queries CRM for all open opportunities with their stages, close dates, and assigned reps.
3. **Check Deal Engagement** — For each deal, pulls Backstory data on last activity date, contacts engaged, meeting recency, and email thread status.
4. **AI Hygiene Assessment** — AI Agent identifies hygiene issues per deal (stale, single-threaded, no exec, past close date) and prioritizes by deal value and stage.
5. **Deliver Action Lists** — Sends a per-rep cleanup checklist via Messaging, CC'ing their manager, with specific actions for each flagged deal.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly Monday 7:30 AM trigger             |
| `crmQuery`            | Fetches open pipeline opportunities       |
| `mcpClientTool`       | Backstory deal engagement data            |
| `code`                | Hygiene rule evaluation and flagging      |
| `agent`               | AI prioritization and action generation   |
| `lmChat`              | LLM language model                        |

## Credentials Required

- **Backstory MCP** — Deal engagement and activity data
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI hygiene assessment
- **CRM (Salesforce, HubSpot, etc.)** — Open pipeline data
- **Messaging (Slack, Teams, Email)** — Delivers action lists to reps and managers

## Sample Output

<!--mockup:slack-->
<!--bot:Scrub-->
<!--bot-app:true-->

🧹 **Weekly Deal Hygiene Audit** — @sarah.chen | 4 deals need cleanup

🔴 **CRITICAL — Fix Today:**
- **Initech** ===$92,000=== | Stage: POC | Close: **Feb 28 (PAST DUE)**
- Close date is 3 days overdue — update to realistic date or mark as slipped
- No next steps logged in CRM since Feb 20
- 👉 Action: Update close date + add next step with owner and due date

- **Wayne Enterprises** ===$87,000=== | Stage: Discovery | Close: Mar 15
- Single-threaded: Only 1 contact engaged (Sarah Kim, Manager)
- No executive sponsor identified after 4 weeks in pipeline
- 👉 Action: Add at least 1 VP+ contact to opportunity. Request intro from Sarah Kim

🟡 **IMPORTANT — Fix This Week:**
- **NovaTech** ===$275,000=== | Stage: Negotiation | Close: Mar 28
- Last activity was 8 days ago (email) — below 3-day norm for Negotiation stage
- Champion is engaged but legal hasn't responded to MSA sent Mar 1
- 👉 Action: Follow up on MSA status. Log next step: "Legal follow-up by Mar 12"

- **Contoso Ltd** ===$150,000=== | Stage: Qualification | Close: Apr 15
- Missing fields: Competition (blank), MEDDIC score (incomplete), Champion (not identified)
- 3 meetings held but discovery notes not logged
- 👉 Action: Complete MEDDIC fields and log discovery call summaries

🟢 **CLEAN:** 8 deals passed all hygiene checks

---
*Powered by Backstory MCP — 12 deals audited, 4 flagged, 8 clean*
