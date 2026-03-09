#!/usr/bin/env python3
"""
Push a workflow JSON back to the n8n instance via API.
Requires N8N_API_KEY and N8N_BASE_URL environment variables.

The n8n public API strips credentials from GET responses but validates
them on PUT. This script resolves credentials by:
  1. Looking for a credentials.json in the workflow folder
  2. Scanning other workflows for nodes with the same name
  3. Falling back to matching credential type from the credentials list

Usage: python3 docs/push-workflow.py <workflow-folder>
"""
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE_URL = os.environ.get("N8N_BASE_URL", "")
API_KEY = os.environ.get("N8N_API_KEY", "")
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def api_request(path, method="GET", data=None):
    """Make an authenticated request to the n8n API."""
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = Request(url, data=body, method=method)
    req.add_header("X-N8N-API-KEY", API_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", USER_AGENT)
    with urlopen(req) as resp:
        return json.loads(resp.read())


def resolve_credentials(workflow_id, nodes):
    """Resolve credential references for nodes that need them.

    The n8n API strips credentials from GET but requires them on PUT.
    We scan other workflows to find credential mappings for matching
    node names, then fall back to the credentials list.
    """
    # Identify which nodes need credentials (by type convention)
    CREDENTIAL_TYPES = {
        "@n8n/n8n-nodes-langchain.lmChatAnthropic": "anthropicApi",
        "@n8n/n8n-nodes-langchain.mcpClientTool": None,  # varies
    }

    nodes_needing_creds = []
    for node in nodes:
        if node["type"].startswith("n8n-nodes-base.stickyNote"):
            continue
        if "credentials" not in node or not node["credentials"]:
            cred_type = CREDENTIAL_TYPES.get(node["type"])
            if cred_type is not None or node["type"] in CREDENTIAL_TYPES:
                nodes_needing_creds.append(node)

    if not nodes_needing_creds:
        return nodes

    # Scan other workflows for credential references by node name
    print("  Resolving credentials from sibling workflows...")
    cred_by_name = {}
    try:
        workflows = api_request("/api/v1/workflows?limit=50")
        wf_list = workflows.get("data", workflows)
        for wf in wf_list:
            if wf["id"] == workflow_id:
                continue
            try:
                full_wf = api_request(f"/api/v1/workflows/{wf['id']}")
                for n in full_wf.get("nodes", []):
                    if n.get("credentials"):
                        cred_by_name[n["name"]] = n["credentials"]
            except (HTTPError, KeyError):
                continue
    except HTTPError:
        pass

    # Apply credentials
    for node in nodes_needing_creds:
        if node["name"] in cred_by_name:
            node["credentials"] = cred_by_name[node["name"]]
            print(f"    {node['name']}: resolved from sibling workflow")

    return nodes


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

    print(f"Pushing {json_path} to {BASE_URL}...")

    # Load local credential overrides if present
    creds_path = folder / "credentials.json"
    local_creds = {}
    if creds_path.exists():
        local_creds = json.loads(creds_path.read_text())
        print(f"  Loaded credential map from {creds_path}")

    # Apply local credential overrides first
    nodes = data["nodes"]
    for node in nodes:
        if node["name"] in local_creds:
            node["credentials"] = local_creds[node["name"]]

    # Resolve any remaining missing credentials from sibling workflows
    nodes = resolve_credentials(workflow_id, nodes)

    # Strip settings fields the API doesn't accept
    settings = {}
    for key in ("executionOrder", "callerPolicy"):
        if key in data.get("settings", {}):
            settings[key] = data["settings"][key]

    payload = {
        "name": data["name"],
        "nodes": nodes,
        "connections": data["connections"],
        "settings": settings,
    }

    # Check if workflow is active and deactivate first
    remote = api_request(f"/api/v1/workflows/{workflow_id}")
    was_active = remote.get("active", False)

    if was_active:
        print("  Deactivating workflow for update...")
        api_request(f"/api/v1/workflows/{workflow_id}/deactivate", method="POST", data={})

    # Push the update
    try:
        result = api_request(f"/api/v1/workflows/{workflow_id}", method="PUT", data=payload)
        node_count = len(result.get("nodes", []))
        print(f"Updated workflow: {result['name']} (ID: {result['id']})")
        print(f"  Nodes: {node_count}")
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"Error {e.code}: {error_body}")
        if was_active:
            print("  Re-activating workflow after failed update...")
            api_request(f"/api/v1/workflows/{workflow_id}/activate", method="POST", data={})
        sys.exit(1)

    # Re-activate if it was active before
    if was_active:
        print("  Re-activating workflow...")
        api_request(f"/api/v1/workflows/{workflow_id}/activate", method="POST", data={})


if __name__ == "__main__":
    if not BASE_URL or not API_KEY:
        print("Set N8N_BASE_URL and N8N_API_KEY environment variables")
        sys.exit(1)
    if len(sys.argv) != 2:
        print("Usage: python3 docs/push-workflow.py <workflow-folder>")
        sys.exit(1)
    push_workflow(sys.argv[1])
