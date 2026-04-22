# 17 — Marketing-to-Sales Handoff Scorer

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 17-marketing-sales-handoff-scorer                    |
| **Status**     | Active                                               |
| **Trigger**    | Webhook — New MQL created in CRM/MAP                 |
| **Node Count** | 23                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
pipeline-forecasting

## Description

Enriches marketing-qualified leads at the moment of handoff by checking Backstory for existing engagement history. When a new MQL is created in the CRM or marketing automation platform, the workflow queries Backstory to see if the account already has relationship history — prior meetings, email threads, known contacts, or past opportunities. An AI agent scores the handoff quality (hot / warm / cold) and generates a context brief for the receiving SDR or AE, so they never walk into a "cold" call that's actually warm. Delivered instantly via Messaging.

## Node Flow

1. **Webhook Trigger** — Fires when a new MQL is created in CRM or marketing automation platform.
2. **Enrich with Backstory History** — Queries Backstory for any existing engagement with the MQL's account: past meetings, email history, known contacts, prior opportunities.
3. **AI Handoff Scoring** — AI Agent evaluates the engagement history to score the handoff (hot / warm / cold) and generates a context brief with key talking points and relationship history.
4. **Deliver to SDR/AE** — Sends the scored handoff with context brief to the assigned SDR or AE via Messaging, including recommended first outreach approach.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `webhookTrigger`      | New MQL creation event                    |
| `mcpClientTool`       | Backstory account engagement history      |
| `agent`               | AI handoff scoring and brief generation   |
| `lmChat`              | LLM language model                        |
| `outputParserStructured` | Enforces typed handoff score output    |
| `switch`              | Routes hot/warm/cold to different urgency levels |

## Credentials Required

- **Backstory MCP** — Account engagement history
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI handoff scoring
- **CRM (Salesforce, HubSpot, etc.)** — MQL data and account lookup
- **Messaging (Slack, Teams, Email)** — Delivers scored handoff to SDR/AE

## Sample Output

<!--mockup:slack-->
<!--bot:Handoff-->
<!--bot-app:true-->

🤝 **New MQL Handoff** — Scored & Ready for Outreach

🔥 **HOT HANDOFF** — Immediate follow-up recommended

**Contoso Ltd** | MQL: Maria Santos, COO | Score: **Hot (9/10)**

📊 **EXISTING RELATIONSHIP HISTORY:**
- Account has **prior engagement**: 12 meetings + 34 emails over 6 months in 2024
- Previous opp: ===$150,000=== — Closed Lost (budget timing, not competitive)
- Champion from prior deal (Kevin Marsh, Director) still at company and was recently promoted
- @james.park was the prior AE — already has relationship context

🎯 **CONTEXT BRIEF FOR @james.park:**
- Maria Santos (COO) is new to the account since your last engagement — joined from Globex Industries in Jan 2026
- She downloaded the enterprise pricing guide + ROI calculator this week
- Budget cycle: Q2 planning starts next week (per prior intel from Kevin)
- Prior objection (budget timing) is likely resolved given new fiscal year

📋 **RECOMMENDED FIRST OUTREACH:**
- Approach: Warm re-engagement — reference prior relationship with Kevin Marsh
- Opening: "Maria, Kevin Marsh suggested I reach out — we worked together on an evaluation last year and I understand you're exploring solutions for Q2"
- Ask: 30-minute discovery call focused on what's changed since last evaluation
- Urgency: High — budget cycle window is narrow

---
*Powered by Backstory MCP — full account engagement history matched*
