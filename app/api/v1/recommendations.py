from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session



from app.api.auth_deps import get_current_user

from app.api.deps import get_db

from app.models.user import User

from app.schemas.assessment import RecommendationCreate, RecommendationOut

from app.services.access_service import assert_assessment_access

from app.services.assessment_service import create_recommendation_data, get_recommendation_data



router = APIRouter()





@router.get("/recommendations/{assessment_id}", response_model=RecommendationOut)

def read_recommendation_public(

    assessment_id: int,

    user: User = Depends(get_current_user),

    db: Session = Depends(get_db),

):

    assert_assessment_access(db, user, assessment_id)

    return get_recommendation_data(db, assessment_id)





@router.post("/recommendations", response_model=RecommendationOut, status_code=201)

def create_recommendation_public(payload: RecommendationCreate, db: Session = Depends(get_db)):

    return create_recommendation_data(db, payload)


