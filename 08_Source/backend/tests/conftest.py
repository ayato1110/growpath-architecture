import os
import sys
from pathlib import Path

import pytest

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

TEST_EMAIL = "umkm@growpath.id"
TEST_PASSWORD = "rahasia-uji-123"
TEST_TENANT_ID = "11111111-1111-4111-8111-111111111111"

os.environ.update(
    {
        "APP_ENV": "development",
        "AUTH_MODE": "local",
        "LOCAL_AUTH_SECRET": "local-secret-for-tests-only-32bytes",
        "LOCAL_USER_EMAIL": TEST_EMAIL,
        "LOCAL_USER_PASSWORD": TEST_PASSWORD,
        "LOCAL_USER_NAME": "Sari UMKM",
        "LOCAL_USER_TENANT_ID": TEST_TENANT_ID,
        "LOCAL_USER_ROLE": "umkm",
    }
)

from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(create_app())
