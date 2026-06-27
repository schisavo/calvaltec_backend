from datetime import datetime

from pydantic import BaseModel, Field


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2)
    email: str | None = None
    nit: str | None = Field(default=None, min_length=5)
    sector: str | None = Field(default=None, min_length=2)
    size: str | None = Field(default=None, pattern="^(pequena|mediana|grande)$")


class CompanyOut(BaseModel):
    id: int
    name: str
    email: str
    nit: str
    sector: str
    size: str
    created_at: datetime


class CompanySummary(BaseModel):
    id: int
    name: str
    email: str
    nit: str
    sector: str
    size: str
    assessment_count: int = 0
    latest_score: float | None = None
    latest_status: str | None = None
