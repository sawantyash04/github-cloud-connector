from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str


class AuthenticatedUserResponse(BaseModel):
    login: str
    id: int
    name: str | None = None
    public_repos: int | None = None
    html_url: str


class RepositoryResponse(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    html_url: str
    description: str | None = None
    language: str | None = None
    stargazers_count: int
    forks_count: int
    open_issues_count: int


class IssueResponse(BaseModel):
    id: int
    number: int
    title: str
    state: str
    html_url: str
    user_login: str | None = None
    created_at: str
    body: str | None = None


class CreateIssueRequest(BaseModel):
    owner: str = Field(..., min_length=1, description="Repository owner or organization")
    repo: str = Field(..., min_length=1, description="Repository name")
    title: str = Field(..., min_length=1, max_length=256, description="Issue title")
    body: str | None = Field(default=None, description="Issue description")


class CommitResponse(BaseModel):
    sha: str
    author_name: str | None = None
    message: str
    html_url: str
