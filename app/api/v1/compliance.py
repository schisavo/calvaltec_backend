from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.compliance import ComplianceProgressOut, ComplianceProgressUpdate
from app.services.compliance_service import get_compliance_progress, update_compliance_progress

router = APIRouter()


@router.get("/compliance/progress", response_model=ComplianceProgressOut)
def read_compliance_progress(
    assessment_id: int | None = Query(default=None),
    company_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return get_compliance_progress(db, assessment_id=assessment_id, company_id=company_id)


@router.put("/compliance/progress", response_model=ComplianceProgressOut)
def write_compliance_progress(
    payload: ComplianceProgressUpdate,
    assessment_id: int | None = Query(default=None),
    company_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return update_compliance_progress(
        db, payload, assessment_id=assessment_id, company_id=company_id
    )
