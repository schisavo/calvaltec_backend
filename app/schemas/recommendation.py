from datetime import datetime
from typing import Any
from pydantic import BaseModel

class RecommendationCreate(BaseModel):
    assessment_id: int
    report: dict[str, Any]

class RecommendationOut(BaseModel):
    id: int
    assessment_id: int
    report: dict[str, Any]
    created_at: datetime
