from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.recommendation_repository import create_recommendation, get_recommendation
from app.schemas.recommendation import RecommendationCreate, RecommendationOut

def create_recommendation_data(db: Session, payload: RecommendationCreate) -> RecommendationOut:
    existing = get_recommendation(db, payload.assessment_id)
    if existing:
        raise HTTPException(status_code=409, detail="Ya existe una recomendación para este assessment")
    rec = create_recommendation(db, payload)
    return RecommendationOut(
        id=rec.id,
        assessment_id=rec.assessment_id,
        report=rec.report,
        created_at=rec.created_at
    )

def get_recommendation_data(db: Session, assessment_id: int) -> RecommendationOut:
    rec = get_recommendation(db, assessment_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    return RecommendationOut(
        id=rec.id,
        assessment_id=rec.assessment_id,
        report=rec.report,
        created_at=rec.created_at
    )
