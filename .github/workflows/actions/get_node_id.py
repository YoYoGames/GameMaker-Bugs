#!/usr/bin/env python3
import os
import sys
import requests

GH_TOKEN = os.environ.get("GH_TOKEN")
REPO = "YoYoGames/GameMaker-Bugs"

if not GH_TOKEN:
    print("Please set GH_TOKEN environment variable.", file=sys.stderr)
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: get_project_item.py <issue_number>", file=sys.stderr)
    sys.exit(1)

issue_number = sys.argv[1]

headers = {
    "Authorization": f"Bearer {GH_TOKEN}",
    "Accept": "application/vnd.github+json",
}

resp = requests.get(f"https://api.github.com/repos/{REPO}/issues/{issue_number}", headers=headers)
if resp.status_code != 200:
    print("[ERROR] Failed to fetch issue info:", resp.text, file=sys.stderr)
    sys.exit(1)

issue_node_id = resp.json().get("node_id")
if not issue_node_id:
    print("[ERROR] Could not get node_id for issue.", file=sys.stderr)
    sys.exit(1)
print(f"[DEBUG] Issue node ID: {issue_node_id}")

query = """
query($issueId: ID!) {
  node(id: $issueId) {
    ... on Issue {
      projectItems(first: 10) {
        nodes {
          id
          project {
            id
            title
          }
        }
      }
    }
  }
}
"""
variables = {"issueId": issue_node_id}
r = requests.post("https://api.github.com/graphql", headers=headers, json={"query": query, "variables": variables}, timeout=30)

if r.status_code != 200:
    print("[ERROR] GraphQL query failed:", r.text, file=sys.stderr)
    sys.exit(1)

data = r.json()
if "errors" in data:
    print("[ERROR] GraphQL returned errors:", data["errors"], file=sys.stderr)
    sys.exit(1)

nodes = data["data"]["node"]["projectItems"]["nodes"]
print(f"[DEBUG] Found {len(nodes)} project items for this issue.")

item_id = None
for node in nodes:
    item_id = node["id"]
    project_title = node["project"]["title"]
    print(f"[DEBUG] Found project item ID: {item_id} in project '{project_title}'")
    break  

if item_id:
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"item_id={item_id}\n")
    print(f"[DEBUG] item_id={item_id}")
else:
    print("Issue is not in any project — skipping.", file=sys.stderr)
    sys.exit(0)
