from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.recommendation import Recommendation
from app.repositories.recommendation_repository import (
    create_recommendation,
    delete_recommendation,
    get_recommendation_by_assessment as repo_get_by_assessment,
    get_recommendation_by_id as repo_get_by_id,
    update_recommendation as repo_update_recommendation,
)
from app.schemas.recommendation import RecommendationCreate, RecommendationOut


def _to_out(rec: Recommendation) -> RecommendationOut:
    return RecommendationOut(
        id=rec.id,
        assessment_id=rec.assessment_id,
        report=rec.report,
        created_at=rec.created_at,
    )


def create_recommendation_data(db: Session, payload: RecommendationCreate) -> RecommendationOut:
    rec = create_recommendation(db, payload)
    return _to_out(rec)


def get_recommendation_data_by_id(db: Session, recommendation_id: int) -> RecommendationOut:
    rec = repo_get_by_id(db, recommendation_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    return _to_out(rec)


def get_recommendation_by_assessment(db: Session, assessment_id: int) -> RecommendationOut:
    rec = repo_get_by_assessment(db, assessment_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada para este assessment")
    return _to_out(rec)


def update_recommendation_data(db: Session, recommendation_id: int, report: dict) -> RecommendationOut:
    rec = repo_update_recommendation(db, recommendation_id, report)
    if not rec:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    return _to_out(rec)


def delete_recommendation_data(db: Session, recommendation_id: int) -> dict:
    success = delete_recommendation(db, recommendation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    return {"detail": "Recomendación eliminada correctamente"}
