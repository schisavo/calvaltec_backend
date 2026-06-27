from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.models.company import Company
from app.repositories.assessment_repository import get_recommendation, list_assessments
from app.repositories.company_repository import get_company, list_companies, update_company
from app.schemas.company import CompanyOut, CompanySummary, CompanyUpdate


def _score_status(score: float) -> str:
    if score >= 80:
        return "Cumple"
    if score >= 60:
        return "Parcial"
    return "No cumple"


def company_to_out(company: Company) -> CompanyOut:
    return CompanyOut(
        id=company.id,
        name=company.name,
        email=company.email,
        nit=company.nit,
        sector=company.sector,
        size=getattr(company, "size", "mediana"),
        created_at=company.created_at,
    )


def get_company_data(db: Session, company_id: int) -> CompanyOut:
    company = get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return company_to_out(company)


def update_company_data(db: Session, company_id: int, payload: CompanyUpdate) -> CompanyOut:
    company = get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    updated = update_company(db, company, payload)
    return company_to_out(updated)


def list_companies_summary(db: Session) -> list[CompanySummary]:
    companies = list_companies(db)
    summaries: list[CompanySummary] = []
    for c in companies:
        assessments = list_assessments(db, company_id=c.id, limit=1)
        latest = assessments[0] if assessments else None
        count = db.query(Assessment).filter(Assessment.company_id == c.id).count()
        summaries.append(
            CompanySummary(
                id=c.id,
                name=c.name,
                email=c.email,
                nit=c.nit,
                sector=c.sector,
                size=getattr(c, "size", "mediana"),
                assessment_count=count,
                latest_score=latest.score if latest else None,
                latest_status=_score_status(latest.score) if latest else None,
            )
        )
    return summaries
