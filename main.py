from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

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
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "N8nApiKey": {
            "type": "apiKey",
            "in": "header",
            "name": "x-api-key",
            "description": "Clave para llamadas HTTP desde n8n (API_KEY_SECRET).",
        },
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Token JWT obtenido en POST /api/v1/auth/login.",
        },
    }
    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi


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
