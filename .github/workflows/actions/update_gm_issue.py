#!/usr/bin/env python3
"""Handle the one-shot `update_gm` issue-label automation."""

import json
import os
import sys
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen


API_URL = "https://api.github.com"
GRAPHQL_URL = f"{API_URL}/graphql"
COMMENT_MARKER = "<!-- update-gm-comment -->"
COMMENT_BODY = f"""{COMMENT_MARKER}

You have reported this using an old and now-unsupported version of GameMaker, so this report will be closed just now. It's very likely you will find this issue has already been fixed in the current version, so please move to that version as soon as it's convenient.

Whenever you're ready to get the new version you can find download links and release information by visiting [https://releases.gamemaker.io/](https://releases.gamemaker.io/) - we always suggest using the newest LTS release. (Betas if you want.)

While you're downloading and installing that new version, ensure you also check its Required SDKs wiki page and the permissions guide. Links to both of these can also be found on the release notes page mentioned above.
"""


def request(token, method, url, payload=None, expected=(200,)):
    """Send an authenticated GitHub API request and decode its JSON response."""
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = Request(
        url,
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    try:
        with urlopen(req, timeout=30) as response:
            status = response.status
            response_body = response.read().decode("utf-8")
    except HTTPError as error:
        status = error.code
        response_body = error.read().decode("utf-8")

    if status not in expected:
        raise RuntimeError(
            f"GitHub API request failed ({method} {url}, HTTP {status}): "
            f"{response_body}"
        )

    return (json.loads(response_body) if response_body else None), status


def graphql(token, query, variables):
    """Run a GraphQL request and fail on either HTTP or GraphQL errors."""
    response, _ = request(
        token,
        "POST",
        GRAPHQL_URL,
        {"query": query, "variables": variables},
    )
    if response.get("errors"):
        raise RuntimeError(f"GitHub GraphQL request failed: {response['errors']}")
    return response["data"]


def comment_exists(token, repository, issue_number):
    """Check every issue-comment page for this automation's marker."""
    page = 1
    while True:
        comments, _ = request(
            token,
            "GET",
            f"{API_URL}/repos/{repository}/issues/{issue_number}/comments"
            f"?per_page=100&page={page}",
        )
        if any(COMMENT_MARKER in comment.get("body", "") for comment in comments):
            return True
        if len(comments) < 100:
            return False
        page += 1


def get_issue_and_project(token, owner, repository_name, issue_number, project_number):
    query = """
    query($owner: String!, $repository: String!, $issue: Int!, $project: Int!) {
      repository(owner: $owner, name: $repository) {
        issue(number: $issue) {
          id
          state
          stateReason
          projectItems(first: 50) {
            nodes {
              id
              project { id }
            }
          }
        }
      }
      organization(login: $owner) {
        projectV2(number: $project) {
          id
          fields(first: 50) {
            nodes {
              __typename
              ... on ProjectV2SingleSelectField {
                id
                name
                options { id name }
              }
            }
          }
        }
      }
    }
    """
    data = graphql(
        token,
        query,
        {
            "owner": owner,
            "repository": repository_name,
            "issue": issue_number,
            "project": project_number,
        },
    )

    repository = data.get("repository")
    issue = repository and repository.get("issue")
    organization = data.get("organization")
    project = organization and organization.get("projectV2")
    if not issue:
        raise RuntimeError(f"Issue #{issue_number} was not found")
    if not project:
        raise RuntimeError(f"ProjectV2 #{project_number} was not found")
    return issue, project


def find_status_configuration(project):
    status_field = next(
        (
            field
            for field in project["fields"]["nodes"]
            if field.get("__typename") == "ProjectV2SingleSelectField"
            and field.get("name", "").casefold() == "status"
        ),
        None,
    )
    if not status_field:
        raise RuntimeError("The project's Status field was not found")

    not_planned_option = next(
        (
            option
            for option in status_field["options"]
            if option.get("name", "").casefold() == "not planned"
        ),
        None,
    )
    if not not_planned_option:
        raise RuntimeError("The Status field's Not Planned option was not found")
    return status_field["id"], not_planned_option["id"]


def get_or_add_project_item(token, issue, project):
    project_item = next(
        (
            item
            for item in issue["projectItems"]["nodes"]
            if item.get("project") and item["project"].get("id") == project["id"]
        ),
        None,
    )
    if project_item:
        return project_item["id"]

    mutation = """
    mutation($project: ID!, $issue: ID!) {
      addProjectV2ItemById(input: {projectId: $project, contentId: $issue}) {
        item { id }
      }
    }
    """
    data = graphql(
        token,
        mutation,
        {"project": project["id"], "issue": issue["id"]},
    )
    print(f"Added issue to ProjectV2 {project['id']}")
    return data["addProjectV2ItemById"]["item"]["id"]


def set_project_status(token, project_id, item_id, field_id, option_id):
    mutation = """
    mutation($project: ID!, $item: ID!, $field: ID!, $option: String!) {
      updateProjectV2ItemFieldValue(
        input: {
          projectId: $project
          itemId: $item
          fieldId: $field
          value: {singleSelectOptionId: $option}
        }
      ) {
        projectV2Item { id }
      }
    }
    """
    graphql(
        token,
        mutation,
        {
            "project": project_id,
            "item": item_id,
            "field": field_id,
            "option": option_id,
        },
    )
    print("Set project Status to Not Planned")


def close_as_not_planned(token, repository, issue_number):
    issue_url = f"{API_URL}/repos/{repository}/issues/{issue_number}"

    # Read the live state from this response so an issue already closed as
    # completed is corrected before the final Project status update.
    issue, _ = request(token, "PATCH", issue_url, {"milestone": None})
    print("Cleared milestone")

    current_state = issue.get("state")
    current_reason = issue.get("state_reason")

    if current_state == "closed" and current_reason != "not_planned":
        request(
            token,
            "PATCH",
            issue_url,
            {"state": "open", "state_reason": "reopened"},
        )
        current_state = "open"
        print("Reopened issue so its close reason can be corrected")

    if current_state != "closed":
        issue, _ = request(
            token,
            "PATCH",
            issue_url,
            {"state": "closed", "state_reason": "not_planned"},
        )

    if (
        issue.get("state") != "closed"
        or issue.get("state_reason") != "not_planned"
        or issue.get("milestone") is not None
    ):
        raise RuntimeError("Issue did not end closed as Not Planned with no milestone")
    print("Closed issue as Not Planned")


def main():
    token = os.getenv("GH_TOKEN")
    repository = os.getenv("GITHUB_REPOSITORY", "YoYoGames/GameMaker-Bugs")
    issue_number_text = os.getenv("ISSUE_NUMBER")
    project_number_text = os.getenv("PROJECT_NUMBER", "17")
    if not token or not issue_number_text:
        sys.exit("Missing GH_TOKEN or ISSUE_NUMBER")

    try:
        owner, repository_name = repository.split("/", 1)
        issue_number = int(issue_number_text)
        project_number = int(project_number_text)
    except ValueError as error:
        sys.exit(f"Invalid repository, issue number, or project number: {error}")

    if not comment_exists(token, repository, issue_number):
        request(
            token,
            "POST",
            f"{API_URL}/repos/{repository}/issues/{issue_number}/comments",
            {"body": COMMENT_BODY},
            expected=(201,),
        )
        print("Added update_gm comment")
    else:
        print("The update_gm comment already exists; skipping duplicate")

    issue, project = get_issue_and_project(
        token, owner, repository_name, issue_number, project_number
    )
    field_id, option_id = find_status_configuration(project)
    item_id = get_or_add_project_item(token, issue, project)

    close_as_not_planned(token, repository, issue_number)
    set_project_status(token, project["id"], item_id, field_id, option_id)

    _, status = request(
        token,
        "DELETE",
        f"{API_URL}/repos/{repository}/issues/{issue_number}/labels/"
        f"{quote('update_gm', safe='')}",
        expected=(200, 404),
    )
    if status == 200:
        print("Removed update_gm label; all other labels were preserved")
    else:
        print("The update_gm label was already absent")


if __name__ == "__main__":
    main()
