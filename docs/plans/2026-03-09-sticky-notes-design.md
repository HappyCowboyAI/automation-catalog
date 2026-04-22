# Workflow Sticky Notes Design

## Goal

Add sticky notes to n8n workflows that document what each section does, highlight setup steps, and warn about gotchas. Notes are added both to the exported catalog JSON and pushed to the live n8n instance.

## Audience

Both new users importing workflows and developers customizing them.

## Color System

| Color ID | Color  | Purpose                                      |
|----------|--------|----------------------------------------------|
| 1        | Blue   | Section banners — what a group of nodes does |
| 3        | Yellow | Setup callouts — credentials, config to change before first run |
| 4        | Orange | Warnings — rate limits, gotchas, failure modes |

## Placement Convention

- **Section banners (blue)**: Above the node group, spanning roughly the section width. Title + 2-3 line description.
- **Setup callouts (yellow)**: Below or beside the specific node they reference. Smaller.
- **Warning callouts (orange)**: Below or beside the specific node. Smaller.

## Channel Pulse (#18) — Sticky Notes

### Section Banners (blue)

1. **"1. Triggers & Configuration"** — above x=-1200 to -750
   - "Dual trigger: scheduled interval or on-demand webhook. Configuration node holds all tunables — update this first."

2. **"2. Data Gathering"** — above x=-750 to 370
   - "Authenticates with Backstory, queries customer accounts and open renewals, then fetches Slack channel/user mappings to resolve posting targets."

3. **"3. AI-Powered Summarization"** — above x=370 to 1840
   - "Loops through each account, builds a prompt with context, sends to Claude via Backstory MCP, then extracts and filters the response."

4. **"4. Delivery & Summary"** — above x=1840 to 2960
   - "Formats Slack message payload, posts to the mapped channel, loops to next account, then sends a run summary when complete."

### Setup Callouts (yellow)

5. **Configuration node** (x=-976)
   - "START HERE: Set your Backstory org ID, Slack bot token, and target account filters before first run."

6. **Anthropic Chat Model node** (x=1056)
   - "Set your LLM API key and model. Default: Claude. Swap for OpenAI/Gemini by replacing this node."

### Warning Callouts (orange)

7. **Post to Slack node** (x=2288)
   - "Slack rate limit: ~1 message/second. The batch loop handles this, but reduce batch size if you hit 429 errors."

## Implementation

1. Python script (`docs/add-sticky-notes.py`) that:
   - Reads a workflow `full.json`
   - Injects `n8n-nodes-base.stickyNote` nodes with correct positions, dimensions, colors, and markdown content
   - Writes updated JSON back

2. Push to production n8n instance via `PUT /api/v1/workflows/{id}` with the updated node list.

3. Save the annotated JSON to the catalog repo as the new `full.json`.

## Rollout

- **Phase 1**: Channel Pulse (#18) — prove the pattern
- **Phase 2**: Export and annotate high-value workflows (Sales Digest #01, etc.)
- **Phase 3**: Remaining workflows as they get exported

## n8n Sticky Note Node Schema

```json
{
  "id": "unique-id",
  "name": "Sticky Note",
  "type": "n8n-nodes-base.stickyNote",
  "position": [x, y],
  "typeVersion": 1,
  "parameters": {
    "content": "## Title\nMarkdown body",
    "height": 200,
    "width": 400,
    "color": 1
  }
}
```
