import pytest

from app.core.config import Settings
from app.main import validate_settings


def make_settings(**overrides) -> Settings:
    values = {
        "app_env": "development",
        "auth_mode": "local",
        "local_auth_secret": "x" * 32,
        "local_user_email": "umkm@growpath.id",
        "local_user_password": "rahasia-uji",
        "local_user_tenant_id": "11111111-1111-4111-8111-111111111111",
        "local_user_role": "umkm",
    }
    values.update(overrides)
    return Settings(**values)


def test_supabase_mode_requires_url_and_anon_key():
    with pytest.raises(RuntimeError, match="SUPABASE_URL"):
        validate_settings(make_settings(auth_mode="supabase"))


def test_local_tenant_id_must_be_uuid():
    with pytest.raises(RuntimeError, match="LOCAL_USER_TENANT_ID"):
        validate_settings(make_settings(local_user_tenant_id="bukan-uuid"))


def test_local_role_must_be_known():
    with pytest.raises(RuntimeError, match="LOCAL_USER_ROLE"):
        validate_settings(make_settings(local_user_role="raja"))


def test_production_refuses_local_mode():
    with pytest.raises(RuntimeError, match="production"):
        validate_settings(make_settings(app_env="production"))
