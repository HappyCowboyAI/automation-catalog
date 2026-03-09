# 09 — Onboarding Pulse

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 09-onboarding-pulse                                  |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Daily 8:00 AM                             |
| **Node Count** | 26                                                   |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
customer-success

## Description

Monitors newly closed deals during their first 90 days to detect accounts going dark before they become a retention problem. The workflow identifies recently closed-won accounts, checks People.ai engagement data for post-sale activity (meetings booked, emails exchanged, contacts engaged), and flags accounts with below-threshold engagement. An AI agent assesses each flagged account and recommends specific re-engagement actions. Alerts are sent to the CSM and sales handoff team via Messaging.

## Node Flow

1. **Schedule Trigger** — Fires daily at 8:00 AM.
2. **Find New Customers** — Queries CRM for accounts closed-won in the last 90 days.
3. **Check Post-Sale Engagement** — For each account, pulls People.ai data on meetings, emails, and contact engagement since close date.
4. **AI Engagement Assessment** — AI Agent evaluates whether engagement is on track, at risk, or dark. Generates re-engagement recommendations for at-risk accounts.
5. **Alert on Silent Accounts** — Sends alerts to the CSM for accounts flagged as at-risk or dark, with specific recommended next steps.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Daily 8 AM trigger                        |
| `crmQuery`            | Fetches recently closed-won accounts      |
| `mcpClientTool`       | People.ai post-sale engagement data       |
| `code`                | Engagement threshold calculation           |
| `if`                  | Filters for at-risk and dark accounts     |
| `agent`               | AI engagement assessment and recommendations |
| `lmChat`              | LLM language model                        |

## Credentials Required

- **People.ai MCP** — Post-sale engagement tracking
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI engagement assessment
- **CRM (Salesforce, HubSpot, etc.)** — Closed-won account data
- **Messaging (Slack, Teams, Email)** — Alerts to CSMs

## Sample Output

<!--mockup:slack-->
<!--bot:Onboard-->
<!--bot-app:true-->

👶 **Onboarding Pulse** — 2 new customers need attention

🔴 **GOING DARK — Immediate Re-engagement Needed:**
- **Dunder Mifflin** | ===$125,000=== | Closed Won: Feb 3 | Day 34 of 90
- Post-sale engagement: **0 meetings, 2 emails** (benchmark: 4 meetings, 12 emails by Day 34)
- Champion Michael Scott hasn't responded to last 3 CSM emails
- No kickoff meeting scheduled — implementation hasn't started
- 👉 @emily.ross: Escalate to sales handoff team. @sarah.chen (AE) should call champion directly — leverage closing relationship

🟡 **AT RISK — Below Engagement Threshold:**
- **Pied Piper Inc** | ===$88,000=== | Closed Won: Feb 18 | Day 19 of 90
- Post-sale engagement: 1 meeting, 5 emails (benchmark: 2 meetings, 8 emails by Day 19)
- Kickoff completed but no follow-up meeting scheduled
- Technical contact Dinesh Chugtai is responsive via email but hasn't booked implementation session
- 👉 @david.kim: Send calendar link with 3 time slots for implementation kickoff. Include pre-work checklist to reduce friction

🟢 **ON TRACK:** 5 accounts progressing normally through onboarding
- Strongest: Contoso Ltd (Day 12) — 3 meetings already, full team engaged

---
*Powered by People.ai MCP — 7 accounts in onboarding window monitored*
