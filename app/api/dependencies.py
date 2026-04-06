from fastapi import Header

from app.core.config import get_settings
from app.core.exceptions import MissingGitHubTokenError


def resolve_github_token(x_github_token: str | None = Header(default=None)) -> str:
    """
    Resolve a GitHub token from the incoming request header first.
    Falls back to the optional .env value for local development.
    """
    if x_github_token and x_github_token.strip():
        return x_github_token.strip()

    settings = get_settings()
    if settings.github_token and settings.github_token.strip():
        return settings.github_token.strip()

    raise MissingGitHubTokenError(
        "GitHub token missing. Send it in the X-GitHub-Token header or set GITHUB_TOKEN in .env"
    )
