from uuid import NAMESPACE_URL, uuid5

import httpx
from fastapi import APIRouter, Depends

from app.core.config import LocalAccount, Settings, get_settings
from app.core.errors import ApiError
from app.core.security import create_local_token, decode_access_token
from app.dependencies import get_current_user, user_from_claims
from app.schemas.auth import AuthResponse, LoginRequest, User

router = APIRouter(tags=["auth"])


@router.post("/auth/login", response_model=AuthResponse)
def login(
    payload: LoginRequest, settings: Settings = Depends(get_settings)
) -> AuthResponse:
    if settings.auth_mode.lower() == "local":
        return _local_login(payload, settings)
    return _supabase_login(payload, settings)


@router.get("/auth/me", response_model=User)
def me(user: User = Depends(get_current_user)) -> User:
    return user


def _local_user(account: LocalAccount) -> User:
    user_id = uuid5(
        NAMESPACE_URL,
        f"growpath-local:{account.tenant_id}:{account.email}",
    )
    return User(
        id=user_id,
        tenant_id=account.tenant_id,
        email=account.email,
        full_name=account.full_name,
        role=account.role,
        status="active",
    )


def _local_login(payload: LoginRequest, settings: Settings) -> AuthResponse:
    account = next(
        (
            item
            for item in settings.local_users
            if str(item.email).lower() == payload.email.lower()
        ),
        None,
    )
    if account is None or payload.password != account.password:
        raise ApiError(
            401,
            "AUTH_INVALID_CREDENTIALS",
            "Kredensial tidak valid",
            "Email atau kata sandi salah.",
        )
    user = _local_user(account)
    token, expires_in = create_local_token(
        settings,
        {
            "sub": str(user.id),
            "tenant_id": str(user.tenant_id),
            "role": user.role,
            "email": user.email,
            "full_name": user.full_name,
            "status": user.status,
        },
    )
    return AuthResponse(access_token=token, expires_in=expires_in, user=user)


def _supabase_login(payload: LoginRequest, settings: Settings) -> AuthResponse:
    if not settings.supabase_url or not settings.supabase_anon_key:
        raise RuntimeError(
            "SUPABASE_URL dan SUPABASE_ANON_KEY wajib diisi untuk AUTH_MODE=supabase."
        )
    url = f"{settings.supabase_url.rstrip('/')}/auth/v1/token"
    try:
        response = httpx.post(
            url,
            params={"grant_type": "password"},
            headers={"apikey": settings.supabase_anon_key},
            json={"email": payload.email, "password": payload.password},
            timeout=10.0,
        )
    except httpx.HTTPError as exc:
        raise ApiError(
            502,
            "AUTH_UPSTREAM_UNAVAILABLE",
            "Layanan autentikasi tidak tersedia",
            "Coba lagi beberapa saat lagi.",
        ) from exc
    if response.status_code >= 400:
        raise ApiError(
            401,
            "AUTH_INVALID_CREDENTIALS",
            "Kredensial tidak valid",
            "Email atau kata sandi salah.",
        )
    body = response.json()
    token = body["access_token"]
    return AuthResponse(
        access_token=token,
        refresh_token=body.get("refresh_token", ""),
        expires_in=int(body.get("expires_in", 3600)),
        user=user_from_claims(decode_access_token(token, settings)),
    )
