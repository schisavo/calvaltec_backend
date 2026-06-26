from sqlalchemy import create_engine
from sqlalchemy import inspect, text
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.core.config import settings

LEGACY_TABLES = ("answer", "assessment", "company")

engine = create_engine(
    settings.database_url,
    echo=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def _drop_legacy_tables() -> None:
    inspector = inspect(engine)
    existing = set(inspector.get_table_names())
    tables_to_drop = [name for name in LEGACY_TABLES if name in existing]
    if not tables_to_drop:
        return

    with engine.begin() as conn:
        for table in tables_to_drop:
            conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))


def _ensure_schema_updates() -> None:
    statements = [
        "ALTER TABLE companies ADD COLUMN IF NOT EXISTS size VARCHAR DEFAULT 'mediana'",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id)",
    ]
    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))


def init_db() -> None:
    import app.models  # noqa: F401
    from app.core.seed import seed_admin_user

    _drop_legacy_tables()
    SQLModel.metadata.create_all(engine)
    _ensure_schema_updates()

    db = SessionLocal()
    try:
        seed_admin_user(db)
    finally:
        db.close()
