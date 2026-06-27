from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.compliance_repository import get_progress, upsert_progress
from app.repositories.assessment_repository import get_assessment
from app.schemas.compliance import ComplianceProgressOut, ComplianceProgressUpdate


def _to_out(row) -> ComplianceProgressOut:
    return ComplianceProgressOut(
        company_id=row.company_id,
        assessment_id=row.assessment_id,
        checklist=row.checklist or {},
        action_status=row.action_status or {},
        dismissed_alerts=row.dismissed_alerts or [],
        document_analyses=row.document_analyses or [],
        updated_at=row.updated_at,
    )


def _resolve_company_id(
    db: Session, assessment_id: int | None, company_id: int | None
) -> int | None:
    if assessment_id is not None:
        assessment, _ = get_assessment(db, assessment_id)
        if not assessment:
            raise HTTPException(status_code=404, detail="Evaluación no encontrada")
        return assessment.company_id
    return company_id


def get_compliance_progress(
    db: Session,
    assessment_id: int | None = None,
    company_id: int | None = None,
) -> ComplianceProgressOut:
    resolved_company_id = _resolve_company_id(db, assessment_id, company_id)
    if resolved_company_id is None:
        return ComplianceProgressOut(company_id=0, assessment_id=assessment_id)

    row = get_progress(db, resolved_company_id, assessment_id)
    if not row:
        return ComplianceProgressOut(
            company_id=resolved_company_id,
            assessment_id=assessment_id,
        )
    return _to_out(row)


def update_compliance_progress(
    db: Session,
    payload: ComplianceProgressUpdate,
    assessment_id: int | None = None,
    company_id: int | None = None,
) -> ComplianceProgressOut:
    resolved_company_id = _resolve_company_id(db, assessment_id, company_id)
    if resolved_company_id is None:
        raise HTTPException(status_code=400, detail="Indica company_id o assessment_id")

    row = upsert_progress(
        db,
        resolved_company_id,
        assessment_id,
        checklist=payload.checklist,
        action_status=payload.action_status,
        dismissed_alerts=payload.dismissed_alerts,
        document_analyses=payload.document_analyses,
    )
    return _to_out(row)
