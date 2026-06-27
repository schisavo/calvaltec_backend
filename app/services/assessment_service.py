from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.assessment_repository import (
    create_assessment,
    delete_assessment,
    get_assessment,
    update_assessment,
)
from app.schemas.assessment import (
    AnswerCreate,
    AnswerOut,
    AssessmentCreate,
    AssessmentOut,
    CompanyOut,
)

REQUIRED_QUESTIONS = {1, 6, 7, 8, 9, 10}
POLICY_DETAIL_QUESTIONS = {2, 3, 4, 5}


def _validate_answers(answers: list[AnswerCreate]) -> None:
    if not answers:
        raise HTTPException(status_code=400, detail="Se requiere al menos una respuesta")

    by_question = {a.question_number: a.answer for a in answers}

    if len(by_question) != len(answers):
        raise HTTPException(status_code=400, detail="Hay números de pregunta duplicados")

    invalid = [q for q in by_question if q < 1 or q > 11]
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"Preguntas fuera de rango (1-11): {sorted(invalid)}",
        )

    missing_required = REQUIRED_QUESTIONS - by_question.keys()
    if missing_required:
        raise HTTPException(
            status_code=400,
            detail=f"Faltan preguntas obligatorias: {sorted(missing_required)}",
        )

    has_policy = by_question[1]
    policy_details = POLICY_DETAIL_QUESTIONS & by_question.keys()

    if not has_policy and policy_details:
        raise HTTPException(
            status_code=400,
            detail="Las preguntas 2 a 5 no aplican si no hay política de datos (pregunta 1)",
        )

    if has_policy:
        missing_policy = POLICY_DETAIL_QUESTIONS - by_question.keys()
        if missing_policy:
            raise HTTPException(
                status_code=400,
                detail=f"Faltan preguntas de detalle de política: {sorted(missing_policy)}",
            )

    if 11 in by_question and not by_question.get(10):
        raise HTTPException(
            status_code=400,
            detail="La pregunta 11 solo aplica si hay oficial de protección (pregunta 10)",
        )

    count = len(answers)
    if count == 6:
        if has_policy:
            raise HTTPException(
                status_code=400,
                detail="Con política de datos se esperan 10 u 11 respuestas, no 6",
            )
    elif count == 10:
        if not has_policy:
            raise HTTPException(
                status_code=400,
                detail="Sin política de datos se esperan 6 respuestas, no 10",
            )
    elif count == 11:
        if not has_policy or 11 not in by_question:
            raise HTTPException(
                status_code=400,
                detail="11 respuestas solo aplican con política y pregunta complementaria 11",
            )
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Cantidad de respuestas inválida: {count} (se esperan 6, 10 u 11)",
        )


def _to_assessment_out(assessment, answers) -> AssessmentOut:
    if not assessment.company:
        raise HTTPException(status_code=500, detail="Empresa asociada a la evaluación no encontrada")
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
    _validate_answers(payload.answers)

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
