from datetime import UTC, datetime, timedelta
from functools import lru_cache
from typing import Any

import jwt
from jwt import PyJWKClient

from app.core.config import Settings
from app.core.errors import ApiError

LOCAL_ISSUER = "growpath-local"


@lru_cache
def _jwks_client(jwks_url: str) -> PyJWKClient:
    return PyJWKClient(jwks_url)


def create_local_token(settings: Settings, claims: dict[str, Any]) -> tuple[str, int]:
    if settings.app_env.lower() == "production":
        raise RuntimeError("Token lokal tidak boleh dibuat saat APP_ENV=production.")
    ttl_seconds = settings.local_token_ttl_minutes * 60
    now = datetime.now(UTC)
    payload = {
        **claims,
        "iss": LOCAL_ISSUER,
        "iat": now,
        "exp": now + timedelta(seconds=ttl_seconds),
    }
    token = jwt.encode(payload, settings.local_auth_secret, algorithm="HS256")
    return token, ttl_seconds


def decode_access_token(token: str, settings: Settings) -> dict[str, Any]:
    try:
        if settings.auth_mode.lower() == "local":
            return jwt.decode(
                token,
                settings.local_auth_secret,
                algorithms=["HS256"],
                issuer=LOCAL_ISSUER,
                options={"verify_aud": False},
            )
        return _decode_supabase_token(token, settings)
    except jwt.PyJWTError as exc:
        raise ApiError(
            401,
            "AUTH_TOKEN_INVALID",
            "Token tidak valid",
            "Sesi tidak valid atau sudah kedaluwarsa.",
        ) from exc


def _decode_supabase_token(token: str, settings: Settings) -> dict[str, Any]:
    if not settings.supabase_url:
        raise RuntimeError("SUPABASE_URL wajib diisi untuk AUTH_MODE=supabase.")
    jwks_url = f"{settings.supabase_url.rstrip('/')}/auth/v1/.well-known/jwks.json"
    try:
        signing_key = _jwks_client(jwks_url).get_signing_key_from_jwt(token)
        return jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256", "ES256"],
            options={"verify_aud": False},
        )
    except jwt.PyJWTError:
        if settings.supabase_jwt_secret:
            return jwt.decode(
                token,
                settings.supabase_jwt_secret,
                algorithms=["HS256"],
                options={"verify_aud": False},
            )
        raise
