from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str = "cavaltec-dev-secret-change-in-production"
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    OPENAI_API_KEY: str | None = None
    REDIS_URL: str | None = None
    API_KEY_SECRET: str | None = None
    N8N_CHAT_WEBHOOK_URL: str = (
        "https://smartteam2026.app.n8n.cloud/webhook/chat-assistant"
    )
    SWAGGER_API_KEY: str = "26yusesaal06secaval2026"

    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgresql://") and "+psycopg2" not in value:
            return value.replace("postgresql://", "postgresql+psycopg2://", 1)
        return value

    @property
    def database_url(self) -> str:
        return self.DATABASE_URL

    class Config:
        env_file = ".env"


settings = Settings()
