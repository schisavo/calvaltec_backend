from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentOut,
    AssessmentUpdate,
    RecommendationCreate,
    RecommendationOut,
)
from app.services.assessment_service import (
    create_assessment_data,
    delete_assessment_data,
    get_assessment_data,
    update_assessment_data,
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/assessments/{assessment_id}", response_model=AssessmentOut)
def read_assessment(assessment_id: int, db: Session = Depends(get_db)):
    return get_assessment_data(db, assessment_id)


@router.post("/assessments", response_model=AssessmentOut, status_code=201)
def create_assessment_endpoint(payload: AssessmentCreate, db: Session = Depends(get_db)):
    return create_assessment_data(db, payload)


@router.put("/assessments/{assessment_id}", response_model=AssessmentOut)
def update_assessment_endpoint(
    assessment_id: int,
    payload: AssessmentUpdate,
    db: Session = Depends(get_db),
):
    return update_assessment_data(db, assessment_id, payload.score)


@router.delete("/assessments/{assessment_id}")
def delete_assessment_endpoint(assessment_id: int, db: Session = Depends(get_db)):
    return delete_assessment_data(db, assessment_id)
