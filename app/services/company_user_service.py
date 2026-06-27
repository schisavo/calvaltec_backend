from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.user import User


def ensure_user_company(db: Session, user: User) -> int | None:
    """Vincula company/evaluador a su empresa por company_id o por email."""
    if user.role not in ("company", "evaluador"):
        return user.company_id
    if user.company_id is not None:
        return user.company_id

    company = (
        db.query(Company)
        .filter(Company.email == user.email.lower())
        .order_by(Company.id.desc())
        .first()
    )
    if not company:
        return None

    user.company_id = company.id
    db.add(user)
    db.commit()
    db.refresh(user)
    return company.id


def link_user_to_company(db: Session, user: User, company_id: int) -> None:
    if user.company_id == company_id:
        return
    user.company_id = company_id
    db.add(user)
    db.commit()
    db.refresh(user)
