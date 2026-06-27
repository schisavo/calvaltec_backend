import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from joserfc import jwt
from joserfc.jwk import OctKey

from app.core.config import settings

TOKEN_EXPIRE_HOURS = 24


def _jwt_key() -> OctKey:
    return OctKey.import_key(settings.JWT_SECRET)


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"{salt}${pwd_hash.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    salt, pwd_hash = hashed.split("$", 1)
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return secrets.compare_digest(candidate.hex(), pwd_hash)


def create_access_token(*, user_id: int, email: str, role: str) -> tuple[str, int]:
    expires_in = TOKEN_EXPIRE_HOURS * 3600
    exp = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    token = jwt.encode(
        {"alg": "HS256"},
        {"sub": str(user_id), "email": email, "role": role, "exp": int(exp.timestamp())},
        _jwt_key(),
    )
    return token, expires_in


def decode_access_token(token: str) -> dict:
    decoded = jwt.decode(token, _jwt_key())
    return dict(decoded.claims)
