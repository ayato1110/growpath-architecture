from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import UmkmProfile
from app.schemas.profile import ProfileRequest


def get_by_user(session: Session, tenant_id: UUID, user_id: UUID) -> UmkmProfile | None:
    return session.scalar(
        select(UmkmProfile).where(
            UmkmProfile.tenant_id == tenant_id,
            UmkmProfile.user_id == user_id,
        )
    )


def upsert(
    session: Session,
    tenant_id: UUID,
    user_id: UUID,
    payload: ProfileRequest,
    completeness_pct: float,
) -> UmkmProfile:
    profile = get_by_user(session, tenant_id, user_id)
    values = payload.model_dump()
    values["email"] = str(payload.email) if payload.email else None
    if profile is None:
        profile = UmkmProfile(
            id=uuid4(),
            tenant_id=tenant_id,
            user_id=user_id,
            **values,
        )
        session.add(profile)
    else:
        for field, value in values.items():
            setattr(profile, field, value)
    profile.completeness_pct = Decimal(str(completeness_pct))
    session.commit()
    session.refresh(profile)
    return profile
