from sqlmodel import SQLModel, Field

class Answer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    assessment_id: int = Field(foreign_key="assessment.id")
    question: str
    answer: bool
