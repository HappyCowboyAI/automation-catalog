#!/usr/bin/env python3
"""
Inject documentation sticky notes into n8n workflow JSON exports.

Usage: python3 docs/add-sticky-notes.py <workflow-folder>
Example: python3 docs/add-sticky-notes.py 18-channel-pulse
"""
import json
import sys
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
            "Authenticates with Backstory, queries customer accounts and open renewals, "
            "then fetches Slack channel/user mappings to resolve posting targets."
        ),
        (
            "banner-ai", "3. AI-Powered Summarization", BLUE,
            380, 110, 1480, 160,
            "## 3. AI-Powered Summarization\n"
            "Loops through each account, builds a prompt with context, "
            "sends to Claude via Backstory MCP, then extracts and filters the response."
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
            "**START HERE:** Set your Backstory org ID, Slack bot token, "
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

    json_path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Injected {len(notes)} sticky notes into {json_path}")
    print(f"  Total nodes: {len(data['nodes'])}")
    return data


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 docs/add-sticky-notes.py <workflow-folder>")
        print("Example: python3 docs/add-sticky-notes.py 18-channel-pulse")
        sys.exit(1)
    inject_notes(sys.argv[1])
