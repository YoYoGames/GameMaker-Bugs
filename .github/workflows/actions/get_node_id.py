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


cursor = None
item_id = None
page_count = 0
MAX_ITEMS = 200 
items_checked = 0

while True:
    page_count += 1
    print(f"[DEBUG] Fetching project items page {page_count}, cursor={cursor}...")

    query = """
    query($project: ID!, $cursor: String) {
      node(id: $project) {
        ... on ProjectV2 {
          items(first: 100, after: $cursor) {
            pageInfo {
              hasNextPage
              endCursor
            }
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

    variables = {"project": project_id, "cursor": cursor}
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
    print(f"[DEBUG] Found {len(nodes)} items in this page.")

    for node in nodes:
        items_checked += 1
        content = node.get("content")
        if content and content.get("id") == issue_node_id:
            item_id = node["id"]
            print(f"[DEBUG] Found project item ID: {item_id}")
            break

    if item_id or items_checked >= MAX_ITEMS:
        break

    page_info = data["data"]["node"]["items"]["pageInfo"]
    if not page_info["hasNextPage"]:
        break
    cursor = page_info["endCursor"]

if item_id:
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"item_id={item_id}\n")
    print(f"[DEBUG] item_id={item_id}")
else:
    print(f"Issue not found in project (checked last {items_checked} items) — skipping.", file=sys.stderr)
    sys.exit(0)
