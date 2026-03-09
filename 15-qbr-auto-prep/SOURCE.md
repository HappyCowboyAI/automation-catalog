# 15 — QBR Auto-Prep

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 15-qbr-auto-prep                                     |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly (configurable to quarterly cadence) |
| **Node Count** | 30                                                   |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Calendar (Google Calendar, Outlook), Messaging (Slack, Teams, Email) |

## Category
strategic-intelligence

## Description

Automatically prepares quarterly business review materials for every account on an upcoming QBR agenda. The workflow scans the calendar for meetings tagged as QBRs (or matching configurable title patterns), then for each account on the agenda, pulls the full quarter's engagement data from People.ai: meeting frequency, email volume, contacts engaged, key relationship changes, and deal progression. An AI agent generates a structured QBR prep document with executive summary, engagement trends, wins/risks, and talking points. Delivered to the account team 48 hours before the QBR.

## Node Flow

1. **Schedule Trigger** — Fires on a configurable schedule to check for upcoming QBRs within the next 48 hours.
2. **Find Upcoming QBRs** — Scans calendar for meetings matching QBR title patterns, extracts the associated account names.
3. **Pull Quarterly Engagement** — For each QBR account, queries People.ai for the full quarter's engagement data: meetings, emails, contact maps, and activity trends.
4. **AI QBR Document Generation** — AI Agent produces a structured QBR prep document with executive summary, quarter-over-quarter trends, key wins, risk areas, and recommended talking points.
5. **Deliver Prep Materials** — Sends the QBR prep document to the account team via Messaging 48 hours before the meeting.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Configurable cadence trigger              |
| `calendarQuery`       | Finds upcoming QBR meetings               |
| `mcpClientTool`       | People.ai quarterly engagement data       |
| `agent`               | AI QBR document generation                |
| `lmChat`              | LLM language model                        |
| `outputParserStructured` | Enforces typed QBR document output     |
| `code`                | Quarter date range calculation            |

## Credentials Required

- **People.ai MCP** — Quarterly engagement data and relationship maps
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI document generation
- **CRM (Salesforce, HubSpot, etc.)** — Account and opportunity context
- **Calendar (Google Calendar, Outlook)** — QBR meeting detection
- **Messaging (Slack, Teams, Email)** — Delivers prep materials to account teams

## Sample Output

<!--mockup:slack-->
<!--bot:QBR Prep-->
<!--bot-app:true-->

📑 **QBR Prep Document** — ACME Corp | Meeting: Thursday Mar 13, 2:00 PM

📊 **EXECUTIVE SUMMARY:**
- Account: ACME Corp | ARR: ===$425,000=== | Customer since Jan 2024
- Health Score: 8/10 (up from 7 last quarter)
- Quarter highlights: 2 new departments onboarded, feature adoption up 23%
- Primary risk: Executive sponsor engagement declining (see below)

📈 **QUARTER-OVER-QUARTER TRENDS:**
- Meetings: 18 this quarter vs 14 last quarter (+29%)
- Contacts engaged: 12 vs 8 (+50%) — excellent multi-threading growth
- Email volume: 94 vs 71 (+32%)
- Support tickets: 4 vs 7 (-43%) — trending positive
- NPS: 9 (up from 7) — driven by successful API launch

🏆 **KEY WINS THIS QUARTER:**
- Engineering team (Dan Reeves) completed full platform integration ahead of schedule
- Marketing department self-onboarded 15 users without CSM assistance
- Champion Lisa Wong promoted to Senior Director — expanded influence internally
- Zero P1 incidents for 90 consecutive days

⚠️ **RISK AREAS:**
- CFO Mike Torres hasn't attended last 2 monthly check-ins — re-engage on ROI narrative
- Competitor Vendara mentioned by IT Director in Feb — monitor for evaluation signals
- Contract auto-renewal clause expires Apr 30 — need renewal commitment before QBR

🎯 **RECOMMENDED TALKING POINTS:**
- Lead with ROI metrics: $2.3M pipeline influenced, 340 hours saved per quarter
- Introduce enterprise tier upgrade path (potential ===$120,000=== expansion)
- Address competitor mention proactively — show integration depth advantage
- Request CFO attendance at next monthly check-in to reinforce exec alignment

---
*Powered by People.ai MCP — 90 days of engagement data compiled*
