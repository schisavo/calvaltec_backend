from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth_deps import get_current_user
from app.api.deps import get_db
from app.models.user import User
from app.schemas.recommendation import RecommendationCreate, RecommendationOut
from app.services.access_service import assert_assessment_access
from app.services.recommendation_service import (
    create_recommendation_data,
    delete_recommendation_data,
    get_recommendation_by_assessment,
    get_recommendation_by_id,
    update_recommendation_data,
)

router = APIRouter()


@router.post("/recommendations", response_model=RecommendationOut, status_code=201)
def create_recommendation(payload: RecommendationCreate, db: Session = Depends(get_db)):
    return create_recommendation_data(db, payload)


@router.get("/recommendations/{assessment_id}", response_model=RecommendationOut)
def read_recommendation_by_assessment_id(
    assessment_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    assert_assessment_access(db, user, assessment_id)
    return get_recommendation_by_assessment(db, assessment_id)


@router.get("/assessments/{assessment_id}/recommendations", response_model=RecommendationOut)
def read_recommendation_by_assessment(assessment_id: int, db: Session = Depends(get_db)):
    return get_recommendation_by_assessment(db, assessment_id)


@router.put("/recommendations/{recommendation_id}", response_model=RecommendationOut)
def update_recommendation(recommendation_id: int, report: dict, db: Session = Depends(get_db)):
    return update_recommendation_data(db, recommendation_id, report)


@router.delete("/recommendations/{recommendation_id}")
def delete_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    return delete_recommendation_data(db, recommendation_id)
