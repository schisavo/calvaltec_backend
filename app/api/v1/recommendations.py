from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.recommendation import RecommendationCreate, RecommendationOut
from app.services.recommendation_service import create_recommendation_data, get_recommendation_data

router = APIRouter()

@router.post("/recommendations", response_model=RecommendationOut, status_code=201)
def create_recommendation(payload: RecommendationCreate, db: Session = Depends(get_db)):
    return create_recommendation_data(db, payload)

@router.get("/recommendations/{assessment_id}", response_model=RecommendationOut)
def read_recommendation(assessment_id: int, db: Session = Depends(get_db)):
    return get_recommendation_data(db, assessment_id)
