from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth_deps import get_current_user, require_roles
from app.api.deps import get_db
from app.core.security import create_access_token, verify_password
from app.models.company import Company
from app.models.user import User
from app.repositories.user_repository import get_user_by_email
from app.schemas.auth import (
    AdminUserCreate,
    AuthResponse,
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    UserOut,
)
from app.services.auth_service import _user_out, register_company_user
from app.services.company_user_service import ensure_user_company
from app.services.user_admin_service import create_user_admin, list_users_data

router = APIRouter()


def _user_response(db: Session, user: User) -> UserOut:
    if user.role in ("company", "evaluador"):
        ensure_user_company(db, user)
    company = None
    if user.company_id:
        company = db.query(Company).filter(Company.id == user.company_id).first()
    return _user_out(user, company)


@router.post("/auth/register", response_model=AuthResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user_out = register_company_user(db, payload)
        user = get_user_by_email(db, payload.email.lower())
        token, expires_in = create_access_token(user_id=user.id, email=user.email, role=user.role)
        return AuthResponse(access_token=token, expires_in=expires_in, user=user_out)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/auth/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email.lower())
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    token, expires_in = create_access_token(user_id=user.id, email=user.email, role=user.role)
    return AuthResponse(access_token=token, expires_in=expires_in, user=_user_response(db, user))


@router.get("/auth/me", response_model=UserOut)
def me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _user_response(db, user)


@router.post("/auth/forgot-password", response_model=MessageResponse)
def forgot_password(_: ForgotPasswordRequest):
    return MessageResponse(
        message="Si el correo existe, recibirás instrucciones para restablecer tu contraseña."
    )


@router.get("/auth/oauth/{provider}")
def oauth_redirect(provider: str):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"OAuth con {provider} disponible próximamente. Usa correo y contraseña.",
    )


@router.get("/users", response_model=list[UserOut])
def list_users_endpoint(_: User = Depends(require_roles("admin")), db: Session = Depends(get_db)):
    return list_users_data(db)


@router.post("/users", response_model=UserOut, status_code=201)
def create_user_endpoint(
    payload: AdminUserCreate,
    _: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    return create_user_admin(db, payload)
