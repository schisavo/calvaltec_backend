from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.company import Company
from app.models.user import User
from app.schemas.auth import RegisterRequest, UserOut


def _user_out(user: User, company: Company | None = None) -> UserOut:
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


def register_company_user(db: Session, payload: RegisterRequest) -> UserOut:
    """Registro público: siempre crea usuario con rol company. Admin y auditor los crea un admin."""
    email = payload.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise ValueError("El correo ya está registrado")

    company = Company(
        name=payload.company_name,
        email=email,
        nit=payload.nit,
        sector=payload.sector,
        size=payload.size,
    )
    db.add(company)
    db.flush()

    user = User(
        email=email,
        password_hash=hash_password(payload.password),
        name=payload.contact_name,
        role="company",
        company_id=company.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _user_out(user, company)
