from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import Settings, get_settings
from app.core.errors import register_error_handlers

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
        _require({"LOCAL_AUTH_SECRET": settings.local_auth_secret}, "AUTH_MODE=local")
        if not settings.local_users:
            raise RuntimeError(
                "LOCAL_USERS wajib berisi minimal satu akun untuk AUTH_MODE=local."
            )
        emails = [str(account.email).lower() for account in settings.local_users]
        duplicates = sorted({email for email in emails if emails.count(email) > 1})
        if duplicates:
            raise RuntimeError("LOCAL_USERS memuat email ganda: " + ", ".join(duplicates))
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
