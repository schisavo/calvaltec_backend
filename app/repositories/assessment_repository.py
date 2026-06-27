from sqlalchemy.orm import Session, joinedload

from app.models.answer import Answer
from app.models.assessment import Assessment
from app.models.company import Company
from app.models.compliance_progress import ComplianceProgress
from app.models.recommendation import Recommendation
from app.schemas.assessment import AssessmentCreate


def get_assessment(db: Session, assessment_id: int):
    assessment = (
        db.query(Assessment)
        .options(joinedload(Assessment.company))
        .filter(Assessment.id == assessment_id)
        .first()
    )
    if not assessment:
        return None, []
    answers = (
        db.query(Answer)
        .filter(Answer.assessment_id == assessment_id)
        .order_by(Answer.question_number)
        .all()
    )
    return assessment, answers


def create_assessment(db: Session, payload: AssessmentCreate) -> Assessment:
    if payload.company_id:
        company = db.query(Company).filter(Company.id == payload.company_id).first()
        if not company:
            raise ValueError(f"Empresa {payload.company_id} no encontrada")
    else:
        company = Company(
            name=payload.company.name,
            email=payload.company.email,
            nit=payload.company.nit,
            sector=payload.company.sector,
        )
        db.add(company)
        db.flush()

    assessment = Assessment(company_id=company.id, score=payload.score)
    db.add(assessment)
    db.flush()

    for item in payload.answers:
        db.add(
            Answer(
                assessment_id=assessment.id,
                question_number=item.question_number,
                answer=item.answer,
            )
        )

    db.commit()
    db.refresh(assessment)
    return assessment


def update_assessment(db: Session, assessment_id: int, score: float) -> Assessment | None:
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        return None
    assessment.score = score
    db.commit()
    db.refresh(assessment)
    return assessment


def delete_assessment(db: Session, assessment_id: int) -> bool:
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        return False

    db.query(Answer).filter(Answer.assessment_id == assessment_id).delete(
        synchronize_session=False
    )
    db.query(Recommendation).filter(Recommendation.assessment_id == assessment_id).delete(
        synchronize_session=False
    )
    db.query(ComplianceProgress).filter(
        ComplianceProgress.assessment_id == assessment_id
    ).delete(synchronize_session=False)

    db.delete(assessment)
    db.commit()
    return True


def get_recommendation(db: Session, assessment_id: int) -> Recommendation | None:
    return (
        db.query(Recommendation)
        .filter(Recommendation.assessment_id == assessment_id)
        .first()
    )


def list_assessments(db: Session, company_id: int | None = None, limit: int = 100) -> list[Assessment]:
    q = db.query(Assessment).order_by(Assessment.created_at.desc())
    if company_id is not None:
        q = q.filter(Assessment.company_id == company_id)
    return q.limit(limit).all()
