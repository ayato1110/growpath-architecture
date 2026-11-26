import pytest
from conftest import LOCAL_ACCOUNTS, TEST_EMAIL, TEST_TENANT_ID


@pytest.mark.parametrize(
    "account",
    LOCAL_ACCOUNTS,
    ids=[account["role"] for account in LOCAL_ACCOUNTS],
)
def test_setiap_akun_lokal_masuk_dengan_rolenya(client, account):
    response = client.post(
        "/auth/login",
        json={"email": account["email"], "password": account["password"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["user"]["role"] == account["role"]
    assert body["user"]["full_name"] == account["full_name"]
    assert body["user"]["tenant_id"] == TEST_TENANT_ID

    me = client.get(
        "/auth/me", headers={"Authorization": f"Bearer {body['access_token']}"}
    )
    assert me.status_code == 200
    assert me.json()["role"] == account["role"]


def test_kata_sandi_akun_lain_ditolak(client):
    mentor = next(a for a in LOCAL_ACCOUNTS if a["role"] == "mentor")

    response = client.post(
        "/auth/login",
        json={"email": mentor["email"], "password": "rahasia-uji-123"},
    )

    assert response.status_code == 401
    assert response.json()["code"] == "AUTH_INVALID_CREDENTIALS"


def test_email_tidak_terdaftar_ditolak(client):
    response = client.post(
        "/auth/login",
        json={"email": "tidak-ada@growpath.id", "password": "apa-saja"},
    )

    assert response.status_code == 401
    assert response.json()["code"] == "AUTH_INVALID_CREDENTIALS"


def test_akun_umkm_tetap_bisa_masuk(client):
    response = client.post(
        "/auth/login",
        json={"email": TEST_EMAIL, "password": "rahasia-uji-123"},
    )

    assert response.status_code == 200
    assert response.json()["user"]["role"] == "umkm"
