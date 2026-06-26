from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Supabase Demo",
    description="API REST con FastAPI + Supabase",
    version="0.1.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc"      # Documentación alternativa
)

@app.get("/")
def root():
    return {"message": "API funcionando en Render 🚀"}

@app.get("/ping")
def ping():
    return {"status": "ok"}


# uvicorn main:app --reload
