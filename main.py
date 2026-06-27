from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.api.v1 import assessments, auth, chat, companies, compliance, n8n_routes, recommendations, users
from app.core.config import settings
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="FastAPI Supabase Demo",
    description="API REST con FastAPI + Supabase",
    version="0.1.0",
    lifespan=lifespan,
)

_DEFAULT_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
]


def _cors_origins() -> list[str]:
    origins = list(_DEFAULT_ORIGINS)
    if settings.FRONTEND_URL and settings.FRONTEND_URL not in origins:
        origins.append(settings.FRONTEND_URL.rstrip("/"))
    return origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
_is_https = bool(
    settings.BACKEND_PUBLIC_URL and settings.BACKEND_PUBLIC_URL.startswith("https://")
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.JWT_SECRET,
    max_age=900,
    same_site="none" if _is_https else "lax",
    https_only=_is_https,
)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")


@app.get("/")
def root():
    return {"message": "API funcionando en Render 🚀"}


app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(companies.router, prefix="/api/v1", tags=["companies"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(assessments.router, prefix="/api/v1", tags=["assessments"])
app.include_router(recommendations.router, prefix="/api/v1", tags=["recommendations"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(compliance.router, prefix="/api/v1", tags=["compliance"])
app.include_router(n8n_routes.router, prefix="/api/v1", tags=["n8n"])
# uvicorn main:app --reload
