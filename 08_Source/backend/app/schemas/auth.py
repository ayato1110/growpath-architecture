from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

Role = Literal["umkm", "pendamping", "mentor", "admin_b2g", "admin_platform"]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class User(BaseModel):
    id: UUID
    tenant_id: UUID
    email: EmailStr
    full_name: str
    phone: str | None = None
    role: Role
    status: Literal["active", "invited", "suspended", "deleted"] = "active"
    last_login_at: datetime | None = None


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int
    user: User


class Health(BaseModel):
    status: Literal["ok", "degraded"] = "ok"
    version: str
    dependencies: dict[str, str] = Field(default_factory=dict)
