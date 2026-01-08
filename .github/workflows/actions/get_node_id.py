#!/usr/bin/env python3
import os
import sys
import requests

GH_TOKEN = os.environ.get("GH_TOKEN")
REPO = "YoYoGames/GameMaker-Bugs"  

if not GH_TOKEN:
    print("Please set GH_TOKEN environment variable.", file=sys.stderr)
    sys.exit(1)

if len(sys.argv) < 3:
    print("Usage: get_project_item.py <issue_number> <project_id>", file=sys.stderr)
    sys.exit(1)

issue_number = sys.argv[1]
project_id = sys.argv[2]

headers = {
    "Authorization": f"Bearer {GH_TOKEN}",
    "Accept": "application/vnd.github+json",
}

print(f"[DEBUG] Getting node ID for issue #{issue_number}...")
resp = requests.get(
    f"https://api.github.com/repos/{REPO}/issues/{issue_number}",
    headers=headers,
    timeout=30
)
if resp.status_code != 200:
    print("[ERROR] Failed to fetch issue info:", resp.text, file=sys.stderr)
    sys.exit(1)

issue_node_id = resp.json().get("node_id")
if not issue_node_id:
    print("[ERROR] Could not get node_id for issue.", file=sys.stderr)
    sys.exit(1)
print(f"[DEBUG] Issue node ID: {issue_node_id}")

query = """
query($project: ID!, $issueNodeId: ID!) {
  node(id: $project) {
    ... on ProjectV2 {
      items(first: 1, filterBy: {contentId: $issueNodeId}) {
        nodes {
          id
          content {
            ... on Issue {
              id
              number
              title
            }
          }
        }
      }
    }
  }
}
"""
variables = {"project": project_id, "issueNodeId": issue_node_id}

print("[DEBUG] Querying project for this issue...")
r = requests.post(
    "https://api.github.com/graphql",
    headers=headers,
    json={"query": query, "variables": variables},
    timeout=30
)
if r.status_code != 200:
    print("[ERROR] GraphQL query failed:", r.text, file=sys.stderr)
    sys.exit(1)

data = r.json()
if "errors" in data:
    print("[ERROR] GraphQL returned errors:", data["errors"], file=sys.stderr)
    sys.exit(1)

nodes = data["data"]["node"]["items"]["nodes"]
if nodes:
    item_id = nodes[0]["id"]
    print(f"[DEBUG] Found project item ID: {item_id}")

    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"item_id={item_id}\n")
    print(f"[DEBUG] item_id={item_id}")
else:
    print("Issue not found in project — skipping.", file=sys.stderr)
    sys.exit(0)
