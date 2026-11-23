from app.dependencies import user_from_claims

TENANT = "11111111-1111-4111-8111-111111111111"


def test_supabase_role_comes_from_app_metadata_not_reserved_claim():
    claims = {
        "sub": "a6b693cc-9428-59c8-a082-92b64a218d3b",
        "email": "umkm@growpath.id",
        "role": "authenticated",
        "app_metadata": {"tenant_id": TENANT, "app_role": "umkm"},
    }

    user = user_from_claims(claims)

    assert user.role == "umkm"
    assert str(user.tenant_id) == TENANT


def test_supabase_claims_without_app_role_are_rejected():
    claims = {
        "sub": "a6b693cc-9428-59c8-a082-92b64a218d3b",
        "email": "umkm@growpath.id",
        "role": "authenticated",
        "app_metadata": {"tenant_id": TENANT},
    }

    from app.core.errors import ApiError

    try:
        user_from_claims(claims)
    except ApiError as error:
        assert error.status == 401
        assert error.code == "AUTH_CLAIM_INVALID"
    else:
        raise AssertionError("klaim tanpa app_role harus ditolak")
