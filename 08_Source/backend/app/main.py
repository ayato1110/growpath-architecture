from uuid import UUID

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import Settings, get_settings
from app.core.errors import register_error_handlers
from app.schemas.auth import ROLES

API_VERSION = "0.1.0"


def create_app() -> FastAPI:
    settings = get_settings()
    validate_settings(settings)

    app = FastAPI(title="Growpath API", version=API_VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
    register_error_handlers(app)
    app.include_router(api_router)
    return app


def validate_settings(settings: Settings) -> None:
    mode = settings.auth_mode.lower()
    if mode not in {"local", "supabase"}:
        raise RuntimeError("AUTH_MODE harus 'local' atau 'supabase'.")
    if settings.app_env.lower() == "production" and mode == "local":
        raise RuntimeError("AUTH_MODE=local tidak boleh dipakai saat APP_ENV=production.")
    if mode == "local":
        _require(
            {
                "LOCAL_AUTH_SECRET": settings.local_auth_secret,
                "LOCAL_USER_EMAIL": settings.local_user_email,
                "LOCAL_USER_PASSWORD": settings.local_user_password,
                "LOCAL_USER_TENANT_ID": settings.local_user_tenant_id,
            },
            "AUTH_MODE=local",
        )
        try:
            UUID(settings.local_user_tenant_id)
        except ValueError as exc:
            raise RuntimeError("LOCAL_USER_TENANT_ID harus UUID yang valid.") from exc
        if settings.local_user_role not in ROLES:
            raise RuntimeError(
                "LOCAL_USER_ROLE harus salah satu dari: " + ", ".join(ROLES)
            )
        if len(settings.local_auth_secret) < 32:
            raise RuntimeError("LOCAL_AUTH_SECRET minimal 32 karakter.")
    else:
        _require(
            {
                "SUPABASE_URL": settings.supabase_url,
                "SUPABASE_ANON_KEY": settings.supabase_anon_key,
            },
            "AUTH_MODE=supabase",
        )


def _require(values: dict[str, str | None], mode: str) -> None:
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise RuntimeError(
            f"Variabel wajib untuk {mode} belum diisi: " + ", ".join(missing)
        )


app = create_app()
