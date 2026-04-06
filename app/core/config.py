from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GitHub Cloud Connector"
    github_api_base_url: str = "https://api.github.com"
    github_api_version: str = "2022-11-28"
    github_timeout_seconds: float = 20.0
    github_token: str | None = None
    app_port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
