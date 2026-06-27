from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.assessment import Assessment
from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyOut, CompanySummary, CompanyUpdate
from app.services.company_service import (
    get_company_data,
    list_companies_summary,
    update_company_data,
)

router = APIRouter()


@router.get("/companies", response_model=list[CompanySummary])
def list_companies_endpoint(db: Session = Depends(get_db)):
    return list_companies_summary(db)


@router.get("/companies/{company_id}", response_model=CompanyOut)
def get_company_endpoint(
    company_id: int,
    db: Session = Depends(get_db),
):
    return get_company_data(db, company_id)


@router.patch("/companies/{company_id}", response_model=CompanyOut)
def update_company_endpoint(
    company_id: int,
    payload: CompanyUpdate,
    db: Session = Depends(get_db),
):
    return update_company_data(db, company_id, payload)


@router.get("/admin/stats")
def admin_stats(db: Session = Depends(get_db)):
    return {
        "companies": db.query(Company).count(),
        "assessments": db.query(Assessment).count(),
        "users": db.query(User).count(),
    }
