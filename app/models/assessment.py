from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import utc_now

if TYPE_CHECKING:
    from app.models.answer import Answer
    from app.models.company import Company
    from app.models.recommendation import Recommendation


class Assessment(SQLModel, table=True):
    __tablename__ = "assessments"

    id: int | None = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="companies.id")
    score: float
    created_at: datetime = Field(default_factory=utc_now)

    company: Optional["Company"] = Relationship(back_populates="assessments")
    answers: list["Answer"] = Relationship(back_populates="assessment")
    recommendation: Optional["Recommendation"] = Relationship(back_populates="assessment")
