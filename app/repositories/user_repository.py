from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.created_at.desc()).all()


def create_user(db: Session, *, email: str, password_hash: str, name: str, role: str, company_id: int | None = None) -> User:
    user = User(
        email=email.lower(),
        password_hash=password_hash,
        name=name,
        role=role,
        company_id=company_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
