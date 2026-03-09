# Channel Pulse — Platform-Agnostic Recipe

> Rebuild this workflow on **any** automation platform (Make, Power Automate, Zapier, etc.)

## Prerequisites

- **People.ai API access** — Since most platforms lack native MCP support, you'll need the People.ai REST API or a custom MCP-to-REST bridge
- **LLM API key** — Claude, OpenAI, or any LLM with a chat completion endpoint
- **Messaging credentials** — Slack Bot Token, Teams Webhook, or SMTP

## Architecture

```
Schedule (60s) → Fetch Active Accounts → Loop Each Account →
  Gather Context → AI Summarize → Route to Channel → Post Update
```

## Step-by-Step Rebuild

### Step 1: Schedule Trigger
- **What:** Recurring trigger on a configurable interval (default: 60 seconds)
- **Make:** Schedule module → set to every 1 minute
- **Power Automate:** Recurrence trigger → frequency: Minute, interval: 1
- **Zapier:** Schedule by Zapier → every hour (Zapier minimum is 1 min on paid plans)

### Step 2: Identify Active Accounts
- **What:** Query People.ai for accounts with activity in the last 7 days
- **API call:** `GET /api/v1/accounts?activity_since={7_days_ago_ISO}`
- **Make:** HTTP module → GET request to People.ai REST endpoint
- **Power Automate:** HTTP action → Method: GET, URI: People.ai endpoint
- **Zapier:** Webhooks by Zapier → GET request

### Step 3: Loop Over Accounts
- **What:** Iterate through each active account
- **Make:** Iterator module on the accounts array
- **Power Automate:** Apply to Each action
- **Zapier:** Looping by Zapier (or use Paths for up to 3 accounts)

### Step 4: Gather Account Context
- **What:** For each account, pull engagement details from People.ai
- **API call:** `POST /api/v1/accounts/{id}/activity-summary`
  - Body: `{ "lookback_days": 7, "include": ["meetings", "emails", "contacts", "deals"] }`
- **All platforms:** HTTP request module with account ID from Step 3

### Step 5: AI Summarization
- **What:** Send raw activity data to an LLM for formatting
- **API call:** `POST https://api.anthropic.com/v1/messages` (or OpenAI equivalent)
- **System prompt:**
  ```
  You are a sales intelligence assistant. Given raw account activity data,
  produce a concise, scannable channel update with:
  - Account name, deal value, close date, health indicator
  - THIS WEEK'S KEY DEVELOPMENTS (3-5 bullets)
  - RISKS & OPPORTUNITIES (3-5 bullets)
  - NEXT WEEK'S ACTIONS (3-5 bullets with @owner tags)
  ```
- **Make:** HTTP module → POST to Anthropic/OpenAI API
- **Power Automate:** HTTP action → or use the AI Builder "Create text with GPT" action
- **Zapier:** OpenAI integration (built-in) or HTTP request for Claude

### Step 6: Route to Channel
- **What:** Map account name to the correct Slack/Teams channel
- **Implementation:** Lookup table (spreadsheet, database, or hardcoded map)
- **Make:** Data store or Google Sheets lookup
- **Power Automate:** Excel table lookup or Switch action with account conditions
- **Zapier:** Lookup Table (built-in) or Google Sheets lookup

### Step 7: Deliver Update
- **What:** Post the formatted summary to the mapped channel
- **Slack:** `POST https://slack.com/api/chat.postMessage`
  - Body: `{ "channel": "{channel_id}", "text": "{summary}" }`
- **Teams:** POST to incoming webhook URL with message card JSON
- **Email:** SMTP send with HTML body
- **Make:** Slack → Send a Message module (or Teams/Email module)
- **Power Automate:** Post Message in a Chat or Channel (Teams built-in)
- **Zapier:** Slack → Send Channel Message action

## MCP Gap Workaround

Most platforms cannot connect to People.ai via MCP natively. Options:

1. **REST API proxy** — Deploy a lightweight server (FastAPI, Express) that translates MCP calls to REST. Host on Vercel, Railway, or internal infra.
2. **People.ai REST API** — If available for your account, use the REST endpoints directly.
3. **n8n as middleware** — Use n8n's native MCP support to handle the People.ai integration, expose results via webhook that your platform calls.

## Estimated Build Time

| Platform        | Estimated Time | Complexity |
|-----------------|---------------|------------|
| Make            | 2-3 hours     | Medium     |
| Power Automate  | 3-4 hours     | Medium-High (JSON handling) |
| Zapier          | 2-3 hours     | Medium (loop limitations) |
| Custom code     | 1-2 hours     | Low (if you know Python/TS) |
| n8n (native)    | 15 minutes    | Low (import JSON) |
