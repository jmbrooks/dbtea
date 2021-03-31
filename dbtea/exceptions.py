from typing import Any, Dict, Optional
import requests


class DbteaException(Exception):
    """Exception related to dbtea configuration, processing or compatibility."""
    exit_code = 100

    def __init__(self, name: str, title: str, detail: str):
        self.type: str = "/errors/" + name
        self.title = title
        self.detail = detail

    def __repr__(self) -> str:
        return self.title

    def __str__(self) -> str:
        return self.title + " " + self.detail


class GitException(Exception):
    """Exception related to Git or Git provider configuration or APIs."""
    exit_code = 101

    def __init__(
        self,
        name: str,
        provider: str,
        title: str,
        status: int,
        detail: str,
        response: requests.Response,
    ):
        request: requests.PreparedRequest = response.request
        super().__init__("git-errors/" + provider + "/" + name, title, detail)
        self.status = status
        self.looker_api_response: Optional[dict] = _details_from_http_error(response)
        self.request = {"url": request.url, "method": request.method}


def _details_from_http_error(response: requests.Response) -> Optional[Dict[str, Any]]:
    try:
        details = response.json()
    # Requests raises a ValueError if the response is invalid JSON
    except ValueError:
        details = None
    return details
