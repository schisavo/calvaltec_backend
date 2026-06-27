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


class GenerateRecommendationsOut(RecommendationOut):
    """Respuesta al crear recomendaciones; indica si n8n sigue procesando."""

    n8n_pending: bool = False


class GenerateRecommendationsRequest(BaseModel):
    puntaje: float = Field(ge=0, le=100)
    estado: str
    brechas: list[str] = Field(default_factory=list)
    recomendaciones: list[str] = Field(default_factory=list)
    empresa: str | None = None
