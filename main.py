from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import assessments

app = FastAPI(
    title="FastAPI Supabase Demo",
    description="API REST con FastAPI + Supabase",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
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
app.include_router(assessments.router, prefix="/api/v1", tags=["assessments"])


# uvicorn main:app --reload
