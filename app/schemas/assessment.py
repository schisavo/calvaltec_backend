from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


from pydantic import BaseModel, Field, model_validator


class CompanyCreate(BaseModel):
    name: str
    email: str
    nit: str
    sector: str


class CompanyOut(CompanyCreate):
    id: int
    created_at: datetime


class AnswerCreate(BaseModel):
    question_number: int = Field(ge=1, le=11)
    answer: bool


class AnswerOut(AnswerCreate):
    id: int


class AssessmentCreate(BaseModel):
    company: CompanyCreate | None = None
    company_id: int | None = None
    score: float
    answers: list[AnswerCreate]

    @model_validator(mode="after")
    def require_company_or_id(self):
        if self.company is None and self.company_id is None:
            raise ValueError("Debe indicar company o company_id")
        return self


class AssessmentUpdate(BaseModel):
    score: float


class AssessmentOut(BaseModel):
    id: int
    company_id: int
    company: CompanyOut
    score: float
    created_at: datetime
    answers: list[AnswerOut]


class AssessmentSummary(BaseModel):
    id: int
    company_id: int
    company_name: str
    score: float
    status: str
    created_at: datetime
    has_recommendation: bool
    nivel_riesgo: str | None = None


class RecommendationCreate(BaseModel):
    assessment_id: int
    report: dict[str, Any]


class RecommendationOut(BaseModel):
    id: int
    assessment_id: int
    report: dict[str, Any]
    created_at: datetime
