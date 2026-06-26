from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    name: str
    role: str
    company_id: Optional[int] = None

class UserCreate(UserBase):
    password: str  # plain text, se convertirá en hash

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    company_id: Optional[int] = None

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
