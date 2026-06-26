from sqlalchemy.orm import Session
from app.repositories.assessment_repository import (
    get_assessment,
    create_assessment,
    update_assessment,
    delete_assessment
)
from app.schemas.assessment import AssessmentOut, CompanyOut, AnswerOut

def get_assessment_data(db: Session, assessment_id: int) -> AssessmentOut:
    assessment, answers = get_assessment(db, assessment_id)
    return AssessmentOut(
        assessment_id=assessment.id,
        company=CompanyOut(id=assessment.company.id, name=assessment.company.name),
        score=assessment.score,
        answers=[AnswerOut(question=a.question, answer=a.answer) for a in answers]
    )

def create_assessment_data(db: Session, assessment: AssessmentOut) -> AssessmentOut:
    new_assessment = create_assessment(db, assessment)
    return AssessmentOut(
        assessment_id=new_assessment.id,
        company=CompanyOut(id=new_assessment.company.id, name=new_assessment.company.name),
        score=new_assessment.score,
        answers=[]
    )

def update_assessment_data(db: Session, assessment_id: int, assessment: AssessmentOut) -> AssessmentOut:
    updated = update_assessment(db, assessment_id, assessment)
    return AssessmentOut(
        assessment_id=updated.id,
        company=CompanyOut(id=updated.company.id, name=updated.company.name),
        score=updated.score,
        answers=[AnswerOut(question=a.question, answer=a.answer) for a in updated.answers]
    )

def delete_assessment_data(db: Session, assessment_id: int) -> dict:
    delete_assessment(db, assessment_id)
    return {"message": f"Assessment {assessment_id} eliminado"}
