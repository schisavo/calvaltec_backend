from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CompanyCreate(BaseModel):
    name: str
    email: str
    nit: str
    sector: str


class CompanyOut(CompanyCreate):
    id: int
    created_at: datetime


class AnswerCreate(BaseModel):
    question_number: int = Field(ge=1, le=8)
    answer: bool


class AnswerOut(AnswerCreate):
    id: int


class AssessmentCreate(BaseModel):
    company: CompanyCreate
    score: float
    answers: list[AnswerCreate]


class AssessmentUpdate(BaseModel):
    score: float


class AssessmentOut(BaseModel):
    id: int
    company_id: int
    company: CompanyOut
    score: float
    created_at: datetime
    answers: list[AnswerOut]


class RecommendationCreate(BaseModel):
    assessment_id: int
    report: dict[str, Any]


class RecommendationOut(BaseModel):
    id: int
    assessment_id: int
    report: dict[str, Any]
    created_at: datetime
