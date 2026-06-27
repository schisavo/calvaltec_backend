from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.models.company import Company
from app.repositories.assessment_repository import get_recommendation, list_assessments
from app.schemas.assessment import AssessmentSummary


def _score_status(score: float) -> str:
    if score >= 80:
        return "Cumple"
    if score >= 60:
        return "Parcial"
    return "No cumple"


def list_assessments_summary(db: Session, company_id: int | None = None) -> list[AssessmentSummary]:
    rows = list_assessments(db, company_id=company_id)
    summaries: list[AssessmentSummary] = []
    for a in rows:
        rec = get_recommendation(db, a.id)
        nivel = None
        if rec and isinstance(rec.report, dict):
            nivel = rec.report.get("nivel_riesgo")
        company = db.query(Company).filter(Company.id == a.company_id).first()
        summaries.append(
            AssessmentSummary(
                id=a.id,
                company_id=a.company_id,
                company_name=company.name if company else "—",
                score=a.score,
                status=_score_status(a.score),
                created_at=a.created_at,
                has_recommendation=rec is not None,
                nivel_riesgo=str(nivel) if nivel else None,
            )
        )
    return summaries
