from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.assessment import Assessment


class Answer(SQLModel, table=True):
    __tablename__ = "answers"

    id: int | None = Field(default=None, primary_key=True)
    assessment_id: int = Field(foreign_key="assessments.id")
    question_number: int
    answer: bool

    assessment: Optional["Assessment"] = Relationship(back_populates="answers")
