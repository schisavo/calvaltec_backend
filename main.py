from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from app.api.v1 import assessments, auth, chat, companies, compliance, n8n_routes, recommendations, users
from app.core.config import settings
from app.core.database import init_db
from app.core.swagger_auth import SwaggerApiKeyMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="FastAPI Supabase Demo",
    description="API REST con FastAPI + Supabase",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SwaggerApiKeyMiddleware)


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
        "SwaggerApiKey": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "Clave para acceder a /docs y documentación Swagger.",
        },
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


def _validate_swagger_api_key(
    api_key: str | None = None,
    x_api_key: str | None = None,
) -> str:
    key = api_key or x_api_key
    if not key or key != settings.SWAGGER_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "API key inválida o ausente. Usa el header X-API-Key o ?api_key= en la URL."
            ),
        )
    return key


@app.get("/openapi.json", include_in_schema=False)
def openapi_json(
    api_key: str | None = Query(default=None),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    _validate_swagger_api_key(api_key, x_api_key)
    return JSONResponse(custom_openapi())


@app.get("/docs", include_in_schema=False)
def swagger_docs(
    api_key: str | None = Query(default=None),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    key = _validate_swagger_api_key(api_key, x_api_key)
    return get_swagger_ui_html(
        openapi_url=f"/openapi.json?api_key={key}",
        title=f"{app.title} - Swagger UI",
    )


@app.get("/redoc", include_in_schema=False)
def redoc_docs(
    api_key: str | None = Query(default=None),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    key = _validate_swagger_api_key(api_key, x_api_key)
    return get_redoc_html(
        openapi_url=f"/openapi.json?api_key={key}",
        title=f"{app.title} - ReDoc",
    )


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
