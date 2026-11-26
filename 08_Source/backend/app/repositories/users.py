from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import Tenant, User
from app.schemas.auth import User as AuthUser


def ensure_identity(session: Session, user: AuthUser) -> None:
    """Pastikan tenant dan user lokal ada di database sebelum query data."""
    session.execute(
        insert(Tenant)
        .values(
            id=user.tenant_id,
            name=f"Ruang kerja {user.full_name}",
            slug=f"local-{user.tenant_id}",
            type="partner",
            status="active",
        )
        .on_conflict_do_nothing(index_elements=[Tenant.id])
    )
    session.execute(
        insert(User)
        .values(
            id=user.id,
            tenant_id=user.tenant_id,
            email=str(user.email),
            full_name=user.full_name,
            phone=user.phone,
            role=user.role,
            status="active",
        )
        .on_conflict_do_update(
            index_elements=[User.id],
            set_={
                "tenant_id": user.tenant_id,
                "email": str(user.email),
                "full_name": user.full_name,
                "role": user.role,
            },
        )
    )
    session.commit()
