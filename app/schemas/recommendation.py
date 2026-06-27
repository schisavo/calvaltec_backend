from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class RecommendationCreate(BaseModel):
    assessment_id: int
    report: dict[str, Any]


class RecommendationOut(BaseModel):
    id: int
    assessment_id: int
    report: dict[str, Any]
    created_at: datetime


class GenerateRecommendationsRequest(BaseModel):
    puntaje: float = Field(ge=0, le=100)
    estado: str
    brechas: list[str] = Field(default_factory=list)
    recomendaciones: list[str] = Field(default_factory=list)
    empresa: str | None = None
