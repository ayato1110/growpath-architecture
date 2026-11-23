from uuid import uuid4

import pytest

from app.core.errors import ApiError
from app.dependencies import require_role
from app.schemas.auth import User


def make_user(role: str) -> User:
    return User(
        id=uuid4(),
        tenant_id=uuid4(),
        email="umkm@growpath.id",
        full_name="Sari UMKM",
        phone=None,
        role=role,
        status="active",
        last_login_at=None,
    )


def test_role_dependency_allows_umkm():
    guard = require_role("umkm")
    user = make_user("umkm")

    assert guard(user) is user


def test_role_dependency_blocks_other_role():
    guard = require_role("admin_platform")

    with pytest.raises(ApiError) as caught:
        guard(make_user("umkm"))

    assert caught.value.status == 403
    assert caught.value.code == "AUTH_ROLE_REQUIRED"
