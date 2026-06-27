from urllib.parse import urlparse

from starlette.requests import Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories.oauth_state_repository import (
    delete_oauth_state,
    get_oauth_state,
    save_oauth_state,
)


def _state_session_key(state: str) -> str:
    return f"_state_{state}"


def _is_allowed_return_origin(origin: str) -> bool:
    parsed = urlparse(origin)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False

    host = parsed.hostname or ""
    port = parsed.port
    configured = settings.FRONTEND_URL.rstrip("/")
    configured_host = urlparse(configured).hostname or ""

    if origin.rstrip("/") == configured.rstrip("/"):
        return True

    if host in {"localhost", "127.0.0.1"} and port in {5173, 3000, None}:
        return True

    if host.endswith(".onrender.com"):
        return True

    if configured_host and host == configured_host:
        return True

    return False


def normalize_return_origin(origin: str | None) -> str | None:
    if not origin:
        return None
    cleaned = origin.strip().rstrip("/")
    if not _is_allowed_return_origin(cleaned):
        return None
    return cleaned


def persist_oauth_session_states(
    request: Request, db: Session, return_origin: str | None = None
) -> None:
    safe_origin = normalize_return_origin(return_origin)
    for key, value in request.session.items():
        if not key.startswith("_state_") or not isinstance(value, dict):
            continue
        state = key.removeprefix("_state_")
        save_oauth_state(db, state, value, return_origin=safe_origin)


def restore_oauth_session_state(request: Request, db: Session) -> None:
    state = request.query_params.get("state")
    if not state:
        return

    key = _state_session_key(state)
    if key in request.session:
        return

    row = get_oauth_state(db, state)
    if row:
        request.session[key] = row.payload


def resolve_frontend_return_url(request: Request, db: Session) -> str:
    state = request.query_params.get("state")
    if state:
        row = get_oauth_state(db, state)
        if row and row.return_origin:
            return row.return_origin.rstrip("/")
    return settings.FRONTEND_URL.rstrip("/")


def clear_oauth_session_state(request: Request, db: Session) -> None:
    state = request.query_params.get("state")
    if not state:
        return
    delete_oauth_state(db, state)
    request.session.pop(_state_session_key(state), None)
