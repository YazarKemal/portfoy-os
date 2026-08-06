from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    app_timezone: str = "Europe/Istanbul"
    database_url: str = "postgresql+psycopg://portfoy:change-me-locally@localhost:5432/portfoy_os"
    redis_url: str = "redis://localhost:6379/0"
    default_user_email: str = "owner@portfoy.local"
    default_user_display_name: str = "Portföy Sahibi"


settings = Settings()
