# 18 — Channel Pulse

## Overview

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Workflow ID**| 18-channel-pulse                                   |
| **Status**     | Active                                             |
| **Trigger**    | Schedule — Every 60 seconds                        |
| **Node Count** | 22                                                 |
| **Credentials**| People.ai MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email) |

## Description

Sends quick, 60-second scannable updates to internal customer channels with relevant account information from the last 7 days. Designed to keep the extended team and executives abreast of what's happening in key accounts without requiring them to dig through CRM data or attend every meeting.

## Category

account-monitoring

## Trigger

Schedule — Periodic (configurable interval)

## Output

Messaging (Slack channel, Teams channel, or Email)

## Node Flow

1. **Schedule Trigger** — Fires on a configurable interval to check for accounts due for an update.
2. **Identify Active Accounts** — Queries People.ai MCP to find accounts with recent activity in the last 7 days.
3. **Gather Account Context** — For each account, pulls engagement data, meeting notes, deal movements, and contact activity from People.ai.
4. **AI Summarization** — AI Agent synthesizes the raw activity data into a concise, scannable update formatted for quick consumption.
5. **Route to Channel** — Determines the correct internal customer channel for each account.
6. **Deliver Update** — Posts the formatted update to the appropriate Slack/Teams channel or sends via email.

## Credentials Required

- **People.ai MCP** — Account activity, engagement signals, and contact data for the last 7 days
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI summarization of account activity into scannable updates
- **Messaging (Slack, Teams, Email)** — Delivers updates to internal customer channels

## Configuration

- Update interval: How frequently to check for and send account updates
- Lookback window: Number of days of activity to include (default: 7)
- Channel mapping: Map accounts to their internal Slack/Teams channels
- Update format: Customize the summary template and level of detail
- Account filter: Include/exclude accounts based on tier, owner, or segment

## Sample Output

<!--mockup:slack-->
<!--bot:Subplot-->
<!--bot-app:true-->

**ACME CORP** | ===$287,500=== | 09/2027 | 🟢 Strong Health

🎯 **THIS WEEK'S KEY DEVELOPMENTS:**
- @sarah.chen leading technical validation with engineering team, completed POC review with positive feedback
- Mike Torres (CFO) engaged in renewal pricing discussion — first direct involvement in 3 weeks
- Champion initiated internal advocacy email thread with 4 stakeholders copied
- @james.park completed security questionnaire ahead of schedule

🎯 **RISKS & OPPORTUNITIES:**
- Economic buyer (Mike Torres) had been quiet for 12 days before this week's re-engagement — monitor continuity
- Competitor Vendara mentioned in internal Slack thread by prospect's IT Director
- Champion pushing for faster timeline — potential to pull close date forward by 2 weeks
- Legal review not yet started, could become bottleneck if not initiated this week

👉 **NEXT WEEK'S ACTIONS:**
- @sarah.chen: Schedule executive alignment call with VP Engineering and CFO
- @james.park: Send legal review package to procurement team
- @rep.owner: Follow up on competitor mention with champion for positioning guidance
- @sarah.chen: Prep QBR deck with updated engagement metrics

---
*Powered by People.ai MCP: please thread comments*
