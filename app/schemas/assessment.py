from pydantic import BaseModel
from typing import List

class CompanyOut(BaseModel):
    id: int
    name: str

class AnswerOut(BaseModel):
    question: str
    answer: bool

class AssessmentOut(BaseModel):
    assessment_id: int
    company: CompanyOut
    score: float
    answers: List[AnswerOut]
