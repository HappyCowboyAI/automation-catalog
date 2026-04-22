# 01 — Sales Digest

## Overview

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Workflow ID**| 01-sales-digest                                    |
| **Status**     | Active                                             |
| **Trigger**    | Schedule — 6:00 AM weekdays                        |
| **Node Count** | 23                                                 |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email), User Configuration Store (built-in JSON, Supabase, Airtable, or any database) |

## Description

Generates a personalized daily sales digest for each enrolled user. At 6 AM on weekdays, the workflow retrieves the list of digest subscribers from the User Config Store, queries Backstory via MCP for each user's relevant account and opportunity activity, then passes the data to the LLM to compose a concise, actionable summary. The finished digest is delivered via Messaging (Slack, Teams, or Email) to each user.

## Node Flow

1. **Schedule Trigger** — Fires at 6:00 AM on weekdays.
2. **Fetch Digest Users** — Reads the subscriber list from the Config Store and splits into individual batches.
3. **Gather Account Activity** — For each user, calls Backstory MCP to pull overnight account updates, engagement signals, and deal movements.
4. **AI Summarization** — AI Agent (via LLM + `agent`) synthesizes raw data into a personalized narrative with key takeaways and recommended actions.
5. **Deliver via Messaging** — Sends the formatted digest via Slack, Teams, or Email to the user.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Cron-based weekday 6 AM trigger           |
| `configStore`         | Reads digest subscriber list              |
| `splitInBatches`      | Iterates over each subscriber             |
| `code`                | Data transformation and formatting        |
| `httpRequest`         | API calls for supplemental data           |
| `agent`               | Orchestrates AI reasoning chain           |
| `lmChat`              | LLM language model                        |
| `mcpClientTool`       | Backstory MCP integration                 |

## Credentials Required

- **Backstory MCP** — Account activity and engagement data
- **LLM API (Claude, OpenAI, Gemini, etc.)** — LLM for digest generation
- **Messaging (Slack, Teams, Email)** — Delivers digests to subscribers
- **User Configuration Store (built-in JSON, Supabase, Airtable, or any database)** — Subscriber list storage

## Sample Output

<!--mockup:slack-->
<!--bot:Aria-->
<!--bot-app:true-->

☀️ **Good Morning, @sarah.chen** — Here's your daily digest for **Tuesday, Mar 4**

📊 **PIPELINE MOVEMENT:**
- **ACME Corp** ===$425,000=== moved to Technical Validation — @james.park scheduled POC for Thursday
- **Globex Industries** ===$180,000=== — Procurement sent redlines on MSA, legal review needed by EOD Wednesday
- **Initech** ===$92,000=== went dark after demo last Tuesday — 6 days no response from champion

🔔 **ENGAGEMENT HIGHLIGHTS:**
- @mike.torres (VP Sales, NovaTech) opened your proposal deck 3x yesterday, forwarded to CFO
- New inbound: Director of Ops at Contoso downloaded whitepaper + visited pricing page
- Wayne Enterprises champion Sarah Kim accepted your QBR invite for next Monday

⚡ **RECOMMENDED ACTIONS:**
- Follow up with Initech champion — silence exceeds your 5-day threshold
- Prep legal response for Globex MSA redlines before Wednesday deadline
- Send NovaTech CFO a personalized ROI summary while momentum is hot

---
*Powered by Backstory MCP — 14 accounts tracked, 3 need attention*
