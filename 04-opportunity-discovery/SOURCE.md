# 04 — Opportunity Discovery

## Overview

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Workflow ID**| 04-opportunity-discovery                           |
| **Status**     | Active                                             |
| **Trigger**    | Schedule — Weekly                                  |
| **Node Count** | 30                                                 |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email), SMTP |

## Description

Surfaces hidden revenue opportunities by identifying accounts with recent engagement activity but no corresponding open opportunities in the pipeline. On a weekly cadence, the workflow cross-references People.ai activity data against the CRM pipeline, flags accounts showing buying signals without active deals, and uses the LLM to analyze the strength of those signals. Findings are posted via Messaging (Slack, Teams, or Email) and optionally emailed, giving reps a curated list of accounts worth pursuing.

## Node Flow

1. **Schedule Trigger** — Fires on a weekly cadence.
2. **Gather Activity & Pipeline Data** — Pulls recent account engagement from People.ai MCP and current open opportunities, then merges the datasets to identify gaps.
3. **Identify Unmatched Accounts** — Code and set nodes cross-reference activity against pipeline to find accounts with engagement signals but no open opportunity.
4. **AI Signal Analysis** — AI Agent evaluates each flagged account's activity patterns, contact seniority, and engagement intensity to score opportunity likelihood and recommend next steps.
5. **Notify via Messaging** — Posts a prioritized list of discovered opportunities via Messaging (Slack, Teams, or Email) and sends email summaries to relevant stakeholders via SMTP.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly trigger                            |
| `set`                 | Variable configuration                    |
| `httpRequest`         | API calls for activity and pipeline data  |
| `code`                | Cross-referencing and gap detection       |
| `agent`               | Orchestrates AI signal analysis           |
| `lmChat`              | LLM language model                        |
| `mcpClientTool`       | People.ai MCP integration                 |
| `merge`               | Combines activity and pipeline datasets   |
| `emailSend`           | SMTP email delivery                       |

## Credentials Required

- **People.ai MCP** — Account engagement and activity signals
- **LLM API (Claude, OpenAI, Gemini, etc.)** — LLM for opportunity scoring
- **Messaging (Slack, Teams, Email)** — Posts discovery results to channel
- **SMTP** — Email delivery for stakeholder summaries

## Sample Output

<!--mockup:slack-->
<!--bot:Prospector-->
<!--bot-app:true-->

🔍 **Weekly Opportunity Discovery** — 4 hidden opportunities found

🟢 **HIGH CONFIDENCE:**
- **NovaTech Solutions** | No open opp | Signal strength: **Strong**
- 7 meetings in last 30 days with VP Product + Director of Engineering
- @mike.torres received inbound pricing inquiry last Tuesday
- Previously churned 18 months ago — re-engagement pattern suggests renewed interest
- 👉 @sarah.chen: Create opp, estimated ===$200,000=== based on prior deal size + expansion signals
- **Contoso Ltd** | No open opp | Signal strength: **Strong**
- Downloaded 4 technical whitepapers + attended webinar last week
- CTO Maria Santos connected with @james.park on LinkedIn and engaged 2 posts
- No prior relationship — net new logo opportunity
- 👉 @james.park: Outbound with personalized demo offer referencing webinar attendance

🟡 **MODERATE CONFIDENCE:**
- **Initrode Systems** | No open opp | Signal strength: **Moderate**
- 3 emails exchanged with mid-level contact, but no meetings booked yet
- Account matches ICP: 500+ employees, Series C, SaaS vertical
- 👉 @rep.owner: Nurture with case study from similar company, attempt meeting
- **Pied Piper Inc** | No open opp | Signal strength: **Moderate**
- CFO visited pricing page 3x this week (tracked via marketing automation)
- No direct engagement with sales team yet
- 👉 @david.kim: Warm intro via mutual connection at board level

---
*Powered by People.ai MCP — 230 accounts scanned, 4 opportunities surfaced*
