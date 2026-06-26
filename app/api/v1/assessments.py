from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.assessment_service import (
    get_assessment_data,
    create_assessment_data,
    update_assessment_data,
    delete_assessment_data
)
from app.schemas.assessment import AssessmentOut

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

@router.post("/assessments", response_model=AssessmentOut)
def create_assessment(assessment: AssessmentOut, db: Session = Depends(get_db)):
    return create_assessment_data(db, assessment)

@router.put("/assessments/{assessment_id}", response_model=AssessmentOut)
def update_assessment(assessment_id: int, assessment: AssessmentOut, db: Session = Depends(get_db)):
    return update_assessment_data(db, assessment_id, assessment)

@router.delete("/assessments/{assessment_id}")
def delete_assessment(assessment_id: int, db: Session = Depends(get_db)):
    return delete_assessment_data(db, assessment_id)


"""

POST /api/v1/assessments → crear

GET /api/v1/assessments/{id} → leer

PUT /api/v1/assessments/{id} → actualizar

DELETE /api/v1/assessments/{id} → eliminar


"""