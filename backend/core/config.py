from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = Field(default="Breathe", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    cors_origins: str = Field(default="http://localhost:5173", alias="CORS_ORIGINS")
    api_prefix: str = Field(default="/api", alias="API_PREFIX")
    frontend_dist_dir: str = Field(default="backend/static", alias="FRONTEND_DIST_DIR")
    ai_provider: str = Field(default="placeholder", alias="AI_PROVIDER")
    ai_model: str = Field(
        default="gemini-2.5-flash",
        validation_alias=AliasChoices("AI_MODEL", "GEMINI_MODEL"),
    )
    ai_api_key: str = Field(
        default="",
        validation_alias=AliasChoices("AI_API_KEY", "GEMINI_API_KEY"),
    )
    gemini_timeout_seconds: float = Field(
        default=12.0,
        validation_alias=AliasChoices("GEMINI_TIMEOUT_SECONDS"),
    )
    gemini_api_base_url: str = Field(
        default="https://generativelanguage.googleapis.com/v1beta/interactions",
        validation_alias=AliasChoices("GEMINI_API_BASE_URL"),
    )

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() in {"dev", "development", "local"}

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def gemini_enabled(self) -> bool:
        return self.ai_provider.lower() == "gemini" and bool(self.ai_api_key.strip())


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
