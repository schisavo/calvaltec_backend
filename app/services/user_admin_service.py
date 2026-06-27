from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.company import Company
from app.repositories.user_repository import create_user, get_user_by_email, list_users
from app.schemas.auth import AdminUserCreate, UserOut


def _user_out(db: Session, user) -> UserOut:
    company = None
    if user.company_id:
        company = db.query(Company).filter(Company.id == user.company_id).first()
    return UserOut(
        id=user.id,
        email=user.email,
        name=user.name,
        role=user.role,
        company_id=user.company_id,
        company_name=company.name if company else None,
        company_email=company.email if company else None,
        company_nit=company.nit if company else None,
        company_sector=company.sector if company else None,
    )


def list_users_data(db: Session) -> list[UserOut]:
    return [_user_out(db, u) for u in list_users(db)]


def create_user_admin(db: Session, payload: AdminUserCreate) -> UserOut:
    if get_user_by_email(db, payload.email.lower()):
        raise HTTPException(status_code=409, detail="El correo ya está registrado")
    user = create_user(
        db,
        payload.email.lower(),
        payload.password,
        payload.name,
        payload.role,
    )
    return _user_out(db, user)
