# 02 — Meeting Brief

## Overview

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Workflow ID**| 02-meeting-brief                                   |
| **Status**     | Active                                             |
| **Trigger**    | Sub-workflow (called by Meeting Prep Cron, every 15 min) |
| **Node Count** | 13                                                 |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email), User Configuration Store (built-in JSON, Supabase, Airtable, or any database) |

## Category
daily-intelligence

## Description

Prepares an AI-generated briefing document before each upcoming meeting. A parent cron workflow fires every 15 minutes and invokes this sub-workflow for meetings approaching on the calendar. The workflow fetches account context from Backstory via MCP — recent activity, engagement history, key contacts — and passes it to the LLM to produce a concise meeting brief. The brief is delivered to the meeting owner via Messaging (Slack, Teams, or Email) so they walk in fully prepared.

## Node Flow

1. **Sub-workflow Trigger** — Receives meeting details from the parent Meeting Prep Cron workflow.
2. **Enrich with Account Context** — Calls Backstory MCP to pull recent account activity, engagement timeline, and stakeholder map for the meeting's associated account.
3. **AI Brief Generation** — AI Agent analyzes the account context and composes a structured briefing with key talking points, recent interactions, and risk/opportunity signals.
4. **Deliver via Messaging** — Sends the formatted meeting brief via Slack, Teams, or Email to the meeting owner ahead of the call.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `executeWorkflowTrigger` | Entry point from parent cron workflow  |
| `httpRequest`         | API calls for meeting and account data    |
| `code`                | Data shaping and brief formatting         |
| `agent`               | Orchestrates AI reasoning chain           |
| `lmChat`              | LLM language model                        |
| `mcpClientTool`       | Backstory MCP integration                 |

## Credentials Required

- **Backstory MCP** — Account activity and engagement context
- **LLM API (Claude, OpenAI, Gemini, etc.)** — LLM for brief generation
- **Messaging (Slack, Teams, Email)** — Delivers briefs via Slack, Teams, or Email
- **User Configuration Store (built-in JSON, Supabase, Airtable, or any database)** — Meeting and user metadata

## Sample Output

<!--mockup:slack-->
<!--bot:Aria-->
<!--bot-app:true-->

📋 **Meeting Brief** — ACME Corp Technical Review | Today 2:00 PM

👥 **ATTENDEES:**
- @sarah.chen (Account Owner) + @james.park (SE)
- Dan Reeves (VP Engineering, ACME) — Decision maker, attended 3 of last 4 calls
- Lisa Wong (Director of IT, ACME) — Technical champion, drove POC approval
- New: Kevin Marsh (Security Architect) — First time joining, likely for compliance review

📊 **ACCOUNT CONTEXT:**
- Deal: ===$425,000=== | Stage: Technical Validation | Close: 04/2026
- Last meeting (Feb 28): POC results review — positive feedback, 2 action items open
- Champion @lisa.wong sent internal email to procurement team Monday (good sign)
- Competitor Vendara still in evaluation — ACME IT Director mentioned them in a Feb 25 email

🎯 **TALKING POINTS:**
- Address Kevin Marsh's security concerns — prep SOC2 report and data residency docs
- Follow up on open action item: custom API integration timeline (Dan asked Feb 28)
- Ask about procurement timeline — Lisa's internal email suggests they're moving forward
- Subtly position against Vendara: emphasize integration depth and time-to-value

⚠️ **WATCH FOR:**
- Dan Reeves missed last week's check-in — gauge his engagement level today
- If security review scope expands, it could push timeline 2-3 weeks

---
*Powered by Backstory MCP — 47 days of engagement history analyzed*
