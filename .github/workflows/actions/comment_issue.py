#!/usr/bin/env python3
"""
Move GitHub ProjectV2 issue from Backlog to Triage based on comment.
If the issue is not in the project, add it first.
"""

import os
import sys
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG = "YoYoGames"
REPO = "GameMaker-Bugs"
COMMENT_BODY = "https://api.gamemaker.io/api/github/downloads/"
ISSUE_NUMBER = os.getenv("ISSUE_NUMBER")
if ISSUE_NUMBER:
    ISSUE_NUMBER = int(ISSUE_NUMBER)
PROJECT_NUMBER = int(os.getenv("PROJECT_NUMBER", 17)) 
STATUS_FIELD_NAME = "Status"
TARGET_URL = "https://api.gamemaker.io/api/github/downloads/"

GRAPHQL_URL = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Content-Type": "application/json"}

if not all([GITHUB_TOKEN, ORG, REPO, COMMENT_BODY, ISSUE_NUMBER]):
    sys.exit("❌ Missing required environment variables")

if TARGET_URL.lower() not in COMMENT_BODY.lower():
    print("ℹ️ Comment does not contain sample link. Exiting.")
    sys.exit(0)

def gql(query: str, variables: dict):
    resp = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": query, "variables": variables})
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]

print("🔎 Updating issue labels...")
labels_query = gql(
    """
    query ($owner: String!, $repo: String!, $number: Int!) {
      repository(owner: $owner, name: $repo) {
        issue(number: $number) {
          id
          labels(first: 50) {
            nodes { name }
          }
        }
      }
    }
    """,
    {"owner": ORG, "repo": REPO, "number": ISSUE_NUMBER}
)

issue_labels = [l["name"] for l in labels_query["repository"]["issue"]["labels"]["nodes"]]

new_labels = [l for l in issue_labels if l != "project_required"]
if "project" not in new_labels:
    new_labels.append("project")

update_labels_resp = requests.post(
    f"https://api.github.com/repos/{ORG}/{REPO}/issues/{ISSUE_NUMBER}/labels",
    headers={"Authorization": f"token {GITHUB_TOKEN}"},
    json={"labels": new_labels}
)
if update_labels_resp.status_code not in [200, 201]:
    print("❌ Failed to update labels")
else:
    print(f"✅ Updated labels for issue #{ISSUE_NUMBER}: {new_labels}")

print("🔎 Loading project metadata...")
project_data = gql(
    """
    query ($org: String!, $number: Int!) {
      organization(login: $org) {
        projectV2(number: $number) {
          id
          fields(first: 50) {
            nodes {
              __typename
              ... on ProjectV2SingleSelectField {
                id
                name
                options {
                  id
                  name
                }
              }
            }
          }
        }
      }
    }
    """,
    {"org": ORG, "number": PROJECT_NUMBER},
)

project = project_data["organization"]["projectV2"]
if not project:
    sys.exit("❌ ProjectV2 not found")

status_field = next(
    (f for f in project["fields"]["nodes"]
     if f.get("__typename") == "ProjectV2SingleSelectField"
     and f.get("name") == STATUS_FIELD_NAME),
    None
)
if not status_field:
    sys.exit(f"❌ Status field '{STATUS_FIELD_NAME}' not found in project")

triage_option = next(
    (o for o in status_field["options"] if o["name"].lower() == "triage"),
    None
)
if not triage_option:
    sys.exit("❌ Triage option not found in Status field")

issue_data = gql(
    """
    query ($owner: String!, $repo: String!, $number: Int!) {
      repository(owner: $owner, name: $repo) {
        issue(number: $number) {
          id
          number
          title
        }
      }
    }
    """,
    {"owner": ORG, "repo": REPO, "number": ISSUE_NUMBER},
)
issue_node_id = issue_data["repository"]["issue"]["id"]

project_items = gql(
    """
    query ($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          items(first: 100) {
            nodes {
              id
              content {
                __typename
                ... on Issue {
                  id
                  number
                }
              }
            }
          }
        }
      }
    }
    """,
    {"projectId": project["id"]}
)

items = project_items["node"]["items"]["nodes"]
existing_item = next(
    (i for i in items
     if i["content"]
     and i["content"].get("__typename") == "Issue"
     and i["content"].get("number") == ISSUE_NUMBER),
    None
)

if existing_item:
    item_id = existing_item["id"]
    print(f"✅ Found issue in ProjectV2, item ID: {item_id}")
else:
    add_item = gql(
        """
        mutation ($projectId: ID!, $contentId: ID!) {
          addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
            item { id }
          }
        }
        """,
        {"projectId": project["id"], "contentId": issue_node_id},
    )
    item_id = add_item["addProjectV2ItemById"]["item"]["id"]
    print(f"✅ Added issue to ProjectV2, item ID: {item_id}")

print(f"🔎 Updating Status field to 'Triage'...")
mutation_status = """
mutation ($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: $projectId,
      itemId: $itemId,
      fieldId: $fieldId,
      value: { singleSelectOptionId: $optionId }
    }
  ) {
    projectV2Item { id }
  }
}
"""
update_field = gql(
    mutation_status,
    {
        "projectId": project["id"],
        "itemId": item_id,
        "fieldId": status_field["id"],
        "optionId": triage_option["id"],  
    },
)

print(f"✅ Issue #{ISSUE_NUMBER} moved to Triage in ProjectV2 #{PROJECT_NUMBER}")
