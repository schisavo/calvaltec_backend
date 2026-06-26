from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import utc_now

if TYPE_CHECKING:
    from app.models.assessment import Assessment


class Company(SQLModel, table=True):
    __tablename__ = "companies"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    nit: str
    sector: str
    size: str = "mediana"
    created_at: datetime = Field(default_factory=utc_now)

    assessments: list["Assessment"] = Relationship(back_populates="company")
