# Automation Catalog Expansion — Drops 2–4 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Expand the Backstory Automation Catalog from 6 to 17 workflows across 6 categories, adding Customer Success, Coaching & Enablement, and Strategic Intelligence workflow groups.

**Architecture:** Each new workflow follows the existing pattern: a numbered folder with `SOURCE.md` metadata and (eventually) sanitized JSON exports. Three new categories are added to `build-catalog.py`. The SPA needs no structural changes — it already renders dynamically from `workflows.json`. The build script is updated once, then each workflow is just a new `SOURCE.md` file + rebuild.

**Tech Stack:** Python build script, SOURCE.md markdown files, existing SPA.

---

## Phase Overview

| Drop | Theme | Workflows | New Category |
|------|-------|-----------|-------------|
| 2 | Customer Success / Retention | 07–09 | `customer-success` |
| 3 | Rep Coaching & Enablement | 10–12 | `coaching-enablement` |
| 4 | Strategic Intelligence | 13–15 | `strategic-intelligence` |
| Bonus | Cross-Functional | 16–17 | Split across existing categories |

---

### Task 1: Add New Categories to Build Script

**Files:**
- Modify: `docs/build-catalog.py`

**Step 1: Add 3 new categories to the CATEGORIES list**

In `docs/build-catalog.py`, update the `CATEGORIES` list (line ~24) to add:

```python
CATEGORIES = [
    {"id": "daily-intelligence", "name": "Daily Intelligence", "icon": "sun"},
    {"id": "pipeline-forecasting", "name": "Pipeline & Forecasting", "icon": "trending-up"},
    {"id": "account-monitoring", "name": "Account Monitoring", "icon": "shield"},
    {"id": "customer-success", "name": "Customer Success", "icon": "heart"},
    {"id": "coaching-enablement", "name": "Coaching & Enablement", "icon": "target"},
    {"id": "strategic-intelligence", "name": "Strategic Intelligence", "icon": "zap"},
]
```

**Step 2: Update `_infer_category` to handle new categories**

Add keyword inference for the 3 new categories:

```python
def _infer_category(text: str) -> str:
    t = text.lower()
    if any(kw in t for kw in ["digest", "daily", "morning", "intelligence", "brief"]):
        return "daily-intelligence"
    if any(kw in t for kw in ["pipeline", "forecast", "deal", "revenue", "opportunity"]):
        return "pipeline-forecasting"
    if any(kw in t for kw in ["account", "monitor", "alert", "watch", "silence", "inbox"]):
        return "account-monitoring"
    if any(kw in t for kw in ["churn", "retention", "renewal", "onboarding", "customer success", "health"]):
        return "customer-success"
    if any(kw in t for kw in ["coaching", "enablement", "activity gap", "hygiene", "win/loss", "debrief", "rep"]):
        return "coaching-enablement"
    if any(kw in t for kw in ["competitive", "territory", "qbr", "displacement", "heat map", "strategic", "sponsor"]):
        return "strategic-intelligence"
    return "daily-intelligence"
```

**Step 3: Rebuild catalog to verify no errors**

Run: `cd /Users/scottmetcalf/projects/n8n && python3 docs/build-catalog.py`
Expected: 6 workflows (existing), no errors.

**Step 4: Commit**

```bash
git add docs/build-catalog.py docs/workflows.json
git commit -m "feat: add customer-success, coaching-enablement, strategic-intelligence categories"
```

---

### Task 2: Drop 2 — Churn Risk Scorecard (07)

**Files:**
- Create: `07-churn-risk-scorecard/SOURCE.md`
- Create: `07-churn-risk-scorecard/assets/` (directory)

**Step 1: Create folder and SOURCE.md**

```bash
mkdir -p 07-churn-risk-scorecard/assets
```

**Step 2: Write SOURCE.md**

```markdown
# 07 — Churn Risk Scorecard

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 07-churn-risk-scorecard                              |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly Monday 7:00 AM                     |
| **Node Count** | 28                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email), CRM (Salesforce, HubSpot, etc.) |

## Category
customer-success

## Description

Generates a weekly churn risk scorecard for the customer success team. The workflow pulls engagement trends, support ticket volumes, champion contact activity, and product usage signals from Backstory and the CRM. An AI agent scores each account on a 1–10 churn risk scale, identifies the top risk drivers, and suggests specific save plays. The scorecard is delivered to CS managers via Messaging with accounts ranked by risk severity.

## Node Flow

1. **Schedule Trigger** — Fires weekly on Monday at 7:00 AM.
2. **Fetch Active Accounts** — Queries CRM for all active customer accounts assigned to the CS team.
3. **Enrich with Engagement Data** — For each account, pulls Backstory engagement trends, contact activity changes, and meeting frequency from MCP.
4. **AI Risk Scoring** — AI Agent analyzes engagement drop-offs, support ticket spikes, champion departures, and usage patterns to assign a 1–10 churn risk score with top risk drivers.
5. **Compile Scorecard** — Aggregates scored accounts into a ranked scorecard with risk tiers (Critical / Watch / Healthy) and suggested save plays.
6. **Deliver to CS Managers** — Sends the formatted scorecard via Messaging to each CS manager for their portfolio.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly Monday 7 AM trigger                |
| `crmQuery`            | Fetches active customer accounts          |
| `splitInBatches`      | Iterates over each account                |
| `mcpClientTool`       | Backstory engagement data retrieval       |
| `agent`               | AI risk scoring and save play generation  |
| `lmChat`              | LLM language model                        |
| `code`                | Score aggregation and tier classification |
| `outputParserStructured` | Enforces typed risk score output       |

## Credentials Required

- **Backstory MCP** — Engagement trends and contact activity
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI risk scoring and analysis
- **CRM (Salesforce, HubSpot, etc.)** — Active account list and support data
- **Messaging (Slack, Teams, Email)** — Delivers scorecard to CS managers
```

**Step 3: Rebuild catalog**

Run: `python3 docs/build-catalog.py`
Expected: 7 workflows.

**Step 4: Commit**

```bash
git add 07-churn-risk-scorecard/
git commit -m "feat: add churn risk scorecard workflow (07)"
```

---

### Task 3: Drop 2 — Renewal Prep Brief (08)

**Files:**
- Create: `08-renewal-prep-brief/SOURCE.md`
- Create: `08-renewal-prep-brief/assets/` (directory)

**Step 1: Create folder and SOURCE.md**

```bash
mkdir -p 08-renewal-prep-brief/assets
```

**Step 2: Write SOURCE.md**

```markdown
# 08 — Renewal Prep Brief

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 08-renewal-prep-brief                                |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Daily 7:00 AM                             |
| **Node Count** | 25                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
customer-success

## Description

Automatically generates renewal preparation briefs at 60, 30, and 15 days before each account's renewal date. The workflow queries the CRM for upcoming renewals, enriches each account with Backstory engagement trends, support history, expansion signals, and key contact activity. An AI agent produces a structured brief covering account health, risk factors, expansion opportunities, and a recommended renewal strategy. Briefs are delivered to the assigned CSM and account executive via Messaging.

## Node Flow

1. **Schedule Trigger** — Fires daily at 7:00 AM.
2. **Find Upcoming Renewals** — Queries CRM for accounts with renewals in 60, 30, or 15 days, filtering out those already briefed at this milestone.
3. **Enrich with Account Health** — For each renewal account, pulls Backstory engagement trends, support ticket history, champion activity, and expansion signals from MCP.
4. **AI Brief Generation** — AI Agent synthesizes engagement data into a structured renewal brief with health score, risk factors, expansion opportunities, and recommended strategy.
5. **Deliver to Account Team** — Sends the brief to the assigned CSM and AE via Messaging with the renewal date and urgency tier highlighted.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Daily 7 AM trigger                        |
| `crmQuery`            | Fetches accounts approaching renewal      |
| `if`                  | Filters by 60/30/15-day milestones        |
| `mcpClientTool`       | Backstory engagement and health data      |
| `agent`               | AI brief generation with structured output|
| `lmChat`              | LLM language model                        |
| `outputParserStructured` | Enforces typed brief output            |

## Credentials Required

- **Backstory MCP** — Engagement trends and relationship health
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI brief generation
- **CRM (Salesforce, HubSpot, etc.)** — Renewal dates and account data
- **Messaging (Slack, Teams, Email)** — Delivers briefs to account teams
```

**Step 3: Rebuild catalog**

Run: `python3 docs/build-catalog.py`
Expected: 8 workflows.

**Step 4: Commit**

```bash
git add 08-renewal-prep-brief/
git commit -m "feat: add renewal prep brief workflow (08)"
```

---

### Task 4: Drop 2 — Onboarding Pulse (09)

**Files:**
- Create: `09-onboarding-pulse/SOURCE.md`
- Create: `09-onboarding-pulse/assets/` (directory)

**Step 1: Create folder and SOURCE.md**

```bash
mkdir -p 09-onboarding-pulse/assets
```

**Step 2: Write SOURCE.md**

```markdown
# 09 — Onboarding Pulse

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 09-onboarding-pulse                                  |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Daily 8:00 AM                             |
| **Node Count** | 26                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
customer-success

## Description

Monitors newly closed deals during their first 90 days to detect accounts going dark before they become a retention problem. The workflow identifies recently closed-won accounts, checks Backstory engagement data for post-sale activity (meetings booked, emails exchanged, contacts engaged), and flags accounts with below-threshold engagement. An AI agent assesses each flagged account and recommends specific re-engagement actions. Alerts are sent to the CSM and sales handoff team via Messaging.

## Node Flow

1. **Schedule Trigger** — Fires daily at 8:00 AM.
2. **Find New Customers** — Queries CRM for accounts closed-won in the last 90 days.
3. **Check Post-Sale Engagement** — For each account, pulls Backstory data on meetings, emails, and contact engagement since close date.
4. **AI Engagement Assessment** — AI Agent evaluates whether engagement is on track, at risk, or dark. Generates re-engagement recommendations for at-risk accounts.
5. **Alert on Silent Accounts** — Sends alerts to the CSM for accounts flagged as at-risk or dark, with specific recommended next steps.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Daily 8 AM trigger                        |
| `crmQuery`            | Fetches recently closed-won accounts      |
| `mcpClientTool`       | Backstory post-sale engagement data       |
| `code`                | Engagement threshold calculation           |
| `if`                  | Filters for at-risk and dark accounts     |
| `agent`               | AI engagement assessment and recommendations |
| `lmChat`              | LLM language model                        |

## Credentials Required

- **Backstory MCP** — Post-sale engagement tracking
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI engagement assessment
- **CRM (Salesforce, HubSpot, etc.)** — Closed-won account data
- **Messaging (Slack, Teams, Email)** — Alerts to CSMs
```

**Step 3: Rebuild catalog and commit**

```bash
python3 docs/build-catalog.py
git add 09-onboarding-pulse/
git commit -m "feat: add onboarding pulse workflow (09)"
```

---

### Task 5: Drop 3 — Activity Gap Detector (10)

**Files:**
- Create: `10-activity-gap-detector/SOURCE.md`
- Create: `10-activity-gap-detector/assets/` (directory)

**Step 1: Create folder and SOURCE.md**

```bash
mkdir -p 10-activity-gap-detector/assets
```

**Step 2: Write SOURCE.md**

```markdown
# 10 — Activity Gap Detector

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 10-activity-gap-detector                             |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly Friday 8:00 AM                     |
| **Node Count** | 24                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email) |

## Category
coaching-enablement

## Description

Compares each rep's weekly activity patterns against team benchmarks and top performer profiles using Backstory activity data. Identifies reps with low outbound activity, thin multi-threading on key deals, or single-threaded opportunities missing executive engagement. An AI agent generates personalized coaching nudges for sales managers, highlighting specific gaps and suggesting actionable improvement areas. Delivered weekly to frontline managers via Messaging.

## Node Flow

1. **Schedule Trigger** — Fires weekly on Friday at 8:00 AM.
2. **Fetch Team Activity** — Pulls Backstory activity data for all reps on the team: emails sent, meetings held, contacts engaged, accounts touched.
3. **Benchmark Analysis** — Code node calculates team averages and top-performer baselines, then flags reps falling below thresholds.
4. **AI Coaching Insights** — AI Agent analyzes each flagged rep's patterns, identifies specific gaps (e.g., low multi-threading, no exec outreach), and generates coaching recommendations.
5. **Deliver to Managers** — Sends a per-manager coaching digest via Messaging, listing their reps' gaps with suggested conversation starters.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly Friday 8 AM trigger                |
| `mcpClientTool`       | Backstory team activity data              |
| `code`                | Benchmark calculation and gap detection   |
| `agent`               | AI coaching insight generation            |
| `lmChat`              | LLM language model                        |
| `splitInBatches`      | Iterates over managers                    |

## Credentials Required

- **Backstory MCP** — Rep activity and engagement data
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI coaching analysis
- **Messaging (Slack, Teams, Email)** — Delivers coaching digests to managers
```

**Step 3: Rebuild and commit**

```bash
python3 docs/build-catalog.py
git add 10-activity-gap-detector/
git commit -m "feat: add activity gap detector workflow (10)"
```

---

### Task 6: Drop 3 — Deal Hygiene Audit (11)

**Files:**
- Create: `11-deal-hygiene-audit/SOURCE.md`
- Create: `11-deal-hygiene-audit/assets/` (directory)

**Step 1: Create folder and SOURCE.md**

```bash
mkdir -p 11-deal-hygiene-audit/assets
```

**Step 2: Write SOURCE.md**

```markdown
# 11 — Deal Hygiene Audit

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 11-deal-hygiene-audit                                |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly Monday 7:30 AM                     |
| **Node Count** | 27                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
coaching-enablement

## Description

Performs a weekly pipeline hygiene audit by scanning all open opportunities in the CRM and cross-referencing with Backstory engagement data. Flags deals with stale close dates, no recent activity, missing next steps, single-threaded contacts, or no executive engagement. An AI agent prioritizes the issues and generates a per-rep action list with specific cleanup tasks. Delivered to reps and their managers via Messaging every Monday morning.

## Node Flow

1. **Schedule Trigger** — Fires weekly on Monday at 7:30 AM.
2. **Pull Open Pipeline** — Queries CRM for all open opportunities with their stages, close dates, and assigned reps.
3. **Cross-Reference Engagement** — For each deal, pulls Backstory data on last activity date, contacts engaged, meeting recency, and email thread status.
4. **AI Hygiene Assessment** — AI Agent identifies hygiene issues per deal (stale, single-threaded, no exec, past close date) and prioritizes by deal value and stage.
5. **Deliver Action Lists** — Sends a per-rep cleanup checklist via Messaging, CC'ing their manager, with specific actions for each flagged deal.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly Monday 7:30 AM trigger             |
| `crmQuery`            | Fetches open pipeline opportunities       |
| `mcpClientTool`       | Backstory deal engagement data            |
| `code`                | Hygiene rule evaluation and flagging      |
| `agent`               | AI prioritization and action generation   |
| `lmChat`              | LLM language model                        |

## Credentials Required

- **Backstory MCP** — Deal engagement and activity data
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI hygiene assessment
- **CRM (Salesforce, HubSpot, etc.)** — Open pipeline data
- **Messaging (Slack, Teams, Email)** — Delivers action lists to reps and managers
```

**Step 3: Rebuild and commit**

```bash
python3 docs/build-catalog.py
git add 11-deal-hygiene-audit/
git commit -m "feat: add deal hygiene audit workflow (11)"
```

---

### Task 7: Drop 3 — Win/Loss Debrief Generator (12)

**Files:**
- Create: `12-win-loss-debrief/SOURCE.md`
- Create: `12-win-loss-debrief/assets/` (directory)

**Step 1: Create folder and SOURCE.md**

```bash
mkdir -p 12-win-loss-debrief/assets
```

**Step 2: Write SOURCE.md**

```markdown
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
4. **Format & Deliver** — Formats the debrief as a rich message and delivers to the rep, their manager, and the team enablement channel via Messaging.

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
```

**Step 3: Rebuild and commit**

```bash
python3 docs/build-catalog.py
git add 12-win-loss-debrief/
git commit -m "feat: add win/loss debrief generator workflow (12)"
```

---

### Task 8: Drop 4 — Competitive Displacement Alert (13)

**Files:**
- Create: `13-competitive-displacement-alert/SOURCE.md`
- Create: `13-competitive-displacement-alert/assets/` (directory)

**Step 1: Create folder and SOURCE.md**

```bash
mkdir -p 13-competitive-displacement-alert/assets
```

**Step 2: Write SOURCE.md**

```markdown
# 13 — Competitive Displacement Alert

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 13-competitive-displacement-alert                    |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Daily 7:00 AM                             |
| **Node Count** | 26                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
strategic-intelligence

## Description

Monitors customer accounts for early signs of competitive displacement. The workflow scans Backstory engagement data for accounts where internal engagement has suddenly dropped while simultaneously checking for competitor mentions in email subjects, meeting titles, or CRM notes. An AI agent evaluates the combined signals to assess displacement risk and recommends defensive actions. High-risk alerts are sent immediately to the account owner and their manager via Messaging.

## Node Flow

1. **Schedule Trigger** — Fires daily at 7:00 AM.
2. **Scan Engagement Drops** — Queries Backstory for accounts with significant week-over-week engagement declines (meetings, emails, response times).
3. **Check Competitor Signals** — For flagged accounts, searches CRM notes, email subjects, and meeting titles for competitor name mentions or evaluation-related keywords.
4. **AI Displacement Assessment** — AI Agent correlates engagement drops with competitor signals, assigns a displacement risk level, and generates a defensive action plan.
5. **Alert Account Team** — Sends high-priority alerts to the account owner and manager via Messaging with risk assessment and recommended defensive plays.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Daily 7 AM trigger                        |
| `mcpClientTool`       | Backstory engagement trend analysis       |
| `crmQuery`            | Competitor signal search in CRM           |
| `code`                | Signal correlation and threshold logic    |
| `agent`               | AI displacement risk assessment           |
| `lmChat`              | LLM language model                        |
| `if`                  | Filters for high-risk accounts only       |

## Credentials Required

- **Backstory MCP** — Engagement trend data and drop detection
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI displacement analysis
- **CRM (Salesforce, HubSpot, etc.)** — Competitor signal search
- **Messaging (Slack, Teams, Email)** — High-priority alerts to account teams
```

**Step 3: Rebuild and commit**

```bash
python3 docs/build-catalog.py
git add 13-competitive-displacement-alert/
git commit -m "feat: add competitive displacement alert workflow (13)"
```

---

### Task 9: Drop 4 — Territory Heat Map (14)

**Files:**
- Create: `14-territory-heat-map/SOURCE.md`
- Create: `14-territory-heat-map/assets/` (directory)

**Step 1: Create folder and SOURCE.md**

```bash
mkdir -p 14-territory-heat-map/assets
```

**Step 2: Write SOURCE.md**

```markdown
# 14 — Territory Heat Map

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 14-territory-heat-map                                |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly Monday 6:30 AM                     |
| **Node Count** | 24                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), Messaging (Slack, Teams, Email) |

## Category
strategic-intelligence

## Description

Generates a weekly territory heat map digest for each rep, showing which accounts in their territory are heating up (increased inbound, new contacts engaging, meeting frequency rising) versus cooling down (declining engagement, unresponsive contacts). The workflow pulls Backstory engagement data across all accounts in each rep's territory, calculates week-over-week momentum scores, and uses an AI agent to summarize trends and recommend where to focus time. Delivered every Monday to help reps prioritize their week.

## Node Flow

1. **Schedule Trigger** — Fires weekly on Monday at 6:30 AM.
2. **Fetch Territory Assignments** — Pulls each rep's assigned accounts from CRM or Backstory territory data.
3. **Calculate Account Momentum** — For each account, queries Backstory for week-over-week engagement changes and calculates a momentum score (heating up / steady / cooling down).
4. **AI Territory Summary** — AI Agent analyzes the momentum map, identifies the hottest opportunities and coldest risks, and recommends a prioritized focus list for the week.
5. **Deliver Heat Map Digest** — Sends a per-rep territory digest via Messaging with accounts color-coded by momentum.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Weekly Monday 6:30 AM trigger             |
| `mcpClientTool`       | Backstory territory engagement data       |
| `code`                | Momentum score calculation                |
| `agent`               | AI territory analysis and prioritization  |
| `lmChat`              | LLM language model                        |
| `splitInBatches`      | Iterates over reps                        |

## Credentials Required

- **Backstory MCP** — Account engagement data across territories
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI territory analysis
- **Messaging (Slack, Teams, Email)** — Delivers heat map digests to reps
```

**Step 3: Rebuild and commit**

```bash
python3 docs/build-catalog.py
git add 14-territory-heat-map/
git commit -m "feat: add territory heat map workflow (14)"
```

---

### Task 10: Drop 4 — QBR Auto-Prep (15)

**Files:**
- Create: `15-qbr-auto-prep/SOURCE.md`
- Create: `15-qbr-auto-prep/assets/` (directory)

**Step 1: Create folder and SOURCE.md**

```bash
mkdir -p 15-qbr-auto-prep/assets
```

**Step 2: Write SOURCE.md**

```markdown
# 15 — QBR Auto-Prep

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 15-qbr-auto-prep                                     |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Weekly (configurable to quarterly cadence) |
| **Node Count** | 30                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Calendar (Google Calendar, Outlook), Messaging (Slack, Teams, Email) |

## Category
strategic-intelligence

## Description

Automatically prepares quarterly business review materials for every account on an upcoming QBR agenda. The workflow scans the calendar for meetings tagged as QBRs (or matching configurable title patterns), then for each account on the agenda, pulls the full quarter's engagement data from Backstory: meeting frequency, email volume, contacts engaged, key relationship changes, and deal progression. An AI agent generates a structured QBR prep document with executive summary, engagement trends, wins/risks, and talking points. Delivered to the account team 48 hours before the QBR.

## Node Flow

1. **Schedule Trigger** — Fires on a configurable schedule to check for upcoming QBRs within the next 48 hours.
2. **Find Upcoming QBRs** — Scans calendar for meetings matching QBR title patterns, extracts the associated account names.
3. **Pull Quarterly Engagement** — For each QBR account, queries Backstory for the full quarter's engagement data: meetings, emails, contact maps, and activity trends.
4. **AI QBR Document Generation** — AI Agent produces a structured QBR prep document with executive summary, quarter-over-quarter trends, key wins, risk areas, and recommended talking points.
5. **Deliver Prep Materials** — Sends the QBR prep document to the account team via Messaging 48 hours before the meeting.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Configurable cadence trigger              |
| `calendarQuery`       | Finds upcoming QBR meetings               |
| `mcpClientTool`       | Backstory quarterly engagement data       |
| `agent`               | AI QBR document generation                |
| `lmChat`              | LLM language model                        |
| `outputParserStructured` | Enforces typed QBR document output     |
| `code`                | Quarter date range calculation            |

## Credentials Required

- **Backstory MCP** — Quarterly engagement data and relationship maps
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI document generation
- **CRM (Salesforce, HubSpot, etc.)** — Account and opportunity context
- **Calendar (Google Calendar, Outlook)** — QBR meeting detection
- **Messaging (Slack, Teams, Email)** — Delivers prep materials to account teams
```

**Step 3: Rebuild and commit**

```bash
python3 docs/build-catalog.py
git add 15-qbr-auto-prep/
git commit -m "feat: add QBR auto-prep workflow (15)"
```

---

### Task 11: Bonus — Executive Sponsor Tracker (16)

**Files:**
- Create: `16-executive-sponsor-tracker/SOURCE.md`
- Create: `16-executive-sponsor-tracker/assets/` (directory)

**Step 1: Create folder and SOURCE.md**

```bash
mkdir -p 16-executive-sponsor-tracker/assets
```

**Step 2: Write SOURCE.md**

```markdown
# 16 — Executive Sponsor Tracker

## Overview

| Field          | Value                                              |
|----------------|------------------------------------------------------|
| **Workflow ID**| 16-executive-sponsor-tracker                         |
| **Status**     | Active                                               |
| **Trigger**    | Schedule — Daily 7:30 AM                             |
| **Node Count** | 25                                                   |
| **Credentials**| Backstory MCP, LLM API (Claude, OpenAI, Gemini, etc.), CRM (Salesforce, HubSpot, etc.), Messaging (Slack, Teams, Email) |

## Category
strategic-intelligence

## Description

Monitors executive-level contact engagement across strategic deals to ensure champion and sponsor relationships stay active. The workflow identifies open opportunities above a configurable deal value threshold, checks Backstory for executive contact engagement (VP+ titles), and flags deals where executive sponsors have gone silent (no meetings or emails in the configured lookback window). An AI agent assesses the risk of each silent-sponsor situation and recommends re-engagement tactics. Alerts are sent to the deal owner and sales leadership via Messaging.

## Node Flow

1. **Schedule Trigger** — Fires daily at 7:30 AM.
2. **Find Strategic Deals** — Queries CRM for open opportunities above the deal value threshold with identified executive contacts.
3. **Check Executive Engagement** — For each deal, pulls Backstory engagement data for VP+ contacts to detect silent sponsors (no activity in lookback window).
4. **AI Risk & Re-engagement** — AI Agent evaluates the impact of sponsor silence on deal health and generates specific re-engagement tactics per deal.
5. **Alert Deal Owners** — Sends alerts to deal owners and sales leadership via Messaging for deals with silent executive sponsors.

## Key Nodes

| Node Type             | Role                                      |
|-----------------------|-------------------------------------------|
| `scheduleTrigger`     | Daily 7:30 AM trigger                     |
| `crmQuery`            | Strategic deal and executive contact data  |
| `mcpClientTool`       | Backstory executive engagement tracking   |
| `code`                | Silence detection logic                   |
| `agent`               | AI risk assessment and re-engagement tips |
| `lmChat`              | LLM language model                        |
| `if`                  | Filters for deals with silent sponsors    |

## Credentials Required

- **Backstory MCP** — Executive contact engagement data
- **LLM API (Claude, OpenAI, Gemini, etc.)** — AI risk and re-engagement analysis
- **CRM (Salesforce, HubSpot, etc.)** — Strategic deal and contact data
- **Messaging (Slack, Teams, Email)** — Alerts to deal owners and leadership
```

**Step 3: Rebuild and commit**

```bash
python3 docs/build-catalog.py
git add 16-executive-sponsor-tracker/
git commit -m "feat: add executive sponsor tracker workflow (16)"
```

---

### Task 12: Bonus — Marketing-to-Sales Handoff Scorer (17)

**Files:**
- Create: `17-marketing-sales-handoff-scorer/SOURCE.md`
- Create: `17-marketing-sales-handoff-scorer/assets/` (directory)

**Step 1: Create folder and SOURCE.md**

```bash
mkdir -p 17-marketing-sales-handoff-scorer/assets
```

**Step 2: Write SOURCE.md**

```markdown
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
```

**Step 3: Rebuild and commit**

```bash
python3 docs/build-catalog.py
git add 17-marketing-sales-handoff-scorer/
git commit -m "feat: add marketing-to-sales handoff scorer workflow (17)"
```

---

### Task 13: Update README and Final Catalog Rebuild

**Files:**
- Modify: `README.md`
- Modify: `docs/workflows.json` (auto-generated)

**Step 1: Update the README workflow table**

Update the table in `README.md` to include all 17 workflows grouped by category:

```markdown
## Workflows

| # | Workflow | Category | Trigger | Output |
|---|---------|----------|---------|--------|
| 01 | Sales Digest | Daily Intelligence | 6am weekday | Slack DM |
| 02 | Meeting Brief | Daily Intelligence | 15-min cron | Slack DM |
| 03 | Silence & Contract Monitor | Account Monitoring | Daily 6:30am | Slack alert |
| 04 | Opportunity Discovery | Pipeline & Forecasting | Weekly | Slack channel |
| 05 | Forecast Coach | Pipeline & Forecasting | Weekly Monday | Email |
| 06 | Executive Inbox | Account Monitoring | Schedule | Slack/Email |
| 07 | Churn Risk Scorecard | Customer Success | Weekly Monday | Slack/Email |
| 08 | Renewal Prep Brief | Customer Success | Daily (milestone) | Slack/Email |
| 09 | Onboarding Pulse | Customer Success | Daily | Slack/Email |
| 10 | Activity Gap Detector | Coaching & Enablement | Weekly Friday | Slack/Email |
| 11 | Deal Hygiene Audit | Coaching & Enablement | Weekly Monday | Slack/Email |
| 12 | Win/Loss Debrief Generator | Coaching & Enablement | Webhook (deal close) | Slack/Email |
| 13 | Competitive Displacement Alert | Strategic Intelligence | Daily | Slack/Email |
| 14 | Territory Heat Map | Strategic Intelligence | Weekly Monday | Slack/Email |
| 15 | QBR Auto-Prep | Strategic Intelligence | Configurable | Slack/Email |
| 16 | Executive Sponsor Tracker | Strategic Intelligence | Daily | Slack/Email |
| 17 | Marketing-to-Sales Handoff Scorer | Pipeline & Forecasting | Webhook (new MQL) | Slack/Email |
```

**Step 2: Final rebuild and verify**

Run: `python3 docs/build-catalog.py`
Expected: 17 workflows across 6 categories.

**Step 3: Verify in browser**

Run: `cd docs && python3 -m http.server 9091`
Open catalog, verify all 17 workflows appear, category filters work for all 6 categories, flow visualizations render for new workflows.

**Step 4: Commit**

```bash
git add README.md docs/workflows.json
git commit -m "feat: complete catalog expansion to 17 workflows across 6 categories"
```

---

## Execution Notes

- Tasks 2–12 are independent and can be parallelized (each is just a new folder + SOURCE.md)
- Task 1 (categories) must come first since all new workflows depend on the new category IDs
- Task 13 (README + final build) must come last
- No SPA code changes needed — `index.html` already renders dynamically from `workflows.json`
- JSON exports for new workflows are deferred (owner-gated, same as existing workflows)
