from functools import lru_cache
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.schemas.auth import Role


class LocalAccount(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)
    role: Role
    tenant_id: UUID
    full_name: str = Field(min_length=1, max_length=120)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_env: str = "development"
    auth_mode: str = "local"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    supabase_url: str | None = None
    supabase_anon_key: str | None = None
    supabase_jwt_secret: str | None = None

    local_auth_secret: str = ""
    local_token_ttl_minutes: int = 60
    local_users: list[LocalAccount] = []

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
