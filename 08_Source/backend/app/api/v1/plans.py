from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.errors import ApiError
from app.dependencies import get_umkm_user
from app.repositories import assessments as assessment_repo
from app.repositories import plans as plan_repo
from app.schemas.auth import User
from app.schemas.plan import MilestoneOut, MilestoneUpdateRequest, RoadmapOut
from app.services.presenters import milestone_out

router = APIRouter(tags=["roadmap"])


@router.get("/assessments/{assessment_id}/roadmap", response_model=RoadmapOut)
def read_roadmap(
    assessment_id: UUID,
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> RoadmapOut:
    assessment = assessment_repo.get_for_tenant(
        session, assessment_id, user.tenant_id
    )
    if assessment is None:
        raise ApiError(
            404,
            "ASSESSMENT_NOT_FOUND",
            "Asesmen tidak ditemukan",
            "Asesmen ini tidak ada pada akun Anda.",
        )
    roadmap = plan_repo.get_active_roadmap(session, assessment.id)
    if roadmap is None:
        raise ApiError(
            404,
            "ROADMAP_NOT_FOUND",
            "Rencana belum tersedia",
            "Kirim asesmen terlebih dahulu untuk membuat rencana.",
        )
    return RoadmapOut(
        id=roadmap.id,
        assessment_id=roadmap.assessment_id,
        version=roadmap.version,
        status=roadmap.status,
        title=roadmap.title,
        summary=roadmap.summary,
        generated_by=roadmap.generated_by,
        generated_at=roadmap.generated_at,
        milestones=[
            milestone_out(row)
            for row in plan_repo.list_milestones(session, roadmap.id)
        ],
    )


@router.patch("/milestones/{milestone_id}", response_model=MilestoneOut)
def update_milestone(
    milestone_id: UUID,
    payload: MilestoneUpdateRequest,
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> MilestoneOut:
    pair = plan_repo.get_milestone_for_tenant(
        session, milestone_id, user.tenant_id
    )
    if pair is None:
        raise ApiError(
            404,
            "MILESTONE_NOT_FOUND",
            "Langkah tidak ditemukan",
            "Langkah ini tidak ada pada rencana Anda.",
        )
    milestone, _ = pair
    updated = plan_repo.update_milestone(
        session,
        milestone,
        payload.status,
        user.id,
        user.tenant_id,
        payload.note,
    )
    return milestone_out(updated)
