from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from fastapi import Depends
from app.core.security import verify_api_key

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_api_key(_: bool = Depends(verify_api_key)):
    return True