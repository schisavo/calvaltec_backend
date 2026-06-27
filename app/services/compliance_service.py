from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.compliance_repository import get_progress, upsert_progress
from app.schemas.compliance import ComplianceProgressOut, ComplianceProgressUpdate
from app.services.access_service import assert_assessment_access


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


def get_compliance_progress(
    db: Session, user: User, assessment_id: int | None = None
) -> ComplianceProgressOut:
    company_id = user.company_id
    if assessment_id is not None:
        assessment = assert_assessment_access(db, user, assessment_id)
        company_id = assessment.company_id
        row = get_progress(db, company_id, assessment_id)
    else:
        if company_id is None:
            return ComplianceProgressOut(company_id=0, assessment_id=None)
        row = get_progress(db, company_id, None)

    if not row:
        return ComplianceProgressOut(
            company_id=company_id or 0,
            assessment_id=assessment_id,
        )
    return _to_out(row)


def update_compliance_progress(
    db: Session, user: User, payload: ComplianceProgressUpdate, assessment_id: int | None = None
) -> ComplianceProgressOut:
    company_id = user.company_id
    if assessment_id is not None:
        assessment = assert_assessment_access(db, user, assessment_id)
        company_id = assessment.company_id
    elif company_id is None and user.role not in ("admin", "auditor"):
        raise HTTPException(status_code=400, detail="Usuario sin empresa asociada")

    if company_id is None:
        raise HTTPException(status_code=400, detail="No se pudo determinar la empresa")

    row = upsert_progress(
        db,
        company_id,
        assessment_id,
        checklist=payload.checklist,
        action_status=payload.action_status,
        dismissed_alerts=payload.dismissed_alerts,
        document_analyses=payload.document_analyses,
    )
    return _to_out(row)
