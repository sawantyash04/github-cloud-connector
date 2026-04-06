from fastapi import APIRouter, Depends

from app.api.dependencies import resolve_github_token
from app.core.config import get_settings
from app.models.schemas import (
    AuthenticatedUserResponse,
    CommitResponse,
    CreateIssueRequest,
    HealthResponse,
    IssueResponse,
    RepositoryResponse,
)
from app.services.github_client import GitHubClient

router = APIRouter()



@router.get("/health", response_model=HealthResponse, tags=["Utility"])
async def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", service=settings.app_name)


@router.get("/github/me", response_model=AuthenticatedUserResponse, tags=["GitHub"])
async def get_authenticated_user(token: str = Depends(resolve_github_token)) -> AuthenticatedUserResponse:
    client = GitHubClient(token)
    payload = await client.get_authenticated_user()
    return AuthenticatedUserResponse(
        login=payload["login"],
        id=payload["id"],
        name=payload.get("name"),
        public_repos=payload.get("public_repos"),
        html_url=payload["html_url"],
    )


@router.get("/github/users/{username}/repos", response_model=list[RepositoryResponse], tags=["GitHub"])
async def get_user_repositories(username: str, token: str = Depends(resolve_github_token)) -> list[RepositoryResponse]:
    client = GitHubClient(token)
    repos = await client.list_user_repositories(username)
    return [RepositoryResponse(**_map_repo(repo)) for repo in repos]


@router.get("/github/orgs/{org}/repos", response_model=list[RepositoryResponse], tags=["GitHub"])
async def get_org_repositories(org: str, token: str = Depends(resolve_github_token)) -> list[RepositoryResponse]:
    client = GitHubClient(token)
    repos = await client.list_org_repositories(org)
    return [RepositoryResponse(**_map_repo(repo)) for repo in repos]


@router.get("/github/repos/{owner}/{repo}/issues", response_model=list[IssueResponse], tags=["GitHub"])
async def get_repository_issues(owner: str, repo: str, token: str = Depends(resolve_github_token)) -> list[IssueResponse]:
    client = GitHubClient(token)
    issues = await client.list_repository_issues(owner, repo)
    filtered_issues = [item for item in issues if "pull_request" not in item]
    return [IssueResponse(**_map_issue(issue)) for issue in filtered_issues]


@router.post("/github/issues", response_model=IssueResponse, status_code=201, tags=["GitHub"])
async def create_repository_issue(
    request: CreateIssueRequest, token: str = Depends(resolve_github_token)
) -> IssueResponse:
    client = GitHubClient(token)
    issue = await client.create_issue(request.owner, request.repo, request.title, request.body)
    return IssueResponse(**_map_issue(issue))


@router.get("/github/repos/{owner}/{repo}/commits", response_model=list[CommitResponse], tags=["GitHub"])
async def get_repository_commits(owner: str, repo: str, token: str = Depends(resolve_github_token)) -> list[CommitResponse]:
    client = GitHubClient(token)
    commits = await client.list_commits(owner, repo)
    return [CommitResponse(**_map_commit(commit)) for commit in commits]


# Assignment-friendly alias endpoints
@router.get("/repos/user/{username}", response_model=list[RepositoryResponse], tags=["Alias Endpoints"])
async def alias_user_repositories(username: str, token: str = Depends(resolve_github_token)) -> list[RepositoryResponse]:
    return await get_user_repositories(username, token)


@router.get("/repos/org/{org}", response_model=list[RepositoryResponse], tags=["Alias Endpoints"])
async def alias_org_repositories(org: str, token: str = Depends(resolve_github_token)) -> list[RepositoryResponse]:
    return await get_org_repositories(org, token)


@router.get("/list-issues/{owner}/{repo}", response_model=list[IssueResponse], tags=["Alias Endpoints"])
async def alias_list_issues(owner: str, repo: str, token: str = Depends(resolve_github_token)) -> list[IssueResponse]:
    return await get_repository_issues(owner, repo, token)


@router.post("/create-issue", response_model=IssueResponse, status_code=201, tags=["Alias Endpoints"])
async def alias_create_issue(request: CreateIssueRequest, token: str = Depends(resolve_github_token)) -> IssueResponse:
    return await create_repository_issue(request, token)



def _map_repo(repo: dict) -> dict:
    return {
        "id": repo["id"],
        "name": repo["name"],
        "full_name": repo["full_name"],
        "private": repo["private"],
        "html_url": repo["html_url"],
        "description": repo.get("description"),
        "language": repo.get("language"),
        "stargazers_count": repo.get("stargazers_count", 0),
        "forks_count": repo.get("forks_count", 0),
        "open_issues_count": repo.get("open_issues_count", 0),
    }



def _map_issue(issue: dict) -> dict:
    return {
        "id": issue["id"],
        "number": issue["number"],
        "title": issue["title"],
        "state": issue["state"],
        "html_url": issue["html_url"],
        "user_login": issue.get("user", {}).get("login"),
        "created_at": issue["created_at"],
        "body": issue.get("body"),
    }



def _map_commit(commit: dict) -> dict:
    return {
        "sha": commit["sha"],
        "author_name": commit.get("commit", {}).get("author", {}).get("name"),
        "message": commit.get("commit", {}).get("message", ""),
        "html_url": commit["html_url"],
    }
