# Opportunity Discovery — Platform-Agnostic Recipe

> Rebuild this workflow on **any** automation platform (Make, Power Automate, Zapier, etc.)

## Prerequisites

- **People.ai API access** — REST API or MCP-to-REST bridge
- **CRM access** — Salesforce, HubSpot, or pipeline data source
- **LLM API key** — Claude, OpenAI, or any chat completion endpoint
- **Messaging credentials** — Slack Bot Token, Teams Webhook, or SMTP

## Architecture

```
Schedule (Weekly) → Fetch Engagement Data → Fetch Open Pipeline →
  Cross-Reference → AI Signal Analysis → Deliver Report (Slack + Email)
```

## Step-by-Step Rebuild

### Step 1: Weekly Trigger
- **What:** Fire once per week (e.g., Monday morning)
- **Make:** Schedule module → every Monday at 8 AM
- **Power Automate:** Recurrence → weekly, Monday, 08:00
- **Zapier:** Schedule by Zapier → every week on Monday

### Step 2: Fetch Engagement Data
- **What:** Pull all accounts with activity in the last 30 days from People.ai
- **API call:**
  `POST /api/v1/accounts/activity-summary`
  Body: `{ "lookback_days": 30, "include": ["meetings", "emails", "content_engagement", "contacts"] }`
- **All platforms:** HTTP request module to People.ai REST API

### Step 3: Fetch Open Pipeline
- **What:** Get all open opportunities from CRM
- **Salesforce:** `GET /services/data/vXX.0/query?q=SELECT+Id,Name,AccountId+FROM+Opportunity+WHERE+IsClosed=false`
- **HubSpot:** `GET /crm/v3/objects/deals?properties=dealname,pipeline,dealstage`
- **Make:** Salesforce → Search Records / HubSpot → List Deals
- **Power Automate:** Salesforce or Dynamics 365 connector
- **Zapier:** Salesforce → Find Records or HubSpot → Find Deals

### Step 4: Cross-Reference
- **What:** Find accounts with engagement but no open opportunity
- **Logic:**
  ```
  engaged_accounts = accounts with activity in last 30 days
  pipeline_accounts = accounts with open opportunities
  gaps = engaged_accounts - pipeline_accounts
  ```
- **Make:** Set module + Array Aggregator + Code module for diff
- **Power Automate:** Compose + Filter Array actions
- **Zapier:** Code by Zapier (Python/JS) for set difference

### Step 5: AI Signal Analysis
- **What:** Score each unmatched account's opportunity potential
- **API call:** `POST https://api.anthropic.com/v1/messages`
- **System prompt:**
  ```
  You are a sales intelligence assistant scoring opportunity potential.
  For each account with engagement but no deal, assess:
  - Signal strength: High or Moderate
  - Evidence: meetings, emails, content downloads, contact seniority
  - Prior relationship: churned, net new, expansion
  - Recommended action with specific next steps
  - Estimated deal size
  Group by confidence. Be specific with numbers and names.
  ```
- **Make:** HTTP module → POST to Anthropic/OpenAI
- **Power Automate:** HTTP action or AI Builder
- **Zapier:** OpenAI integration or HTTP request

### Step 6: Deliver Report
- **What:** Post to Slack channel and email stakeholders
- **Slack:** `POST https://slack.com/api/chat.postMessage`
- **Email:** SMTP or platform email module
- **Make:** Slack → Send Message + Email → Send
- **Power Automate:** Post Message (Teams/Slack) + Send Email
- **Zapier:** Slack → Send Channel Message + Email by Zapier

## MCP Gap Workaround

See the Channel Pulse recipe card for MCP-to-REST bridge options. The same
approach applies — use People.ai REST API directly or deploy a proxy.

## ICP Matching

For stronger signal analysis, add an Ideal Customer Profile (ICP) scoring step:

| Signal               | Weight | Source              |
|----------------------|--------|---------------------|
| Executive meetings   | High   | People.ai           |
| Inbound content      | Medium | Marketing automation |
| Company size/revenue | Medium | CRM or enrichment   |
| Industry fit         | Medium | CRM                 |
| Prior customer       | High   | CRM history         |

## Estimated Build Time

| Platform        | Estimated Time | Complexity |
|-----------------|---------------|------------|
| Make            | 4-5 hours     | High       |
| Power Automate  | 5-6 hours     | High       |
| Zapier          | 4-5 hours     | High       |
| Custom code     | 3-4 hours     | Medium     |
| n8n (native)    | 15 minutes    | Low (import JSON) |
