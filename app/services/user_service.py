from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.user_repository import (
    create_user, get_user, get_users, update_user, delete_user
)
from app.schemas.user import UserCreate, UserUpdate, UserOut

def create_user_data(db: Session, payload: UserCreate) -> UserOut:
    user = create_user(db, payload.email, payload.password, payload.name, payload.role, payload.company_id)
    return UserOut.from_orm(user)

def get_user_data(db: Session, user_id: int) -> UserOut:
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserOut.from_orm(user)

def get_users_data(db: Session) -> list[UserOut]:
    return [UserOut.from_orm(u) for u in get_users(db)]

def update_user_data(db: Session, user_id: int, payload: UserUpdate) -> UserOut:
    user = update_user(db, user_id, payload.name, payload.role, payload.company_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserOut.from_orm(user)

def delete_user_data(db: Session, user_id: int) -> dict:
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"detail": "Usuario eliminado correctamente"}
