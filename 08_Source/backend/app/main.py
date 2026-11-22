from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import Settings, get_settings
from app.core.errors import register_error_handlers

API_VERSION = "0.1.0"


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or get_settings()
    _validate_settings(resolved)

    app = FastAPI(title="Growpath API", version=API_VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
    register_error_handlers(app)
    app.include_router(api_router)
    return app


def _validate_settings(settings: Settings) -> None:
    mode = settings.auth_mode.lower()
    if mode not in {"local", "supabase"}:
        raise RuntimeError("AUTH_MODE harus 'local' atau 'supabase'.")
    if settings.app_env.lower() == "production" and mode == "local":
        raise RuntimeError("AUTH_MODE=local tidak boleh dipakai saat APP_ENV=production.")
    if mode == "local":
        required = {
            "LOCAL_AUTH_SECRET": settings.local_auth_secret,
            "LOCAL_USER_EMAIL": settings.local_user_email,
            "LOCAL_USER_PASSWORD": settings.local_user_password,
            "LOCAL_USER_TENANT_ID": settings.local_user_tenant_id,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise RuntimeError(
                "Variabel wajib untuk AUTH_MODE=local belum diisi: " + ", ".join(missing)
            )


app = create_app()
