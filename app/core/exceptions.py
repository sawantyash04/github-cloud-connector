class GitHubConnectorError(Exception):
    """Base exception for connector-level errors."""


class MissingGitHubTokenError(GitHubConnectorError):
    """Raised when the request does not include a token and no fallback token exists."""


class GitHubAPIError(GitHubConnectorError):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)
