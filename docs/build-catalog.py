#!/usr/bin/env python3
"""
Build the workflow catalog (workflows.json) by reading workflow folders,
parsing SOURCE.md metadata, validating JSON exports, and assembling
a single catalog file.

Usage: python3 docs/build-catalog.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent

CATEGORIES = [
    {"id": "daily-intelligence", "name": "Daily Intelligence", "icon": "sun"},
    {"id": "pipeline-forecasting", "name": "Pipeline & Forecasting", "icon": "trending-up"},
    {"id": "account-monitoring", "name": "Account Monitoring", "icon": "shield"},
]

CATEGORY_IDS = {c["id"] for c in CATEGORIES}

CREDENTIAL_PATTERNS = [
    (r'eyJ[A-Za-z0-9_-]{20,}', 'JWT token'),
    (r'xoxb-[0-9A-Za-z-]+', 'Slack bot token'),
    (r'sk-[A-Za-z0-9]{20,}', 'OpenAI/Anthropic API key'),
    (r'sk-ant-[A-Za-z0-9-]+', 'Anthropic API key'),
]

# Keywords used to classify node types
NODE_TYPE_KEYWORDS = {
    "trigger": ["trigger", "schedule", "cron", "webhook"],
    "data":    ["people.ai", "mcp", "fetch", "get", "query", "gmail", "api"],
    "ai":      ["claude", "ai", "agent", "gpt", "anthropic", "analyze"],
    "output":  ["slack", "email", "send", "deliver", "post", "alert"],
}

NODE_TYPE_COLORS = {
    "trigger": "green",
    "data":    "blue",
    "ai":      "purple",
    "output":  "orange",
}


# ---------------------------------------------------------------------------
# SOURCE.md parsing
# ---------------------------------------------------------------------------

def parse_source_md(text: str) -> dict:
    """Parse a SOURCE.md file into a metadata dict.

    Supports two flavours:
    1. The canonical format with explicit ## Category, ## Trigger, etc.
    2. The legacy format that uses an Overview table and different heading names.
    """
    meta: dict = {}

    # --- Name (first H1) ---
    m = re.search(r'^#\s+(.+)', text, re.MULTILINE)
    if m:
        # Strip leading number prefix like "01 — "
        raw_name = m.group(1).strip()
        raw_name = re.sub(r'^\d+\s*[—–-]\s*', '', raw_name)
        meta["name"] = raw_name

    sections = _split_sections(text)

    # --- Description ---
    meta["description"] = (
        sections.get("description", "") or
        sections.get("overview", "")
    ).strip()
    # If description came from overview table, extract prose after the table
    if "overview" in sections and not sections.get("description"):
        desc = sections["overview"]
        # Remove markdown table lines
        lines = [l for l in desc.splitlines() if not re.match(r'^\s*\|', l)]
        meta["description"] = "\n".join(lines).strip()

    # Also look for a standalone Description section below Overview
    if not meta["description"]:
        meta["description"] = sections.get("description", "").strip()

    # --- Category ---
    cat_raw = sections.get("category", "").strip().lower()
    if cat_raw in CATEGORY_IDS:
        meta["category"] = cat_raw
    else:
        # Try to infer from name / description
        meta["category"] = _infer_category(
            meta.get("name", "") + " " + meta.get("description", "")
        )

    # --- Trigger ---
    meta["trigger"] = sections.get("trigger", "").strip()
    if not meta["trigger"]:
        # Try extracting from overview table
        m = re.search(r'\*\*Trigger\*\*\s*\|\s*(.+)', text)
        if m:
            meta["trigger"] = m.group(1).strip()

    # --- Output ---
    meta["output"] = sections.get("output", "").strip()

    # --- Required Credentials ---
    creds_text = (
        sections.get("required credentials", "") or
        sections.get("credentials required", "")
    )
    meta["credentials"] = _parse_bullet_list(creds_text)
    if not meta["credentials"]:
        # Try overview table
        m = re.search(r'\*\*Credentials\*\*\s*\|\s*(.+)', text)
        if m:
            meta["credentials"] = [
                c.strip() for c in m.group(1).split(",")
            ]

    # --- Node Flow ---
    node_flow_text = sections.get("node flow", "")
    meta["node_flow"] = _parse_node_flow(node_flow_text)

    # --- Configuration ---
    meta["configuration"] = _parse_bullet_list(
        sections.get("configuration", "")
    )

    # --- Quick Start vs Full ---
    meta["quick_start_vs_full"] = sections.get(
        "quick start vs full", ""
    ).strip()

    return meta


def _split_sections(text: str) -> dict:
    """Split markdown text into {heading_lower: body} for ## headings."""
    parts: dict = {}
    current_heading = None
    current_lines: list = []
    for line in text.splitlines():
        m = re.match(r'^##\s+(.+)', line)
        if m:
            if current_heading is not None:
                parts[current_heading] = "\n".join(current_lines)
            current_heading = m.group(1).strip().lower()
            current_lines = []
        else:
            current_lines.append(line)
    if current_heading is not None:
        parts[current_heading] = "\n".join(current_lines)
    return parts


def _parse_bullet_list(text: str) -> list:
    """Extract bullet items from markdown text."""
    items = []
    for line in text.splitlines():
        m = re.match(r'^\s*[-*]\s+(.+)', line)
        if m:
            # Strip bold markers for cleaner output
            item = re.sub(r'\*\*(.+?)\*\*', r'\1', m.group(1)).strip()
            items.append(item)
    return items


def _parse_node_flow(text: str) -> list:
    """Parse numbered node flow list and classify each node."""
    nodes = []
    for line in text.splitlines():
        m = re.match(r'^\s*(\d+)\.\s+\*\*(.+?)\*\*\s*[—–-]\s*(.+)', line)
        if not m:
            m = re.match(r'^\s*(\d+)\.\s+(.+?)\s*[—–-]\s*(.+)', line)
        if m:
            name = m.group(2).strip()
            description = m.group(3).strip()
            node_type = _classify_node(name, description)
            nodes.append({
                "step": int(m.group(1)),
                "name": name,
                "description": description,
                "type": node_type,
                "color": NODE_TYPE_COLORS.get(node_type, "gray"),
            })
    return nodes


def _classify_node(name: str, description: str) -> str:
    """Classify a node type based on keywords in name and description."""
    combined = (name + " " + description).lower()
    # Check in priority order: trigger first, then output, ai, data
    for ntype in ["trigger", "output", "ai", "data"]:
        for kw in NODE_TYPE_KEYWORDS[ntype]:
            if kw in combined:
                return ntype
    return "data"  # default


def _infer_category(text: str) -> str:
    """Best-effort category inference from text."""
    t = text.lower()
    if any(kw in t for kw in ["digest", "daily", "morning", "intelligence"]):
        return "daily-intelligence"
    if any(kw in t for kw in ["pipeline", "forecast", "deal", "revenue"]):
        return "pipeline-forecasting"
    if any(kw in t for kw in ["account", "monitor", "alert", "watch"]):
        return "account-monitoring"
    return "daily-intelligence"  # fallback


# ---------------------------------------------------------------------------
# JSON export validation
# ---------------------------------------------------------------------------

def validate_json_export(path: Path) -> list:
    """Check a JSON export for leaked credentials. Returns list of issues."""
    text = path.read_text()
    issues = []
    for pattern, label in CREDENTIAL_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            issues.append(
                f"{path.name}: found {label} ({matches[0][:20]}...)"
            )
    return issues


# ---------------------------------------------------------------------------
# Catalog builder
# ---------------------------------------------------------------------------

def discover_workflows() -> list:
    """Find workflow folders (directories matching NN-name pattern)."""
    folders = []
    for entry in sorted(REPO_ROOT.iterdir()):
        if entry.is_dir() and re.match(r'^\d{2}-', entry.name):
            folders.append(entry)
    return folders


def build_workflow_entry(folder: Path) -> dict | None:
    """Build a single workflow catalog entry from a folder."""
    source_path = folder / "SOURCE.md"
    if not source_path.exists():
        print(f"  SKIP {folder.name}: no SOURCE.md")
        return None

    text = source_path.read_text()
    meta = parse_source_md(text)

    # Collect and validate JSON exports
    json_files = sorted(folder.glob("*.json"))
    all_issues: list = []
    export_names: list = []
    for jf in json_files:
        issues = validate_json_export(jf)
        all_issues.extend(issues)
        export_names.append(jf.name)

    if all_issues:
        print(f"  FAIL {folder.name}: credential leak detected!")
        for issue in all_issues:
            print(f"    - {issue}")
        return None  # will cause a hard fail later

    entry = {
        "id": folder.name,
        "name": meta.get("name", folder.name),
        "description": meta.get("description", ""),
        "category": meta.get("category", ""),
        "trigger": meta.get("trigger", ""),
        "output": meta.get("output", ""),
        "credentials": meta.get("credentials", []),
        "node_flow": meta.get("node_flow", []),
        "configuration": meta.get("configuration", []),
        "quick_start_vs_full": meta.get("quick_start_vs_full", ""),
        "exports": export_names,
    }
    return entry


def build_catalog() -> dict:
    """Build the full catalog dict."""
    folders = discover_workflows()
    workflows = []
    credential_failures = []

    for folder in folders:
        print(f"Processing {folder.name} ...")
        entry = build_workflow_entry(folder)
        if entry is None and (folder / "SOURCE.md").exists():
            # SOURCE.md exists but validation failed -> credential leak
            credential_failures.append(folder.name)
        elif entry is not None:
            workflows.append(entry)

    catalog = {
        "_generated": datetime.now(timezone.utc).isoformat(),
        "_generator": "docs/build-catalog.py",
        "categories": CATEGORIES,
        "workflows": workflows,
    }
    return catalog, credential_failures


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Building workflow catalog from {REPO_ROOT}\n")

    catalog, credential_failures = build_catalog()

    if credential_failures:
        print(f"\nFAILED: credential leaks found in: {credential_failures}")
        sys.exit(1)

    out_path = REPO_ROOT / "docs" / "workflows.json"
    out_path.write_text(json.dumps(catalog, indent=2) + "\n")

    wf_count = len(catalog["workflows"])
    print(f"\nGenerated {out_path} with {wf_count} workflow(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
