from sqlalchemy.orm import Session
from app.models.assessment import Assessment
from app.models.answer import Answer

def get_assessment(db: Session, assessment_id: int):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    answers = db.query(Answer).filter(Answer.assessment_id == assessment_id).all()
    return assessment, answers

def create_assessment(db: Session, assessment):
    new_assessment = Assessment(
        company_id=assessment.company.id,
        score=assessment.score
    )
    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)
    return new_assessment

def update_assessment(db: Session, assessment_id: int, assessment):
    db_assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    db_assessment.score = assessment.score
    db.commit()
    db.refresh(db_assessment)
    return db_assessment

def delete_assessment(db: Session, assessment_id: int):
    db_assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    db.delete(db_assessment)
    db.commit()
