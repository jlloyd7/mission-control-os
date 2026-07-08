"""Application configuration, loaded from environment / .env."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # App
    app_env: str = "development"
    app_name: str = "Mission Control OS"
    app_base_url: str = "http://localhost:3000"
    api_base_url: str = "http://localhost:8000"

    # Database — SQLite by default so P0 needs no Docker.
    database_url: str = "sqlite:///./mcos.db"

    # Dev auth stub
    dev_auth_enabled: bool = True
    dev_user_email: str = "george@example.local"
    dev_org_name: str = "Mission Control Dev"

    # Models — mock by default
    enable_real_models: bool = False
    default_model_provider: str = "mock"
    george_provider: str = "openai"
    george_model: str = "gpt-5.6-sol"
    cipher_provider: str = "anthropic"
    cipher_model: str = "claude-fable-5"
    arty_provider: str = "openai"
    arty_model: str = "gpt-5.6-sol-codex"

    # Keys (blank in mock mode)
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # Security / CORS
    secret_key: str = "change-me-in-dev"
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")


@lru_cache
def get_settings() -> Settings:
    return Settings()
