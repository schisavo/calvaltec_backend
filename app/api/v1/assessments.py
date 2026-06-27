from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from app.api.auth_deps import get_current_user, get_current_user_optional
from app.api.deps import get_db
from app.models.user import User
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentOut,
    AssessmentSummary,
    AssessmentUpdate,
)
from app.services.access_service import assert_assessment_access, assessment_list_company_scope
from app.services.company_user_service import ensure_user_company, link_user_to_company
from app.services.assessment_list_service import list_assessments_summary
from app.services.assessment_service import (
    create_assessment_data,
    delete_assessment_data,
    get_assessment_data,
    update_assessment_data,
)

router = APIRouter()


@router.get("/assessments", response_model=list[AssessmentSummary])
def list_assessments_endpoint(
    company_id: int | None = Query(default=None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role not in ("admin", "auditor"):
        ensure_user_company(db, user)
        if user.company_id is None:
            return []

    scope = assessment_list_company_scope(user, company_id)
    return list_assessments_summary(db, company_id=scope)


@router.get("/assessments/{assessment_id}", response_model=AssessmentOut)
def read_assessment(
    assessment_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    assert_assessment_access(db, user, assessment_id)
    return get_assessment_data(db, assessment_id)


@router.post("/assessments", response_model=AssessmentOut, status_code=201)
def create_assessment_endpoint(
    payload: AssessmentCreate,
    user: User | None = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    if user and user.role in ("company", "evaluador"):
        company_id = ensure_user_company(db, user)
        if company_id:
            payload = payload.model_copy(update={"company_id": company_id, "company": None})

    result = create_assessment_data(db, payload)

    if user and user.role in ("company", "evaluador") and user.company_id is None:
        link_user_to_company(db, user, result.company_id)

    return result


@router.put("/assessments/{assessment_id}", response_model=AssessmentOut)
def update_assessment_endpoint(
    assessment_id: int,
    payload: AssessmentUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    assert_assessment_access(db, user, assessment_id)
    return update_assessment_data(db, assessment_id, payload.score)


@router.delete("/assessments/{assessment_id}")
def delete_assessment_endpoint(
    assessment_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    assert_assessment_access(db, user, assessment_id)
    return delete_assessment_data(db, assessment_id)
