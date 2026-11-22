from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import Settings, get_settings
from app.core.errors import ApiError
from app.core.security import decode_access_token
from app.schemas.auth import Role, User

bearer_scheme = HTTPBearer(auto_error=False)


def user_from_claims(claims: dict) -> User:
    try:
        return User(
            id=UUID(str(claims["sub"])),
            tenant_id=UUID(str(claims["tenant_id"])),
            email=claims["email"],
            full_name=claims.get("full_name") or claims["email"],
            role=claims["role"],
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
