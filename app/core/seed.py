from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "12345"
AUDITOR_EMAIL = "auditor@gmail.com"
AUDITOR_PASSWORD = "12345"


def seed_admin_user(db: Session) -> None:
    existing = db.query(User).filter(User.email == ADMIN_EMAIL).first()
    if not existing:
        db.add(
            User(
                email=ADMIN_EMAIL,
                password_hash=hash_password(ADMIN_PASSWORD),
                name="Admin",
                role="admin",
            )
        )

    auditor = db.query(User).filter(User.email == AUDITOR_EMAIL).first()
    if not auditor:
        db.add(
            User(
                email=AUDITOR_EMAIL,
                password_hash=hash_password(AUDITOR_PASSWORD),
                name="Auditor Demo",
                role="auditor",
            )
        )

    db.commit()
