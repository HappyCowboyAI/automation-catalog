#!/usr/bin/env python3
"""
Export workflows from n8n and sanitize them.
Requires N8N_API_KEY and N8N_BASE_URL environment variables.

Usage: python3 export-workflows.py
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen

WORKFLOW_MAP = {
    # n8n workflow ID -> (folder, version)
    # FILL IN with your workflow IDs before running
    # 'WORKFLOW_ID': ('01-sales-digest', 'full'),
}

BASE_URL = os.environ.get('N8N_BASE_URL', '')
API_KEY = os.environ.get('N8N_API_KEY', '')


def export_workflow(workflow_id):
    req = Request(f'{BASE_URL}/api/v1/workflows/{workflow_id}')
    req.add_header('X-N8N-API-KEY', API_KEY)
    with urlopen(req) as resp:
        return json.loads(resp.read())


def main():
    if not BASE_URL or not API_KEY:
        print("Set N8N_BASE_URL and N8N_API_KEY environment variables")
        sys.exit(1)

    for wf_id, (folder, version) in WORKFLOW_MAP.items():
        print(f"Exporting {folder}/{version}.json ...")
        data = export_workflow(wf_id)
        raw_path = Path(f'/tmp/{folder}-{version}-raw.json')
        raw_path.write_text(json.dumps(data, indent=2))
        out_path = Path(folder) / f'{version}.json'
        out_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            'python3', 'docs/sanitize-export.py',
            str(raw_path), str(out_path)
        ], check=True)

    print("\nDone. REVIEW ALL OUTPUT FILES before committing.")


if __name__ == '__main__':
    main()
