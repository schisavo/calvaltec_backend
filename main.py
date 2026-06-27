from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import assessments, auth, chat, companies, recommendations
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="FastAPI Supabase Demo",
    description="API REST con FastAPI + Supabase",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
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

@app.get("/ping")
def ping():
    return {"status": "ok"}

# Aquí se agregan las rutas del CRUD
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(companies.router, prefix="/api/v1", tags=["companies"])
app.include_router(assessments.router, prefix="/api/v1", tags=["assessments"])
app.include_router(recommendations.router, prefix="/api/v1", tags=["recommendations"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])


# uvicorn main:app --reload
