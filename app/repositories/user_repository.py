from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user(db: Session, user_id: int) -> User | None:
    return get_user_by_id(db, user_id)


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.created_at.desc()).all()


def get_users(db: Session) -> list[User]:
    return db.query(User).all()


def create_user(
    db: Session,
    email: str,
    password: str,
    name: str,
    role: str,
    company_id: int | None = None,
) -> User:
    user = User(
        email=email.lower(),
        password_hash=hash_password(password),
        name=name,
        role=role,
        company_id=company_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(
    db: Session,
    user_id: int,
    name: str | None,
    role: str | None,
    company_id: int | None,
) -> User | None:
    user = get_user(db, user_id)
    if user:
        if name:
            user.name = name
        if role:
            user.role = role
        if company_id is not None:
            user.company_id = company_id
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
