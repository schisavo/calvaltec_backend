from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.oauth_state import OAuthState

OAUTH_STATE_TTL = timedelta(minutes=15)


def purge_expired_oauth_states(db: Session) -> None:
    now = datetime.now(timezone.utc)
    db.query(OAuthState).filter(OAuthState.expires_at < now).delete(synchronize_session=False)


def save_oauth_state(
    db: Session, state: str, payload: dict, return_origin: str | None = None
) -> None:
    purge_expired_oauth_states(db)
    expires_at = datetime.now(timezone.utc) + OAUTH_STATE_TTL
    row = db.get(OAuthState, state)
    if row:
        row.payload = payload
        row.return_origin = return_origin
        row.expires_at = expires_at
    else:
        db.add(
            OAuthState(
                state=state,
                payload=payload,
                return_origin=return_origin,
                expires_at=expires_at,
            )
        )
    db.commit()


def get_oauth_state(db: Session, state: str) -> OAuthState | None:
    row = db.get(OAuthState, state)
    if not row:
        return None
    if row.expires_at < datetime.now(timezone.utc):
        db.delete(row)
        db.commit()
        return None
    return row


def delete_oauth_state(db: Session, state: str) -> None:
    row = db.get(OAuthState, state)
    if row:
        db.delete(row)
        db.commit()
