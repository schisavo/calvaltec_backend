import json
import urllib.error
import urllib.request

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.auth_deps import get_current_user
from app.api.deps import get_db
from app.core.config import settings
from app.models.company import Company
from app.models.user import User
from app.schemas.chat import ChatMessageIn
from app.services.auth_service import _user_out
from app.services.company_user_service import ensure_user_company

router = APIRouter()


def _user_payload(db: Session, user: User) -> dict:
    if user.role in ("company", "evaluador"):
        ensure_user_company(db, user)
    company = None
    if user.company_id:
        company = db.query(Company).filter(Company.id == user.company_id).first()
    out = _user_out(user, company)
    return out.model_dump(exclude_none=True)


def _normalize_n8n_response(data: object) -> dict:
    """Acepta { reply }, { output }, o [{ output }] de nodos IA de n8n."""
    if isinstance(data, list) and data:
        data = data[0]
    if not isinstance(data, dict):
        return {"reply": str(data)}

    for key in ("reply", "message", "response", "output", "text", "answer", "content"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return {**data, "reply": value.strip()}

    nested = data.get("json")
    if isinstance(nested, dict):
        return _normalize_n8n_response(nested)

    return data


def _forward_to_n8n(payload: dict) -> dict:
    url = settings.N8N_CHAT_WEBHOOK_URL
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8")
            if not raw.strip():
                return {"reply": "El asistente no devolvió contenido."}
            parsed = json.loads(raw)
            return _normalize_n8n_response(parsed)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        if exc.code == 404:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=(
                    f"El webhook de n8n respondió 404. URL configurada: {url}. "
                    "Copia la Production URL exacta del nodo Webhook en n8n, "
                    "actívala en BACKEND/.env como N8N_CHAT_WEBHOOK_URL y republica el workflow."
                ),
            ) from exc
        detail = body[:500] if body else f"Error del webhook n8n ({exc.code})"
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail,
        ) from exc
    except urllib.error.URLError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="No se pudo contactar el webhook de n8n. Verifica la URL y que el workflow esté activo.",
        ) from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="El webhook de n8n devolvió una respuesta no válida (JSON).",
        ) from exc


@router.post("/chat")
def chat_with_assistant(
    payload: ChatMessageIn,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    auth_header = request.headers.get("Authorization", "")
    access_token = auth_header[7:] if auth_header.startswith("Bearer ") else ""

    api_url = f"{request.url.scheme}://{request.url.netloc}"
    context = payload.context.model_dump() if payload.context else {"pathname": ""}

    n8n_payload = {
        "message": payload.message,
        "session_id": payload.session_id,
        "history": [item.model_dump() for item in payload.history],
        "user": _user_payload(db, user),
        "access_token": access_token,
        "api_url": api_url,
        "context": context,
    }

    return _forward_to_n8n(n8n_payload)
