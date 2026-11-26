from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.errors import ApiError
from app.dependencies import get_umkm_user
from app.models import UmkmProfile
from app.repositories import profiles as profile_repo
from app.schemas.auth import User
from app.schemas.profile import ProfileOut, ProfileRequest
from app.services.profile import completeness_pct

router = APIRouter(tags=["profile"])


def _to_out(row: UmkmProfile) -> ProfileOut:
    return ProfileOut(
        id=row.id,
        user_id=row.user_id,
        tenant_id=row.tenant_id,
        business_name=row.business_name,
        owner_name=row.owner_name,
        gender=row.gender,
        age=row.age,
        whatsapp=row.whatsapp,
        email=row.email,
        address=row.address,
        sector=row.sector,
        established_year=row.established_year,
        operation_months=row.operation_months,
        business_description=row.business_description,
        completeness_pct=float(row.completeness_pct),
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


@router.get("/me/profile", response_model=ProfileOut)
def read_profile(
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> ProfileOut:
    row = profile_repo.get_by_user(session, user.tenant_id, user.id)
    if row is None:
        raise ApiError(
            404,
            "PROFILE_NOT_FOUND",
            "Data usaha belum diisi",
            "Lengkapi data usaha sebelum memakai fitur lain.",
        )
    return _to_out(row)


@router.put("/me/profile", response_model=ProfileOut)
def replace_profile(
    payload: ProfileRequest,
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> ProfileOut:
    row = profile_repo.upsert(
        session,
        user.tenant_id,
        user.id,
        payload,
        completeness_pct(payload),
    )
    return _to_out(row)


@router.patch("/me/profile", response_model=ProfileOut)
def update_profile(
    payload: ProfileRequest,
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> ProfileOut:
    row = profile_repo.upsert(
        session,
        user.tenant_id,
        user.id,
        payload,
        completeness_pct(payload),
    )
    return _to_out(row)
