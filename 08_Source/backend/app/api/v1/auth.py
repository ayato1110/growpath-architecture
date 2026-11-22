from uuid import NAMESPACE_URL, uuid5

import httpx
from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.core.errors import ApiError
from app.core.security import create_local_token
from app.dependencies import get_current_user
from app.schemas.auth import AuthResponse, LoginRequest, Role, User

router = APIRouter(tags=["auth"])

ROLES: tuple[Role, ...] = (
    "umkm",
    "pendamping",
    "mentor",
    "admin_b2g",
    "admin_platform",
)


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


def _local_user(settings: Settings) -> User:
    user_id = uuid5(
        NAMESPACE_URL,
        f"growpath-local:{settings.local_user_tenant_id}:{settings.local_user_email}",
    )
    return User(
        id=user_id,
        tenant_id=settings.local_user_tenant_id,
        email=settings.local_user_email,
        full_name=settings.local_user_name,
        role=settings.local_user_role,
        status="active",
    )


def _local_login(payload: LoginRequest, settings: Settings) -> AuthResponse:
    email_match = payload.email.lower() == settings.local_user_email.lower()
    password_match = payload.password == settings.local_user_password
    if not (email_match and password_match):
        raise ApiError(
            401,
            "AUTH_INVALID_CREDENTIALS",
            "Kredensial tidak valid",
            "Email atau kata sandi salah.",
        )
    user = _local_user(settings)
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
    supabase_user = body.get("user") or {}
    metadata = supabase_user.get("user_metadata") or {}
    app_metadata = supabase_user.get("app_metadata") or {}
    role = app_metadata.get("role", "umkm")
    tenant_id = app_metadata.get("tenant_id")
    if role not in ROLES or not tenant_id:
        raise ApiError(
            401,
            "AUTH_CLAIM_INVALID",
            "Klaim token tidak lengkap",
            "Token tidak memuat peran atau tenant_id.",
        )
    user = User(
        id=supabase_user["id"],
        tenant_id=tenant_id,
        email=supabase_user["email"],
        full_name=metadata.get("full_name") or supabase_user["email"].split("@")[0],
        phone=supabase_user.get("phone"),
        role=role,
        status="active",
    )
    return AuthResponse(
        access_token=body["access_token"],
        refresh_token=body.get("refresh_token", ""),
        expires_in=int(body.get("expires_in", 3600)),
        user=user,
    )
