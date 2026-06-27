from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.models.user import User
from app.repositories.assessment_repository import get_assessment
from app.services.company_user_service import ensure_user_company


def assert_assessment_access(db: Session, user: User, assessment_id: int) -> Assessment:
    if user.role in ("company", "evaluador"):
        ensure_user_company(db, user)
    assessment, _ = get_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    if user.role in ("admin", "auditor"):
        return assessment
    if user.company_id is None:
        raise HTTPException(status_code=403, detail="Usuario sin empresa asignada")
    if user.company_id != assessment.company_id:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return assessment


def assessment_list_company_scope(user: User, company_id: int | None = None) -> int | None:
    """None = todas las empresas (admin/auditor). int = filtrar por empresa."""
    if user.role in ("admin", "auditor"):
        return company_id
    return user.company_id
