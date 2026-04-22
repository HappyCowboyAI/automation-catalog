# Backstory n8n Workflow Catalog — Design Document

**Date:** 2026-03-08
**Status:** Approved

## Overview

A GitHub Pages SPA that provides importable n8n workflow automations to Backstory customers. Complements the existing LLM Skills Catalog (AI skills for interactive use) with hands-free workflow automation.

**Repo:** `HappyCowboyAI/n8nWorkflows`
**Working directory:** `/Users/scottmetcalf/projects/n8n`
**Audience:** Backstory customers who want ready-to-import n8n automations

## Launch Workflows (6)

| # | Workflow | Category | Trigger | Output | Source ID |
|---|----------|----------|---------|--------|-----------|
| 01 | Sales Digest | Daily Intelligence | 6am weekday schedule | Slack DM | Sales Digest (active) |
| 02 | Meeting Brief | Daily Intelligence | Meeting Prep Cron (15-min) | Slack DM | Meeting Brief (active) |
| 03 | Silence Contract Monitor | Account Monitoring | Daily 6:30am schedule | Slack alert | Silence Contract Monitor (active) |
| 04 | Opportunity Discovery | Pipeline & Forecasting | Weekly schedule | Slack channel | Opportunity Discovery (active) |
| 05 | Forecast Coach | Pipeline & Forecasting | Weekly Monday schedule | Email | Forecast Coach (off) |
| 06 | Executive Inbox | Account Monitoring | Schedule trigger | Slack/Email | Executive Inbox (active) |

## Two Versions Per Workflow

- **Quick Start:** Minimal config — connect credentials, set one Slack channel, activate. Sensible defaults for everything else.
- **Full Version:** All features — region-based routing, team channels, caching, error handling, advanced formatting.

## Project Structure

```
n8n/
├── docs/
│   ├── index.html              # SPA (single-file, same pattern as LLM Skills)
│   ├── workflows.json          # Generated catalog data
│   └── build-catalog.py        # Builds workflows.json from workflow folders
├── 01-sales-digest/
│   ├── SOURCE.md               # Metadata, description, required credentials
│   ├── quickstart.json         # Minimal n8n export (credentials stripped)
│   ├── full.json               # Full version with all features
│   └── assets/                 # Screenshots, sample outputs
├── 02-meeting-brief/
│   └── ...
├── 03-silence-contract-monitor/
│   └── ...
├── 04-opportunity-discovery/
│   └── ...
├── 05-forecast-coach/
│   └── ...
├── 06-executive-inbox/
│   └── ...
└── README.md
```

## SPA Design

### Same design language as LLM Skills Catalog:
- Backstory branded header (dark blue gradient, logo)
- Category filter bar + search
- Card grid with workflow cards: name, description, trigger type badge, output destination badge, status
- Detail view with tabs

### Tabs per workflow:
| Tab | Content |
|-----|---------|
| **Setup** (default) | Animated walkthrough: import JSON -> connect credentials -> configure -> test |
| **Flow** | Animated node-graph visualization showing data flowing through the workflow |
| **Details** | Description, required credentials list, configuration options, sample output |

### Download buttons (replace "Copy Instructions"):
- "Download Quick Start" — minimal JSON
- "Download Full Version" — all features
- Both trigger a reminder: "Connect your own credentials after importing"

### Categories:
- **Daily Intelligence** — Sales Digest, Meeting Brief
- **Pipeline & Forecasting** — Opportunity Discovery, Forecast Coach
- **Account Monitoring** — Silence Contract Monitor, Executive Inbox

## Animated Flow Visualization

### Node-graph style (replaces platform mockups from LLM Skills):
- Dark background matching n8n's canvas aesthetic
- Rounded-rect nodes with icons, connected by curved lines
- Color-coded by node type:
  - **Green** — Triggers (schedule, webhook, Slack command)
  - **Blue** — Data fetch (Backstory API, Salesforce, Gmail)
  - **Purple** — AI processing (Claude, GPT)
  - **Orange** — Output (Slack, email, calendar)

### Animation sequence (example — Sales Digest):
1. Trigger node pulses green — "6am Weekday Trigger fires"
2. Line animates to Backstory MCP node (blue) — "Fetches account activity & engagement data"
3. Line flows to Claude node (purple) — "AI analyzes patterns, generates personalized digest"
4. Line flows to Slack node (orange) — "Delivers digest via Slack DM"
5. Sample output appears below (Slack message preview)

### Simplified view:
- 4-6 nodes max per workflow, showing conceptual flow
- Real workflows may have 20+ nodes; we show the meaningful steps

### Setup walkthrough (reuses animation engine):
1. n8n import screen — drag/drop or paste JSON
2. Credential setup — Backstory API key, Slack bot token, etc.
3. Configure — schedule, channel names, team mapping
4. Activate — toggle on and verify first run

## Credential Safety — Three Layers

### 1. Export sanitizer (Python script)
- Replaces credential values with placeholders (`YOUR_PEOPLE_AI_API_KEY`, `YOUR_SLACK_BOT_TOKEN`)
- Strips `credentials` objects from nodes (n8n reconnects on import)
- Removes org-specific URLs, webhook IDs, Supabase keys
- Removes hardcoded email addresses, Slack channel IDs, team names

### 2. Build-time validator (build-catalog.py)
- Regex scan of every JSON for credential patterns
- Flags JWT tokens (`eyJ...`), Slack tokens (`xoxb-`), OpenAI keys (`sk-`)
- Build fails with clear error if anything suspicious found

### 3. Manual review gate
- Export raw JSON from n8n
- Run sanitizer locally
- Owner reviews sanitized output
- Only then commit to repo

### Credential documentation (per workflow SOURCE.md):
```
## Required Credentials
- Backstory API Key (OAuth via MCP or REST API)
- Slack Bot Token (with chat:write, users:read scopes)
- Anthropic API Key (for Claude AI nodes)
```

## Cross-linking

- LLM Skills Catalog links to n8n Workflow Catalog ("See also: automated workflows")
- n8n Workflow Catalog links back ("See also: interactive AI skills")
- Same GitHub org, separate repos and sites
