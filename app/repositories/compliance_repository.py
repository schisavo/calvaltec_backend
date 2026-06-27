from sqlalchemy.orm import Session

from app.models.compliance_progress import ComplianceProgress


def get_progress(
    db: Session, company_id: int, assessment_id: int | None = None
) -> ComplianceProgress | None:
    q = db.query(ComplianceProgress).filter(ComplianceProgress.company_id == company_id)
    if assessment_id is not None:
        q = q.filter(ComplianceProgress.assessment_id == assessment_id)
    return q.order_by(ComplianceProgress.updated_at.desc()).first()


def upsert_progress(
    db: Session,
    company_id: int,
    assessment_id: int | None,
    *,
    checklist: dict | None = None,
    action_status: dict | None = None,
    dismissed_alerts: list | None = None,
    document_analyses: list | None = None,
) -> ComplianceProgress:
    row = get_progress(db, company_id, assessment_id)
    if not row:
        row = ComplianceProgress(company_id=company_id, assessment_id=assessment_id)
        db.add(row)

    if checklist is not None:
        row.checklist = {**row.checklist, **checklist}
    if action_status is not None:
        row.action_status = {**row.action_status, **action_status}
    if dismissed_alerts is not None:
        row.dismissed_alerts = dismissed_alerts
    if document_analyses is not None:
        row.document_analyses = document_analyses

    db.commit()
    db.refresh(row)
    return row
