from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentOut,
    AssessmentSummary,
    AssessmentUpdate,
)
from app.schemas.recommendation import GenerateRecommendationsRequest, RecommendationOut
from app.services.access_service import assert_assessment_exists
from app.services.assessment_list_service import list_assessments_summary
from app.services.assessment_service import (
    create_assessment_data,
    delete_assessment_data,
    get_assessment_data,
    update_assessment_data,
)
from app.services.recommendation_service import get_recommendation_by_assessment
from app.services.recommendation_trigger_service import generate_recommendations_for_assessment

router = APIRouter()


@router.get("/assessments", response_model=list[AssessmentSummary])
def list_assessments_endpoint(
    company_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return list_assessments_summary(db, company_id=company_id)


@router.get("/assessments/{assessment_id}", response_model=AssessmentOut)
def read_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
):
    assert_assessment_exists(db, assessment_id)
    return get_assessment_data(db, assessment_id)


@router.post("/assessments", response_model=AssessmentOut, status_code=201)
def create_assessment_endpoint(
    payload: AssessmentCreate,
    db: Session = Depends(get_db),
):
    return create_assessment_data(db, payload)


@router.post(
    "/assessments/{assessment_id}/generate-recommendations",
    response_model=RecommendationOut,
    status_code=201,
)
def generate_recommendations_endpoint(
    assessment_id: int,
    payload: GenerateRecommendationsRequest,
    db: Session = Depends(get_db),
):
    assert_assessment_exists(db, assessment_id)
    return generate_recommendations_for_assessment(
        db,
        assessment_id,
        puntaje=payload.puntaje,
        estado=payload.estado,
        brechas=payload.brechas,
        recomendaciones=payload.recomendaciones,
        empresa=payload.empresa,
    )


@router.put("/assessments/{assessment_id}", response_model=AssessmentOut)
def update_assessment_endpoint(
    assessment_id: int,
    payload: AssessmentUpdate,
    db: Session = Depends(get_db),
):
    assert_assessment_exists(db, assessment_id)
    return update_assessment_data(db, assessment_id, payload.score)


@router.delete("/assessments/{assessment_id}")
def delete_assessment_endpoint(
    assessment_id: int,
    db: Session = Depends(get_db),
):
    assert_assessment_exists(db, assessment_id)
    return delete_assessment_data(db, assessment_id)
