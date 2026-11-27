from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.db import get_db
from app.core.errors import ApiError
from app.dependencies import get_umkm_user
from app.repositories import consultations as consultation_repo
from app.schemas.auth import User
from app.schemas.consultation import (
    ConsultationListOut,
    ConsultationOut,
    ConsultationRequest,
    FeedbackRequest,
)
from app.services import consultation as consultation_service
from app.services.presenters import consultation_out

router = APIRouter(tags=["consultation"])


@router.post("/consultations", response_model=ConsultationOut, status_code=201)
def create_consultation(
    payload: ConsultationRequest,
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> ConsultationOut:
    row = consultation_service.answer(
        session,
        settings,
        user,
        payload.assessment_id,
        payload.question,
    )
    return consultation_out(row, consultation_repo.latest_log(session, row.id))


@router.get("/consultations", response_model=ConsultationListOut)
def list_consultations(
    from_at: datetime | None = Query(default=None, alias="from"),
    to_at: datetime | None = Query(default=None, alias="to"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=50),
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> ConsultationListOut:
    rows, total = consultation_repo.list_for_user(
        session,
        user.tenant_id,
        user.id,
        from_at,
        to_at,
        page,
        limit,
    )
    return ConsultationListOut(
        items=[
            consultation_out(row, consultation_repo.latest_log(session, row.id))
            for row in rows
        ],
        page=page,
        limit=limit,
        total=total,
    )


@router.get("/consultations/{consultation_id}", response_model=ConsultationOut)
def read_consultation(
    consultation_id: UUID,
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> ConsultationOut:
    row = consultation_repo.get_for_tenant(session, consultation_id, user.tenant_id)
    if row is None:
        raise ApiError(
            404,
            "CONSULTATION_NOT_FOUND",
            "Konsultasi tidak ditemukan",
            "Konsultasi ini tidak ada pada akun Anda.",
        )
    return consultation_out(row, consultation_repo.latest_log(session, row.id))


@router.post(
    "/consultations/{consultation_id}/feedback",
    response_model=ConsultationOut,
)
def give_feedback(
    consultation_id: UUID,
    payload: FeedbackRequest,
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> ConsultationOut:
    row = consultation_repo.get_for_tenant(session, consultation_id, user.tenant_id)
    if row is None:
        raise ApiError(
            404,
            "CONSULTATION_NOT_FOUND",
            "Konsultasi tidak ditemukan",
            "Konsultasi ini tidak ada pada akun Anda.",
        )
    log = consultation_repo.latest_log(session, row.id)
    if log is None or log.status == "failed":
        raise ApiError(
            409,
            "CONSULTATION_NOT_ANSWERED",
            "Belum ada jawaban",
            "Umpan balik hanya untuk jawaban yang berhasil dibuat.",
        )
    consultation_repo.set_feedback(session, log, payload.value, datetime.now(UTC))
    return consultation_out(row, log)
