from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.recommendation_repository import (
    create_recommendation,
    get_recommendation_by_id,
    get_recommendation_by_assessment as repo_get_by_assessment,  # 👈 alias
    update_recommendation,
    delete_recommendation
)
from app.schemas.recommendation import RecommendationCreate, RecommendationOut

def create_recommendation_data(db: Session, payload: RecommendationCreate) -> RecommendationOut:
    rec = create_recommendation(db, payload)
    return RecommendationOut(**rec.__dict__)

def get_recommendation_by_id(db: Session, recommendation_id: int) -> RecommendationOut:
    rec = get_recommendation_by_id(db, recommendation_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    return RecommendationOut(**rec.__dict__)

def get_recommendation_by_assessment(db: Session, assessment_id: int) -> RecommendationOut:
    rec = repo_get_by_assessment(db, assessment_id)  # 👈 ahora sí llama al repo
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada para este assessment")
    return RecommendationOut(**rec.__dict__)

def update_recommendation_data(db: Session, recommendation_id: int, report: dict) -> RecommendationOut:
    rec = update_recommendation(db, recommendation_id, report)
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    return RecommendationOut(**rec.__dict__)

def delete_recommendation_data(db: Session, recommendation_id: int) -> dict:
    success = delete_recommendation(db, recommendation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    return {"detail": "Recomendación eliminada correctamente"}
