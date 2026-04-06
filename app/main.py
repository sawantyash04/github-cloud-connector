from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import get_settings
from app.core.exceptions import GitHubAPIError, MissingGitHubTokenError

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="A clean FastAPI GitHub connector using secure PAT-based authentication.",
)


@app.exception_handler(MissingGitHubTokenError)
async def missing_token_handler(_: Request, exc: MissingGitHubTokenError) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": str(exc)})


@app.exception_handler(GitHubAPIError)
async def github_api_error_handler(_: Request, exc: GitHubAPIError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(router)
