from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.assessment_repository import (
    create_assessment,
    create_recommendation,
    delete_assessment,
    get_assessment,
    get_recommendation,
    update_assessment,
)
from app.schemas.assessment import (
    AnswerOut,
    AssessmentCreate,
    AssessmentOut,
    CompanyOut,
    RecommendationCreate,
    RecommendationOut,
)


def _to_assessment_out(assessment, answers) -> AssessmentOut:
    return AssessmentOut(
        id=assessment.id,
        company_id=assessment.company_id,
        company=CompanyOut(
            id=assessment.company.id,
            name=assessment.company.name,
            email=assessment.company.email,
            nit=assessment.company.nit,
            sector=assessment.company.sector,
            created_at=assessment.company.created_at,
        ),
        score=assessment.score,
        created_at=assessment.created_at,
        answers=[
            AnswerOut(
                id=a.id,
                question_number=a.question_number,
                answer=a.answer,
            )
            for a in answers
        ],
    )


def get_assessment_data(db: Session, assessment_id: int) -> AssessmentOut:
    assessment, answers = get_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment no encontrado")
    return _to_assessment_out(assessment, answers)


def create_assessment_data(db: Session, payload: AssessmentCreate) -> AssessmentOut:
    if len(payload.answers) != 8:
        raise HTTPException(status_code=400, detail="Se requieren exactamente 8 respuestas")

    try:
        new_assessment = create_assessment(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    _, answers = get_assessment(db, new_assessment.id)
    return _to_assessment_out(new_assessment, answers)


def update_assessment_data(db: Session, assessment_id: int, score: float) -> AssessmentOut:
    updated = update_assessment(db, assessment_id, score)
    if not updated:
        raise HTTPException(status_code=404, detail="Assessment no encontrado")
    _, answers = get_assessment(db, assessment_id)
    return _to_assessment_out(updated, answers)


def delete_assessment_data(db: Session, assessment_id: int) -> dict:
    deleted = delete_assessment(db, assessment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Assessment no encontrado")
    return {"message": f"Assessment {assessment_id} eliminado"}


def get_recommendation_data(db: Session, assessment_id: int) -> RecommendationOut:
    recommendation = get_recommendation(db, assessment_id)
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recomendación no encontrada")
    return RecommendationOut(
        id=recommendation.id,
        assessment_id=recommendation.assessment_id,
        report=recommendation.report,
        created_at=recommendation.created_at,
    )


def create_recommendation_data(db: Session, payload: RecommendationCreate) -> RecommendationOut:
    assessment, _ = get_assessment(db, payload.assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment no encontrado")

    existing = get_recommendation(db, payload.assessment_id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una recomendación para este assessment",
        )

    recommendation = create_recommendation(db, payload)
    return RecommendationOut(
        id=recommendation.id,
        assessment_id=recommendation.assessment_id,
        report=recommendation.report,
        created_at=recommendation.created_at,
    )
