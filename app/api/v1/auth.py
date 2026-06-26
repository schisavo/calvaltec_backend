from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import verify_password
from app.models.company import Company
from app.repositories.user_repository import get_user_by_email
from app.schemas.auth import LoginRequest, RegisterRequest, UserOut
from app.services.auth_service import register_company_user

router = APIRouter()


def _build_user_out(db: Session, user) -> UserOut:
    company = None
    if user.company_id:
        company = db.query(Company).filter(Company.id == user.company_id).first()
    return UserOut(
        email=user.email,
        name=user.name,
        role=user.role,
        company_id=user.company_id,
        company_name=company.name if company else None,
    )


@router.post("/auth/register", response_model=UserOut, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        return register_company_user(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/auth/login", response_model=UserOut)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email.lower())
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    return _build_user_out(db, user)


@router.get("/auth/oauth/{provider}")
def oauth_redirect(provider: str):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"OAuth con {provider} disponible próximamente. Usa registro o correo/contraseña.",
    )