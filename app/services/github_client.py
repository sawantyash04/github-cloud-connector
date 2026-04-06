from typing import Any

import httpx

from app.core.config import get_settings
from app.core.exceptions import GitHubAPIError


class GitHubClient:
    def __init__(self, token: str):
        settings = get_settings()
        self.base_url = settings.github_api_base_url.rstrip("/")
        self.timeout = settings.github_timeout_seconds
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": settings.github_api_version,
            "User-Agent": "github-cloud-connector",
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        url = f"{self.base_url}{endpoint}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    json=json,
                )
        except httpx.TimeoutException as exc:
            raise GitHubAPIError(status_code=504, message="GitHub API request timed out") from exc
        except httpx.RequestError as exc:
            raise GitHubAPIError(status_code=502, message=f"Failed to reach GitHub API: {exc}") from exc

        if response.status_code >= 400:
            message = self._extract_error_message(response)
            raise GitHubAPIError(status_code=response.status_code, message=message)

        if response.status_code == 204:
            return None

        return response.json()

    @staticmethod
    def _extract_error_message(response: httpx.Response) -> str:
        try:
            payload = response.json()
            if isinstance(payload, dict):
                return payload.get("message") or payload.get("error") or response.text
        except ValueError:
            pass
        return response.text or "GitHub API request failed"

    async def get_authenticated_user(self) -> dict[str, Any]:
        return await self._request("GET", "/user")

    async def list_user_repositories(self, username: str) -> list[dict[str, Any]]:
        return await self._request("GET", f"/users/{username}/repos", params={"sort": "updated", "per_page": 30})

    async def list_org_repositories(self, org: str) -> list[dict[str, Any]]:
        return await self._request("GET", f"/orgs/{org}/repos", params={"sort": "updated", "per_page": 30})

    async def list_repository_issues(self, owner: str, repo: str) -> list[dict[str, Any]]:
        return await self._request("GET", f"/repos/{owner}/{repo}/issues", params={"state": "open", "per_page": 30})

    async def create_issue(self, owner: str, repo: str, title: str, body: str | None = None) -> dict[str, Any]:
        payload = {"title": title, "body": body}
        return await self._request("POST", f"/repos/{owner}/{repo}/issues", json=payload)

    async def list_commits(self, owner: str, repo: str) -> list[dict[str, Any]]:
        return await self._request("GET", f"/repos/{owner}/{repo}/commits", params={"per_page": 10})
