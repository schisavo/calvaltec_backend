from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import utc_now

if TYPE_CHECKING:
    from app.models.assessment import Assessment


class Recommendation(SQLModel, table=True):
    __tablename__ = "recommendations"

    id: int | None = Field(default=None, primary_key=True)
    assessment_id: int = Field(foreign_key="assessments.id", unique=True)
    report: dict[str, Any] = Field(sa_column=Column(JSONB, nullable=False))
    created_at: datetime = Field(default_factory=utc_now)

    assessment: Optional["Assessment"] = Relationship(back_populates="recommendation")
