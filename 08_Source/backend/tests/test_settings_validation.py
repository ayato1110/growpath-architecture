import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.main import validate_settings

TENANT = "11111111-1111-4111-8111-111111111111"


def make_settings(**overrides) -> Settings:
    values = {
        "app_env": "development",
        "auth_mode": "local",
        "local_auth_secret": "x" * 32,
        "local_users": [
            {
                "email": "umkm@growpath.id",
                "password": "rahasia-uji",
                "role": "umkm",
                "tenant_id": TENANT,
                "full_name": "Sari UMKM",
            }
        ],
    }
    values.update(overrides)
    return Settings(**values)


def test_local_users_tidak_boleh_kosong():
    with pytest.raises(RuntimeError, match="LOCAL_USERS"):
        validate_settings(make_settings(local_users=[]))


def test_email_ganda_ditolak():
    user = {
        "email": "umkm@growpath.id",
        "password": "rahasia-uji",
        "role": "umkm",
        "tenant_id": TENANT,
        "full_name": "Sari UMKM",
    }

    with pytest.raises(RuntimeError, match="ganda"):
        validate_settings(make_settings(local_users=[user, user]))


def test_secret_lokal_minimal_32_karakter():
    with pytest.raises(RuntimeError, match="32 karakter"):
        validate_settings(make_settings(local_auth_secret="pendek"))


def test_role_tidak_dikenal_ditolak_pydantic():
    with pytest.raises(ValidationError):
        make_settings(
            local_users=[
                {
                    "email": "raja@growpath.id",
                    "password": "rahasia-uji",
                    "role": "raja",
                    "tenant_id": TENANT,
                    "full_name": "Raja",
                }
            ]
        )


def test_supabase_mode_requires_url_and_anon_key():
    with pytest.raises(RuntimeError, match="SUPABASE_URL"):
        validate_settings(make_settings(auth_mode="supabase"))


def test_production_refuses_local_mode():
    with pytest.raises(RuntimeError, match="production"):
        validate_settings(make_settings(app_env="production"))
