"""
Application configuration.
"""

from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    codeforces_api_base_url: str = (
        "https://codeforces.com/api"
    )

    postgres_host: str = "localhost"
    postgres_port: int = 5433
    postgres_database: str = "codeforces_dw"
    postgres_user: str = "codeforces"
    postgres_password: str = "codeforces_dev_password"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()