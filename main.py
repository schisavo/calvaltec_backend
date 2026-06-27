from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import assessments, auth, chat, companies, compliance, n8n_routes, recommendations, users
from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="FastAPI Supabase Demo",
    description="API REST con FastAPI + Supabase",
    version="0.1.0",
    docs_url="/docs",          # Swagger UI abierto
    redoc_url="/redoc",        # ReDoc abierto
    openapi_url="/openapi.json",  # Esquema abierto
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API funcionando en Render 🚀"}

# Routers
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(companies.router, prefix="/api/v1", tags=["companies"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(assessments.router, prefix="/api/v1", tags=["assessments"])
app.include_router(recommendations.router, prefix="/api/v1", tags=["recommendations"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(compliance.router, prefix="/api/v1", tags=["compliance"])
app.include_router(n8n_routes.router, prefix="/api/v1", tags=["n8n"])

# uvicorn main:app --reload