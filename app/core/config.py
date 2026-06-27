from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_ENV_FILE = _BACKEND_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE if _ENV_FILE.is_file() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str
    JWT_SECRET: str = "cavaltec-dev-secret-change-in-production"
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    OPENAI_API_KEY: str | None = None
    REDIS_URL: str | None = None
    API_KEY_SECRET: str = "26yusesaal06secaval2026"
    N8N_CHAT_WEBHOOK_URL: str = (
        "https://smartteam2026.app.n8n.cloud/webhook/chat-assistant"
    )
    N8N_RECOMMENDATIONS_WEBHOOK_URL: str = (
        "https://smartteam2026.app.n8n.cloud/webhook/generate-recommendations"
    )
    FRONTEND_URL: str
    BACKEND_PUBLIC_URL: str

    @field_validator("FRONTEND_URL", "BACKEND_PUBLIC_URL", mode="after")
    @classmethod
    def strip_trailing_slash(cls, value: str) -> str:
        return value.rstrip("/")

    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgresql://") and "+psycopg2" not in value:
            return value.replace("postgresql://", "postgresql+psycopg2://", 1)
        return value

    @property
    def database_url(self) -> str:
        return self.DATABASE_URL


settings = Settings()
