from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.assessment_repository import (
    create_assessment,
    delete_assessment,
    get_assessment,
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

    new_assessment = create_assessment(db, payload)
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
