from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

from app.models.base import utc_now

if TYPE_CHECKING:
    from app.models.company import Company


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    name: str
    role: str
    company_id: int | None = Field(default=None, foreign_key="companies.id")
    created_at: datetime = Field(default_factory=utc_now)