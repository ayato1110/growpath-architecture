from uuid import uuid4

import pytest

from app.core.errors import ApiError
from app.dependencies import require_role
from app.schemas.auth import ROLES, User


def make_user(role: str) -> User:
    return User(
        id=uuid4(),
        tenant_id=uuid4(),
        email="umkm@growpath.id",
        full_name="Sari UMKM",
        role=role,
    )


@pytest.mark.parametrize("role", ROLES)
def test_require_role_allows_same_role(role):
    guard = require_role(role)
    user = make_user(role)

    assert guard(user) is user


@pytest.mark.parametrize("allowed_role", ROLES)
@pytest.mark.parametrize("actual_role", ROLES)
def test_require_role_blocks_other_roles(allowed_role, actual_role):
    if allowed_role == actual_role:
        pytest.skip("same role covered by test_require_role_allows_same_role")

    guard = require_role(allowed_role)

    with pytest.raises(ApiError) as caught:
        guard(make_user(actual_role))

    assert caught.value.status == 403
    assert caught.value.code == "AUTH_ROLE_REQUIRED"
