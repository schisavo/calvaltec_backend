from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field, SQLModel

from app.models.base import utc_now


class OAuthState(SQLModel, table=True):
    __tablename__ = "oauth_states"

    state: str = Field(primary_key=True, max_length=128)
    payload: dict = Field(sa_column=Column(JSON, nullable=False))
    expires_at: datetime = Field(index=True)
    created_at: datetime = Field(default_factory=utc_now)
