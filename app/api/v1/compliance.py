from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.auth_deps import get_current_user
from app.api.deps import get_db
from app.models.user import User
from app.schemas.compliance import ComplianceProgressOut, ComplianceProgressUpdate
from app.services.compliance_service import get_compliance_progress, update_compliance_progress

router = APIRouter()


@router.get("/compliance/progress", response_model=ComplianceProgressOut)
def read_compliance_progress(
    assessment_id: int | None = Query(default=None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_compliance_progress(db, user, assessment_id)


@router.put("/compliance/progress", response_model=ComplianceProgressOut)
def write_compliance_progress(
    payload: ComplianceProgressUpdate,
    assessment_id: int | None = Query(default=None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_compliance_progress(db, user, payload, assessment_id)
