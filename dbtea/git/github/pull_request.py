import json
import os
import requests

GITHUB_API_URL = "https://api.github.com"

# TODO: Create new branch to allow PR to be created from it
def create_pull_request(organization_name: str, repository_name: str, git_token: str, head_branch: str,
                        base_branch: str = 'main',
                        title: str = "dbtea updates", description: str = "dbtea metadata refresh"):
    """Creates the pull request for the head_branch against the base_branch"""
    github_pulls_url = os.path.join(GITHUB_API_URL, "repos", organization_name, repository_name, "pulls")
    headers = {
        "Authorization": "token {}".format(git_token),
        "Content-Type": "application/json"
    }

    payload = {
        "title": title,
        "body": description,
        "head": head_branch,
        "base": base_branch,
    }

    response = requests.post(github_pulls_url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()


create_pull_request("jmbrooks", "dbtea", git_token="010234eb9332c88bdfbb7476aaf792b0233db989",
                    head_branch="feature/pull-request-test", base_branch="main",
                    title="dbtea test pull request", description="dbtea request for metadata refresh test")
