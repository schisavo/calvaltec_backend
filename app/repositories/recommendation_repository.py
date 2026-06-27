from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation
from app.schemas.recommendation import RecommendationCreate


def create_recommendation(db: Session, payload: RecommendationCreate) -> Recommendation:
    existing = get_recommendation_by_assessment(db, payload.assessment_id)
    if existing:
        existing.report = payload.report
        db.commit()
        db.refresh(existing)
        return existing

    rec = Recommendation(assessment_id=payload.assessment_id, report=payload.report)
    db.add(rec)
    try:
        db.commit()
        db.refresh(rec)
        return rec
    except IntegrityError:
        db.rollback()
        existing = get_recommendation_by_assessment(db, payload.assessment_id)
        if not existing:
            raise
        existing.report = payload.report
        db.commit()
        db.refresh(existing)
        return existing


def get_recommendation_by_id(db: Session, recommendation_id: int) -> Recommendation | None:
    return db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()


def get_recommendation_by_assessment(db: Session, assessment_id: int) -> Recommendation | None:
    return db.query(Recommendation).filter(Recommendation.assessment_id == assessment_id).first()


def update_recommendation(db: Session, recommendation_id: int, report: dict) -> Recommendation | None:
    rec = get_recommendation_by_id(db, recommendation_id)
    if rec:
        rec.report = report
        db.commit()
        db.refresh(rec)
    return rec


def delete_recommendation(db: Session, recommendation_id: int) -> bool:
    rec = get_recommendation_by_id(db, recommendation_id)
    if rec:
        db.delete(rec)
        db.commit()
        return True
    return False
