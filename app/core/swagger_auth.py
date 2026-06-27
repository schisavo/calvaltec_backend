from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings

PROTECTED_DOC_PATHS = ("/docs", "/redoc", "/openapi.json")


class SwaggerApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path in PROTECTED_DOC_PATHS or path.startswith("/docs/"):
            api_key = request.headers.get("X-API-Key") or request.query_params.get("api_key")
            if not api_key or api_key != settings.SWAGGER_API_KEY:
                return JSONResponse(
                    status_code=401,
                    content={
                        "detail": "API key inválida o ausente. Usa el header X-API-Key o ?api_key= en la URL.",
                    },
                )
        return await call_next(request)
