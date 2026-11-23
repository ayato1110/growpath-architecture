from conftest import TEST_EMAIL, TEST_PASSWORD, TEST_TENANT_ID


def test_login_returns_umkm_session(client):
    response = client.post(
        "/auth/login", json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "Bearer"
    assert body["access_token"]
    assert body["expires_in"] > 0
    user = body["user"]
    assert user["email"] == TEST_EMAIL
    assert user["role"] == "umkm"
    assert user["tenant_id"] == TEST_TENANT_ID
    assert user["status"] == "active"


def test_login_with_wrong_password_is_401_without_account_leak(client):
    response = client.post(
        "/auth/login", json={"email": TEST_EMAIL, "password": "kata-sandi-salah"}
    )

    assert response.status_code == 401
    detail = response.json()["detail"].lower()
    assert "terdaftar" not in detail
    assert "tidak ditemukan" not in detail


def test_me_without_token_returns_problem_401(client):
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.headers["content-type"].startswith("application/problem+json")
    body = response.json()
    assert body["status"] == 401
    assert body["code"]


def test_me_with_umkm_token_returns_identity(client):
    token = client.post(
        "/auth/login", json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
    ).json()["access_token"]

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    body = response.json()
    assert body["role"] == "umkm"
    assert body["tenant_id"] == TEST_TENANT_ID
    assert body["email"] == TEST_EMAIL
    assert body["id"]
