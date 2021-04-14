import json
import os
import requests

from dbtea.logger import DBTEA_LOGGER as logger
from dbtea.exceptions import GitException

GITHUB_API_URL = "https://api.github.com"


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
    if response.status_code >= 400:
        raise GitException(
            name="pull-request-create-fail",
            provider="github",
            title="Error Creating GitHub Pull Request via API",
            status=response.status_code,
            detail=response.json().get("errors"),
            response=response
        )

    logger.info("Created pull request for branch {} at URL: {}".format(head_branch, response.json().get("html_url")))


create_pull_request("jmbrooks", "dbtea", git_token="010234eb9332c88bdfbb7476aaf792b0233db989",
                    head_branch="feature/initial-looker-github-plugins", base_branch="main",
                    title="dbtea test pull request", description="dbtea request for metadata refresh test")

# TODO: Create new branch to allow PR to be created from it
# TODO: Determine how to auth not as individual user for creating PRs and such