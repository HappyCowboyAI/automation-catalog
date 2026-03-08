# 06 — Executive Inbox

## Overview

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Workflow ID**| 06-executive-inbox                                 |
| **Status**     | Active                                             |
| **Trigger**    | Schedule                                           |
| **Node Count** | 41                                                 |
| **Credentials**| People.ai MCP, Anthropic, Gmail, Slack Bot, Atlassian MCP |

## Category
account-monitoring

## Description

Automates executive email triage by reading unread Gmail messages, identifying those from customers or prospects, enriching them with CRM context from People.ai, and using AI to classify and route each message. Claude analyzes the email content alongside account history to determine urgency, category (support escalation, deal progression, renewal, executive outreach, etc.), and the appropriate internal channel or person. Routed messages land in the right Slack channel or trigger follow-up workflows, ensuring nothing falls through the cracks.

## Node Flow

1. **Schedule Trigger & Email Fetch** — On a recurring schedule, reads unread emails from the executive's Gmail inbox.
2. **Identify Customer Emails** — Code and conditional logic filter out internal, automated, and non-customer messages, keeping only emails that warrant attention.
3. **Enrich with Account Context** — For each customer email, queries People.ai MCP and Atlassian MCP to pull account status, recent activity, open tickets, and relationship history.
4. **AI Triage & Classification** — Claude (via agent, structured output parser, and chain) analyzes email content plus account context to assign urgency, category, and routing recommendation.
5. **Route to Channels** — A switch node directs each classified email to the appropriate Slack channel, team member, or follow-up queue based on the AI's triage decision.
6. **Await & Follow Up** — Wait nodes handle deferred actions and ensure follow-up tasks are tracked.

## Key Nodes

| Node Type                | Role                                      |
|--------------------------|-------------------------------------------|
| `scheduleTrigger`        | Recurring schedule trigger                |
| `gmail`                  | Reads unread executive emails             |
| `splitInBatches`         | Iterates over emails                      |
| `code`                   | Email parsing and data transformation     |
| `if` / `switch`          | Conditional filtering and routing         |
| `agent`                  | Orchestrates AI triage reasoning          |
| `lmChatAnthropic`        | Claude language model                     |
| `mcpClientTool`          | People.ai and Atlassian MCP integration   |
| `chainLlm`              | LLM chain for structured analysis         |
| `outputParserStructured` | Enforces typed classification output      |
| `wait`                   | Manages deferred follow-up actions        |

## Credentials Required

- **People.ai MCP** — Account context and engagement history
- **Anthropic** — Claude LLM for triage and classification
- **Gmail** — Executive inbox access
- **Slack Bot** — Routes messages to appropriate channels
- **Atlassian MCP** — Ticket and project context
