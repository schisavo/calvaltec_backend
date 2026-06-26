from sqlalchemy.orm import Session
from app.models.recommendation import Recommendation
from app.schemas.recommendation import RecommendationCreate

def create_recommendation(db: Session, payload: RecommendationCreate) -> Recommendation:
    rec = Recommendation(assessment_id=payload.assessment_id, report=payload.report)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

def get_recommendation(db: Session, assessment_id: int) -> Recommendation | None:
    return db.query(Recommendation).filter(Recommendation.assessment_id == assessment_id).first()
