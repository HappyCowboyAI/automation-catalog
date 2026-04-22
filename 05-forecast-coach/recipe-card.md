# Forecast Coach — Platform-Agnostic Recipe

> Rebuild this workflow on **any** automation platform (Make, Power Automate, Zapier, etc.)

## Prerequisites

- **Backstory API access** — REST API or MCP-to-REST bridge
- **LLM API key** — Claude, OpenAI, or any chat completion endpoint
- **SMTP credentials** — Email delivery for coaching reports
- **Leader/team mapping** — Who manages which reps (spreadsheet or CRM)

## Architecture

```
Schedule (Monday AM) → Fetch Leaders → Loop Each Leader →
  Pull Team Pipeline → Filter Active Deals → AI Deal Assessment →
  Compile Coaching Report → Email to Leader
```

## Step-by-Step Rebuild

### Step 1: Weekly Monday Trigger
- **What:** Fire every Monday morning
- **Make:** Schedule module → every Monday at 7 AM
- **Power Automate:** Recurrence → weekly, Monday, 07:00
- **Zapier:** Schedule by Zapier → every week on Monday

### Step 2: Fetch Leader Roster
- **What:** Get list of sales leaders and their team members
- **Data format:** `[{"name": "Jen Martinez", "email": "jen@company.com", "reps": ["sarah.chen", "james.park", "david.kim"]}]`
- **Make:** Google Sheets / Airtable → read leader-rep mapping
- **Power Automate:** SharePoint list or Excel table
- **Zapier:** Google Sheets → Get Many Rows

### Step 3: Loop Over Leaders
- **What:** Process each leader's team individually
- **Make:** Iterator module
- **Power Automate:** Apply to Each
- **Zapier:** Looping by Zapier

### Step 4: Pull Team Pipeline
- **What:** For each leader's reps, get their open opportunities
- **API call:**
  `POST /api/v1/opportunities/by-owner`
  Body: `{ "owners": ["sarah.chen", "james.park"], "status": "open", "include": ["engagement", "stakeholders", "stage_history"] }`
- **All platforms:** HTTP request to Backstory REST API or CRM query

### Step 5: AI Deal Health Assessment
- **What:** Analyze each deal across coaching dimensions
- **API call:** `POST https://api.anthropic.com/v1/messages`
- **System prompt:**
  ```
  You are a sales coaching assistant analyzing pipeline health.
  For each deal assess:
  - Engagement recency (last contact)
  - Stakeholder coverage (single vs multi-threaded)
  - Stage velocity (on pace or stalled)
  - Competitive signals
  - Risk indicators (pushed dates, champion changes)

  Generate a coaching report:
  - Pipeline summary (total value, commit, best case)
  - Needs Attention (🔴) with coaching conversation starters
  - Monitor (🟡) with emerging risks
  - On Track (🟢) count
  Each flagged deal: "💬 Coach: [specific question to ask rep]"
  ```
- **Make:** HTTP module → POST to Anthropic/OpenAI
- **Power Automate:** HTTP action or AI Builder
- **Zapier:** OpenAI integration or HTTP request

### Step 6: Deliver Coaching Report
- **What:** Email the personalized report to each leader
- **Make:** Email → Send (SMTP or Gmail)
- **Power Automate:** Send an email (Office 365) or SMTP
- **Zapier:** Email by Zapier or Gmail → Send Email

## MCP Gap Workaround

See the Channel Pulse recipe card for MCP-to-REST bridge options. The same
approach applies — use Backstory REST API directly or deploy a proxy.

## Leader-Rep Mapping Options

| Store              | Best For           | Setup Time |
|--------------------|--------------------|------------|
| Google Sheets      | Small orgs         | 10 min     |
| CRM hierarchy      | Enterprise         | 30 min     |
| Airtable           | Visual management  | 15 min     |
| HR system API      | Auto-sync          | 1-2 hours  |

## Estimated Build Time

| Platform        | Estimated Time | Complexity |
|-----------------|---------------|------------|
| Make            | 4-5 hours     | High       |
| Power Automate  | 5-6 hours     | High       |
| Zapier          | 4-5 hours     | High       |
| Custom code     | 2-3 hours     | Medium     |
| n8n (native)    | 15 minutes    | Low (import JSON) |
