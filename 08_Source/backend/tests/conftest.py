import json
import os
import sys
from pathlib import Path

import pytest

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

TEST_PASSWORD = "rahasia-uji-123"
TEST_TENANT_ID = "11111111-1111-4111-8111-111111111111"

LOCAL_ACCOUNTS = [
    {
        "email": "umkm@growpath.id",
        "password": TEST_PASSWORD,
        "role": "umkm",
        "tenant_id": TEST_TENANT_ID,
        "full_name": "Sari UMKM",
    },
    {
        "email": "pendamping@growpath.id",
        "password": "rahasia-pendamping",
        "role": "pendamping",
        "tenant_id": TEST_TENANT_ID,
        "full_name": "Dewi Pendamping",
    },
    {
        "email": "mentor@growpath.id",
        "password": "rahasia-mentor",
        "role": "mentor",
        "tenant_id": TEST_TENANT_ID,
        "full_name": "Budi Mentor",
    },
    {
        "email": "admin.b2g@growpath.id",
        "password": "rahasia-b2g",
        "role": "admin_b2g",
        "tenant_id": TEST_TENANT_ID,
        "full_name": "Rani Admin B2G",
    },
    {
        "email": "admin.platform@growpath.id",
        "password": "rahasia-platform",
        "role": "admin_platform",
        "tenant_id": TEST_TENANT_ID,
        "full_name": "Tegar Admin Platform",
    },
]

os.environ.update(
    {
        "APP_ENV": "development",
        "AUTH_MODE": "local",
        "LOCAL_AUTH_SECRET": "local-secret-for-tests-only-32bytes",
        "LOCAL_USERS": json.dumps(LOCAL_ACCOUNTS),
    }
)

from fastapi.testclient import TestClient

from app.main import create_app

TEST_EMAIL = LOCAL_ACCOUNTS[0]["email"]


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(create_app())
