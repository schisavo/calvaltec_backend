from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class ComplianceProgress(SQLModel, table=True):
    __tablename__ = "compliance_progress"

    id: int | None = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="companies.id", index=True)
    assessment_id: int | None = Field(default=None, foreign_key="assessments.id", index=True)
    checklist: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    action_status: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    dismissed_alerts: list[str] = Field(default_factory=list, sa_column=Column(JSONB, nullable=False))
    document_analyses: list[dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSONB, nullable=False))
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
    )
