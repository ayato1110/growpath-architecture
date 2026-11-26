from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.db import get_db
from app.core.errors import ApiError
from app.core.security import decode_access_token
from app.repositories.users import ensure_identity
from app.schemas.auth import ROLES, Role, User

bearer_scheme = HTTPBearer(auto_error=False)


def user_from_claims(claims: dict) -> User:
    metadata = claims.get("app_metadata") or {}
    claim_role = claims.get("role")
    role = claim_role if claim_role in ROLES else metadata.get("app_role")
    tenant_id = claims.get("tenant_id") or metadata.get("tenant_id")
    email = claims.get("email")
    try:
        return User(
            id=UUID(str(claims["sub"])),
            tenant_id=UUID(str(tenant_id)),
            email=email,
            full_name=claims.get("full_name") or metadata.get("full_name") or email,
            role=role,
            status=claims.get("status", "active"),
        )
    except (KeyError, ValueError, TypeError) as exc:
        raise ApiError(
            401,
            "AUTH_CLAIM_INVALID",
            "Klaim token tidak lengkap",
            "Token tidak memuat identitas yang dibutuhkan.",
        ) from exc


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    settings: Settings = Depends(get_settings),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise ApiError(
            401,
            "AUTH_TOKEN_MISSING",
            "Token tidak ada",
            "Permintaan membutuhkan Bearer token.",
        )
    return user_from_claims(decode_access_token(credentials.credentials, settings))


def require_role(*roles: Role):
    def guard(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise ApiError(
                403,
                "AUTH_ROLE_REQUIRED",
                "Peran tidak berwenang",
                "Peran akun ini tidak memiliki akses ke sumber daya tersebut.",
            )
        return user

    return guard


def get_umkm_user(
    user: User = Depends(require_role("umkm")),
    session: Session = Depends(get_db),
) -> User:
    ensure_identity(session, user)
    return user
