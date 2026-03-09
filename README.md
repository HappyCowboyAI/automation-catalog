# People.ai Automation Catalog

Ready-to-import workflow automations powered by People.ai. Each workflow connects People.ai CRM intelligence with AI analysis to automate sales workflows.

## Workflows

| # | Workflow | Category | Trigger | Output |
|---|---------|----------|---------|--------|
| 01 | Sales Digest | Daily Intelligence | 6am weekday | Slack DM |
| 02 | Meeting Brief | Daily Intelligence | 15-min cron | Slack DM |
| 03 | Silence Contract Monitor | Account Monitoring | Daily 6:30am | Slack alert |
| 04 | Opportunity Discovery | Pipeline & Forecasting | Weekly | Slack channel |
| 05 | Forecast Coach | Pipeline & Forecasting | Weekly Monday | Email |
| 06 | Executive Inbox | Account Monitoring | Schedule | Slack/Email |

## Getting Started

1. Browse the [catalog](https://happycowboyai.github.io/automation-catalog/)
2. Download a workflow JSON (Quick Start or Full version)
3. Import into your automation platform
4. Connect your credentials (People.ai API, Slack, Anthropic, etc.)
5. Configure and activate

## Prerequisites

- Automation platform (self-hosted or cloud)
- People.ai account with API/MCP access
- Anthropic API key (for Claude AI nodes)
- Slack workspace with bot token

## Adding New Workflows

1. Create a numbered folder (e.g., `07-new-workflow/`)
2. Add `SOURCE.md` with metadata
3. Export workflow from your platform, sanitize with `docs/sanitize-export.py`
4. Review sanitized JSON for any remaining sensitive data
5. Run `python3 docs/build-catalog.py` to rebuild the catalog

## Credential Safety

All workflow exports are sanitized to remove API keys, tokens, and org-specific data. The build script validates every JSON file for credential patterns before generating the catalog.

## See Also

- [People.ai LLM Skills Catalog](https://happycowboyai.github.io/LLMSkills/) — Interactive AI skills powered by People.ai MCP
