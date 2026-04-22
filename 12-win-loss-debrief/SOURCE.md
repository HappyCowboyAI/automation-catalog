# 12 — Win/Loss Debrief Generator

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 12-win-loss-debrief                                  |
| **Status**     | Active                                               |
| **Trigger**    | Webhook — CRM deal stage change to Closed Won/Lost   |
| **Node Count** | 22                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
coaching-enablement

## Description

Automatically generates a structured win/loss debrief when any deal closes (won or lost). Triggered by a CRM webhook on stage change, the workflow pulls the full engagement timeline from Backstory — every meeting, email, contact involved, and engagement cadence throughout the deal cycle. An AI agent analyzes the timeline to produce a structured debrief: what worked, where engagement dropped, key turning points, multi-threading effectiveness, and lessons learned. The debrief is delivered to the rep, their manager, and optionally a shared enablement channel.

## Node Flow

1. **Webhook Trigger** — Fires when a CRM opportunity moves to Closed Won or Closed Lost.
2. **Fetch Deal Timeline** — Pulls the complete Backstory engagement history for the deal: meetings, emails, contacts, activity cadence over the deal lifecycle.
3. **AI Debrief Analysis** — AI Agent analyzes the full timeline, identifies key moments (first exec meeting, proposal sent, competitor mention, engagement gaps), and generates a structured debrief.
4. **Deliver Debrief** — Formats the debrief as a rich message and delivers to the rep, their manager, and the team enablement channel via Messaging.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `webhookTrigger`      | CRM deal closed event                     |
| `mcpClientTool`       | Backstory full deal engagement timeline   |
| `agent`               | AI timeline analysis and debrief writing  |
| `lmChat`              | LLM language model                        |
| `outputParserStructured` | Enforces typed debrief output          |
| `switch`              | Routes Won vs Lost to different templates |

## Credentials Required

- **Backstory MCP** — Full deal engagement timeline
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI debrief generation
- **CRM (Salesforce, HubSpot, etc.)** — Deal close webhook and opportunity data
- **Messaging (Slack, Teams, Email)** — Delivers debriefs to rep, manager, and team

## Sample Output

<!--mockup:slack-->
<!--bot:Debrief-->
<!--bot-app:true-->

🏆 **WIN DEBRIEF** — Globex Industries | ===$340,000=== | Closed Won

📊 **DEAL SNAPSHOT:**
- Cycle length: 67 days (benchmark: 82 days) — 18% faster than avg
- Contacts engaged: 9 across 4 departments
- Total meetings: 14 | Emails: 87 | Multi-thread score: A

🔑 **WHAT WORKED:**
- Early multi-threading: @sarah.chen engaged VP Engineering and CFO by Week 2 — both became internal advocates
- Competitive positioning: Proactively addressed Vendara comparison in Week 3 before prospect raised it
- Champion enablement: Provided @lisa.wong with internal business case deck she used to sell upward

⚠️ **WHAT ALMOST DERAILED IT:**
- 11-day gap in Week 4 when champion went on PTO — no backup contact identified until @james.park escalated
- Legal review took 9 days (2x benchmark) — started too late in the process
- Procurement introduced a new vendor security questionnaire at the 11th hour

📈 **KEY TURNING POINTS:**
- Day 12: CFO Mike Torres joined discovery call — deal velocity doubled after this meeting
- Day 34: Champion forwarded internal Slack thread showing 6 stakeholders aligned
- Day 58: Competitor eliminated from shortlist after technical bake-off win

👉 **LESSONS FOR THE TEAM:**
- Start legal/procurement in parallel with technical validation to avoid late-stage delays
- Always identify a backup champion contact before primary goes on PTO
- Early CFO engagement correlates with shorter cycles — replicate this pattern

---
*Powered by Backstory MCP — full engagement timeline analyzed*
