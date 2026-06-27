from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth_deps import get_current_user, require_roles
from app.api.deps import get_db
from app.models.assessment import Assessment
from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyOut, CompanySummary, CompanyUpdate
from app.services.company_service import (
    company_to_out,
    get_company_data,
    list_companies_summary,
    update_company_data,
)

router = APIRouter()


def _can_access_company(user: User, company_id: int) -> bool:
    if user.role in ("admin", "auditor"):
        return True
    return user.company_id == company_id


@router.get("/companies", response_model=list[CompanySummary])
def list_companies_endpoint(
    _: User = Depends(require_roles("admin", "auditor")),
    db: Session = Depends(get_db),
):
    return list_companies_summary(db)


@router.get("/companies/{company_id}", response_model=CompanyOut)
def get_company_endpoint(
    company_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not _can_access_company(user, company_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")
    return get_company_data(db, company_id)


@router.patch("/companies/{company_id}", response_model=CompanyOut)
def update_company_endpoint(
    company_id: int,
    payload: CompanyUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role not in ("admin", "company", "evaluador"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")
    if user.role in ("company", "evaluador") and user.company_id != company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")
    return update_company_data(db, company_id, payload)


@router.get("/admin/stats")
def admin_stats(
    _: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    return {
        "companies": db.query(Company).count(),
        "assessments": db.query(Assessment).count(),
        "users": db.query(User).count(),
    }
