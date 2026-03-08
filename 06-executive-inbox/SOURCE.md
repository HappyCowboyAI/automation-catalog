# 06 — Executive Inbox

## Overview

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Workflow ID**| 06-executive-inbox                                 |
| **Status**     | Active                                             |
| **Trigger**    | Schedule                                           |
| **Node Count** | 41                                                 |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), Email (Gmail, Outlook, IMAP), Messaging (Slack, Teams, Email), Project Management (Jira, Asana, etc.) — optional |

## Category
account-monitoring

## Description

Automates executive email triage by reading unread email messages, identifying those from customers or prospects, enriching them with CRM context from People.ai, and using AI to classify and route each message. The AI Agent analyzes the email content alongside account history to determine urgency, category (support escalation, deal progression, renewal, executive outreach, etc.), and the appropriate internal channel or person. Routed messages land in the right Messaging channel (Slack, Teams, or Email) or trigger follow-up workflows, ensuring nothing falls through the cracks.

## Node Flow

1. **Schedule Trigger & Email Fetch** — On a recurring schedule, reads unread emails from the executive's inbox (Gmail, Outlook, or IMAP).
2. **Identify Customer Emails** — Code and conditional logic filter out internal, automated, and non-customer messages, keeping only emails that warrant attention.
3. **Enrich with Account Context** — For each customer email, queries People.ai MCP and Project Management (Jira, Asana, etc.) to pull account status, recent activity, open tickets, and relationship history.
4. **AI Triage & Classification** — AI Agent (via agent, structured output parser, and chain) analyzes email content plus account context to assign urgency, category, and routing recommendation.
5. **Route to Channels** — A switch node directs each classified email to the appropriate Messaging channel (Slack, Teams, or Email), team member, or follow-up queue based on the AI's triage decision.
6. **Await & Follow Up** — Wait nodes handle deferred actions and ensure follow-up tasks are tracked.

## Key Nodes

| Node Type                | Role                                      |
|--------------------------|-------------------------------------------|
| `scheduleTrigger`        | Recurring schedule trigger                |
| `email`                  | Reads unread executive emails (Gmail, Outlook, IMAP) |
| `splitInBatches`         | Iterates over emails                      |
| `code`                   | Email parsing and data transformation     |
| `if` / `switch`          | Conditional filtering and routing         |
| `agent`                  | Orchestrates AI triage reasoning          |
| `lmChat`                 | LLM language model                        |
| `mcpClientTool`          | People.ai and Project Management integration |
| `chainLlm`              | LLM chain for structured analysis         |
| `outputParserStructured` | Enforces typed classification output      |
| `wait`                   | Manages deferred follow-up actions        |

## Credentials Required

- **People.ai MCP** — Account context and engagement history
- **LLM API (Claude, OpenAI, Gemini, etc.)** — LLM for triage and classification
- **Email (Gmail, Outlook, IMAP)** — Executive inbox access
- **Messaging (Slack, Teams, Email)** — Routes messages to appropriate channels
- **Project Management (Jira, Asana, etc.) — optional** — Ticket and project context
