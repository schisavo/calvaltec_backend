from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.company import Company
from app.repositories.user_repository import create_user, get_user_by_email
from app.schemas.auth import AuthResponse
from app.services.auth_service import _user_out
from app.services.company_user_service import ensure_user_company


def oauth_login_service(db: Session, user_info: dict | None) -> AuthResponse:
    if not user_info or not user_info.get("email"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google no devolvió el correo del usuario.",
        )

    email = user_info["email"].lower()
    user = get_user_by_email(db, email)
    if not user:
        user = create_user(
            db,
            email=email,
            password="oauth-placeholder",
            name=user_info.get("name") or email.split("@")[0],
            role="company",
            company_id=None,
        )

    if user.role in ("company", "evaluador"):
        ensure_user_company(db, user)

    company = None
    if user.company_id:
        company = db.query(Company).filter(Company.id == user.company_id).first()

    token, expires_in = create_access_token(user_id=user.id, email=user.email, role=user.role)
    return AuthResponse(
        access_token=token,
        expires_in=expires_in,
        user=_user_out(user, company),
    )
