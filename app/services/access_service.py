from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.repositories.assessment_repository import get_assessment


def assert_assessment_exists(db: Session, assessment_id: int) -> Assessment:
    assessment, _ = get_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return assessment
