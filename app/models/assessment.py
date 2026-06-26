from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Company(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class Assessment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="company.id")
    score: float

    company: Optional[Company] = Relationship()
