#!/usr/bin/env python3
import os
import sys
import requests

GH_TOKEN = os.environ.get("GH_TOKEN")
REPO = "YoYoGames/GameMaker-Bugs"  # format: owner/repo

if not GH_TOKEN or not REPO:
    print("Please set GH_TOKEN and GH_REPO environment variables.", file=sys.stderr)
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

# Step 1: Get the issue node ID
print(f"[DEBUG] Getting node ID for issue #{issue_number}...")
resp = requests.get(
    f"https://api.github.com/repos/{REPO}/issues/{issue_number}",
    headers=headers
)
if resp.status_code != 200:
    print("[ERROR] Failed to fetch issue info:", resp.text, file=sys.stderr)
    sys.exit(1)

issue_node_id = resp.json().get("node_id")
if not issue_node_id:
    print("[ERROR] Could not get node_id for issue.", file=sys.stderr)
    sys.exit(1)
print(f"[DEBUG] Issue node ID: {issue_node_id}")

# Step 2: Iterate Project V2 items (paginated)
cursor = None
item_id = None
page_count = 0

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
        content = node.get("content")
        if content and content.get("id") == issue_node_id:
            item_id = node["id"]
            print(f"[DEBUG] Found project item ID: {item_id}")
            break

    if item_id:
        break

    page_info = data["data"]["node"]["items"]["pageInfo"]
    if not page_info["hasNextPage"]:
        break
    cursor = page_info["endCursor"]

if item_id:
    print(f"[DEBUG] Writing project item ID to GitHub output: {item_id}")
    with open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a") as f:
        f.write(f"item_id={item_id}\n")
else:
    print("Issue not found in project — skipping.")
