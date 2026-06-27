from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.models.company import Company
from app.schemas.company import CompanyUpdate


def get_company(db: Session, company_id: int) -> Company | None:
    return db.query(Company).filter(Company.id == company_id).first()


def list_companies(db: Session) -> list[Company]:
    return db.query(Company).order_by(Company.name).all()


def update_company(db: Session, company: Company, payload: CompanyUpdate) -> Company:
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(company, key, value)
    db.commit()
    db.refresh(company)
    return company
