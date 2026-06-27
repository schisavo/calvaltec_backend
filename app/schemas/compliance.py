from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ComplianceProgressOut(BaseModel):
    company_id: int
    assessment_id: int | None
    checklist: dict[str, bool] = Field(default_factory=dict)
    action_status: dict[str, str] = Field(default_factory=dict)
    dismissed_alerts: list[str] = Field(default_factory=list)
    document_analyses: list[dict[str, Any]] = Field(default_factory=list)
    updated_at: datetime | None = None


class ComplianceProgressUpdate(BaseModel):
    checklist: dict[str, bool] | None = None
    action_status: dict[str, str] | None = None
    dismissed_alerts: list[str] | None = None
    document_analyses: list[dict[str, Any]] | None = None
