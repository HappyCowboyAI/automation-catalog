# Workflow Sticky Notes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add documentation sticky notes to the Channel Pulse (#18) workflow JSON and push them to the live n8n instance.

**Architecture:** A Python script reads the workflow JSON, injects sticky note nodes at calculated positions, writes the updated JSON locally, then pushes via the n8n REST API. The script is reusable for future workflows.

**Tech Stack:** Python 3, n8n REST API (`PUT /api/v1/workflows/{id}`), curl

---

### Task 1: Create the sticky note injector script

**Files:**
- Create: `docs/add-sticky-notes.py`

**Step 1: Write the script**

```python
#!/usr/bin/env python3
"""
Inject documentation sticky notes into n8n workflow JSON exports.

Usage: python3 docs/add-sticky-notes.py <workflow-folder>
Example: python3 docs/add-sticky-notes.py 18-channel-pulse
"""
import json
import sys
import uuid
from pathlib import Path

# n8n sticky note color IDs
BLUE = 1      # Section banners
YELLOW = 3    # Setup callouts
ORANGE = 4    # Warnings

# Sticky note definitions per workflow
# Each note: (id_suffix, name, color, x, y, width, height, content)
WORKFLOW_NOTES = {
    "18-channel-pulse": [
        # Section banners (blue) — positioned above node groups
        (
            "banner-triggers", "1. Triggers & Configuration", BLUE,
            -1260, 140, 560, 160,
            "## 1. Triggers & Configuration\n"
            "Dual trigger: scheduled interval or on-demand webhook. "
            "The **Configuration** node holds all tunables — update it first."
        ),
        (
            "banner-data", "2. Data Gathering", BLUE,
            -760, 140, 1100, 160,
            "## 2. Data Gathering\n"
            "Authenticates with People.ai, queries customer accounts and open renewals, "
            "then fetches Slack channel/user mappings to resolve posting targets."
        ),
        (
            "banner-ai", "3. AI-Powered Summarization", BLUE,
            380, 110, 1480, 160,
            "## 3. AI-Powered Summarization\n"
            "Loops through each account, builds a prompt with context, "
            "sends to Claude via People.ai MCP, then extracts and filters the response."
        ),
        (
            "banner-delivery", "4. Delivery & Summary", BLUE,
            1880, 110, 1140, 160,
            "## 4. Delivery & Summary\n"
            "Formats Slack message payload, posts to the mapped channel, "
            "loops to next account, then sends a run summary when complete."
        ),
        # Setup callouts (yellow)
        (
            "setup-config", "Setup: Configuration", YELLOW,
            -1020, 560, 340, 140,
            "**START HERE:** Set your People.ai org ID, Slack bot token, "
            "and target account filters before first run."
        ),
        (
            "setup-llm", "Setup: LLM Model", YELLOW,
            1000, 660, 340, 140,
            "**LLM Setup:** Set your API key and model. Default: Claude. "
            "Swap for OpenAI/Gemini by replacing this node."
        ),
        # Warning callouts (orange)
        (
            "warn-slack-rate", "Warning: Slack Rate Limit", ORANGE,
            2240, 440, 340, 140,
            "**Rate Limit:** Slack allows ~1 msg/sec. "
            "The batch loop handles this, but reduce batch size if you hit 429 errors."
        ),
    ],
}


def make_sticky(id_suffix, name, color, x, y, width, height, content):
    """Create an n8n sticky note node dict."""
    return {
        "id": f"sticky-{id_suffix}",
        "name": name,
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": [x, y],
        "parameters": {
            "content": content,
            "height": height,
            "width": width,
            "color": color,
        },
    }


def inject_notes(workflow_folder):
    folder = Path(workflow_folder)
    json_path = folder / "full.json"

    if not json_path.exists():
        print(f"Error: {json_path} not found")
        sys.exit(1)

    folder_name = folder.name
    if folder_name not in WORKFLOW_NOTES:
        print(f"Error: No sticky note definitions for '{folder_name}'")
        sys.exit(1)

    data = json.loads(json_path.read_text())

    # Remove any existing sticky notes (idempotent)
    data["nodes"] = [
        n for n in data["nodes"]
        if n.get("type") != "n8n-nodes-base.stickyNote"
    ]

    # Add sticky notes
    notes = WORKFLOW_NOTES[folder_name]
    for note_args in notes:
        data["nodes"].append(make_sticky(*note_args))

    json_path.write_text(json.dumps(data, indent=2))
    print(f"Injected {len(notes)} sticky notes into {json_path}")
    print(f"  Total nodes: {len(data['nodes'])}")
    return data


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 docs/add-sticky-notes.py <workflow-folder>")
        print("Example: python3 docs/add-sticky-notes.py 18-channel-pulse")
        sys.exit(1)
    inject_notes(sys.argv[1])
```

**Step 2: Run the script on Channel Pulse**

Run: `python3 docs/add-sticky-notes.py 18-channel-pulse`
Expected: "Injected 7 sticky notes into 18-channel-pulse/full.json" and "Total nodes: 29"

**Step 3: Verify the output JSON is valid**

Run: `python3 -c "import json; d=json.load(open('18-channel-pulse/full.json')); stickies=[n for n in d['nodes'] if 'sticky' in n['type']]; print(f'Sticky notes: {len(stickies)}'); [print(f'  {s[\"name\"]} (color={s[\"parameters\"][\"color\"]})') for s in stickies]"`
Expected: 7 sticky notes listed with correct colors (1=blue, 3=yellow, 4=orange)

**Step 4: Commit**

```bash
git add docs/add-sticky-notes.py 18-channel-pulse/full.json
git commit -m "feat: add sticky note injector and annotate Channel Pulse (#18)"
```

---

### Task 2: Push annotated workflow to production n8n

**Files:**
- Create: `docs/push-workflow.py`

**Step 1: Write the push script**

```python
#!/usr/bin/env python3
"""
Push a workflow JSON back to the n8n instance via API.
Requires N8N_API_KEY and N8N_BASE_URL environment variables.

Usage: python3 docs/push-workflow.py <workflow-folder>
"""
import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen

BASE_URL = os.environ.get("N8N_BASE_URL", "")
API_KEY = os.environ.get("N8N_API_KEY", "")
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def push_workflow(workflow_folder):
    folder = Path(workflow_folder)
    json_path = folder / "full.json"

    if not json_path.exists():
        print(f"Error: {json_path} not found")
        sys.exit(1)

    data = json.loads(json_path.read_text())
    workflow_id = data.get("id")
    if not workflow_id:
        print("Error: No workflow ID found in JSON")
        sys.exit(1)

    # n8n PUT API expects only nodes and connections (plus name)
    payload = {
        "name": data["name"],
        "nodes": data["nodes"],
        "connections": data["connections"],
        "settings": data.get("settings", {}),
    }

    url = f"{BASE_URL}/api/v1/workflows/{workflow_id}"
    body = json.dumps(payload).encode("utf-8")

    req = Request(url, data=body, method="PUT")
    req.add_header("X-N8N-API-KEY", API_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", USER_AGENT)

    with urlopen(req) as resp:
        result = json.loads(resp.read())
        print(f"Updated workflow: {result['name']} (ID: {result['id']})")
        node_count = len(result.get("nodes", []))
        print(f"  Nodes: {node_count}")


if __name__ == "__main__":
    if not BASE_URL or not API_KEY:
        print("Set N8N_BASE_URL and N8N_API_KEY environment variables")
        sys.exit(1)
    if len(sys.argv) != 2:
        print("Usage: python3 docs/push-workflow.py <workflow-folder>")
        sys.exit(1)
    push_workflow(sys.argv[1])
```

**Step 2: Push Channel Pulse to production**

Run:
```bash
N8N_BASE_URL=https://scottai.trackslife.com \
N8N_API_KEY=<key> \
python3 docs/push-workflow.py 18-channel-pulse
```
Expected: "Updated workflow: Weekly Channel Updates v3 (API-Driven) (ID: GEVPltWL6r4SIIaW)" and "Nodes: 29"

**Step 3: Verify by fetching the workflow back**

Run:
```bash
curl -s \
  -H "X-N8N-API-KEY: <key>" \
  -H "User-Agent: Mozilla/5.0 ..." \
  "https://scottai.trackslife.com/api/v1/workflows/GEVPltWL6r4SIIaW" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Nodes: {len(d[\"nodes\"])}'); print(f'Stickies: {len([n for n in d[\"nodes\"] if \"sticky\" in n[\"type\"]])}')"
```
Expected: "Nodes: 29" and "Stickies: 7"

**Step 4: Commit**

```bash
git add docs/push-workflow.py
git commit -m "feat: add workflow push script for n8n API"
```

---

### Task 3: Update catalog and push to GitHub

**Step 1: Rebuild the catalog**

Run: `python3 docs/build-catalog.py`
Expected: "Generated docs/workflows.json with 18 workflow(s)"

**Step 2: Commit and push**

```bash
git add docs/workflows.json
git commit -m "docs: rebuild catalog with annotated Channel Pulse"
git push origin main
```
