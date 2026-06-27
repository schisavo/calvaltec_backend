from sqlalchemy.orm import Session
from app.models.recommendation import Recommendation
from app.schemas.recommendation import RecommendationCreate

def create_recommendation(db: Session, payload: RecommendationCreate) -> Recommendation:
    rec = Recommendation(assessment_id=payload.assessment_id, report=payload.report)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

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
