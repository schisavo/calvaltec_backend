from starlette.requests import Request
from sqlalchemy.orm import Session

from app.repositories.oauth_state_repository import (
    delete_oauth_state,
    get_oauth_state,
    save_oauth_state,
)


def _state_session_key(state: str) -> str:
    return f"_state_{state}"


def persist_oauth_session_states(request: Request, db: Session) -> None:
    for key, value in request.session.items():
        if not key.startswith("_state_") or not isinstance(value, dict):
            continue
        state = key.removeprefix("_state_")
        save_oauth_state(db, state, value)


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


def clear_oauth_session_state(request: Request, db: Session) -> None:
    state = request.query_params.get("state")
    if not state:
        return
    delete_oauth_state(db, state)
    request.session.pop(_state_session_key(state), None)
