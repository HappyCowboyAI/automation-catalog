#!/usr/bin/env python3
"""
Sanitize workflow JSON exports by stripping credentials,
org-specific data, and sensitive values.

Usage: python3 sanitize-export.py input.json output.json
"""
import json
import re
import sys
from pathlib import Path

CREDENTIAL_PATTERNS = [
    (r'eyJ[A-Za-z0-9_-]{20,}', 'JWT token'),
    (r'xoxb-[0-9A-Za-z-]+', 'Slack bot token'),
    (r'xoxp-[0-9A-Za-z-]+', 'Slack user token'),
    (r'sk-[A-Za-z0-9]{20,}', 'OpenAI/Anthropic API key'),
    (r'sk-ant-[A-Za-z0-9-]+', 'Anthropic API key'),
    (r'ghp_[A-Za-z0-9]{36}', 'GitHub token'),
    (r'gho_[A-Za-z0-9]{36}', 'GitHub OAuth token'),
]

STRIP_FIELDS = ['credentials', 'webhookId']

ORG_PATTERNS = [
    (r'scott\.metcalf@people\.ai', 'YOUR_EMAIL'),
    (r'scottai\.trackslife\.com', 'YOUR_N8N_INSTANCE'),
]


def sanitize(data):
    if 'pinData' in data:
        del data['pinData']
    for node in data.get('nodes', []):
        for field in STRIP_FIELDS:
            if field in node:
                del node[field]
        sanitize_params(node.get('parameters', {}))
    return data


def sanitize_params(params):
    if isinstance(params, dict):
        for key, value in params.items():
            if isinstance(value, str):
                params[key] = sanitize_string(value, key)
            elif isinstance(value, (dict, list)):
                sanitize_params(value)
    elif isinstance(params, list):
        for i, item in enumerate(params):
            if isinstance(item, str):
                params[i] = sanitize_string(item, '')
            elif isinstance(item, (dict, list)):
                sanitize_params(item)


def sanitize_string(value, field_name):
    for pattern, replacement in ORG_PATTERNS:
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
    return value


def validate(data):
    text = json.dumps(data)
    issues = []
    for pattern, name in CREDENTIAL_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            issues.append(f"Found {name}: {matches[0][:20]}...")
    return issues


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 sanitize-export.py input.json output.json")
        sys.exit(1)

    input_path, output_path = Path(sys.argv[1]), Path(sys.argv[2])
    data = json.loads(input_path.read_text())

    data = sanitize(data)
    issues = validate(data)

    if issues:
        print("CREDENTIAL LEAK DETECTED - not writing output:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)

    Path(output_path).write_text(json.dumps(data, indent=2))
    print(f"Sanitized: {input_path} -> {output_path}")
    print(f"  Nodes: {len(data.get('nodes', []))}")
    print(f"  Credentials stripped: yes")
    print(f"  Validation: passed")


if __name__ == '__main__':
    main()
