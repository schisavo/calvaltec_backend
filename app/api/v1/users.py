from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services.user_service import (
    create_user_data, get_user_data, get_users_data,
    update_user_data, delete_user_data
)

router = APIRouter()

@router.post("/users", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return create_user_data(db, payload)

@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return get_users_data(db)

@router.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_data(db, user_id)

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return update_user_data(db, user_id, payload)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user_data(db, user_id)
