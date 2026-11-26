from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Milestone, ProgressLog, Roadmap
from app.services.recommendation import MilestonePlan


def get_active_roadmap(session: Session, assessment_id: UUID) -> Roadmap | None:
    return session.scalar(
        select(Roadmap)
        .where(
            Roadmap.assessment_id == assessment_id,
            Roadmap.status.in_(("active", "draft")),
        )
        .order_by(Roadmap.version.desc())
        .limit(1)
    )


def create_roadmap(
    session: Session,
    tenant_id: UUID,
    assessment_id: UUID,
    title: str,
    summary: str,
    plans: list[MilestonePlan],
) -> Roadmap:
    roadmap = Roadmap(
        id=uuid4(),
        tenant_id=tenant_id,
        assessment_id=assessment_id,
        version=1,
        status="active",
        title=title,
        summary=summary,
        generated_by="rule",
    )
    session.add(roadmap)
    for plan in plans:
        session.add(
            Milestone(
                id=uuid4(),
                roadmap_id=roadmap.id,
                order_no=plan.order_no,
                title=plan.title,
                description=plan.description,
                action_items=plan.action_items,
                due_date=plan.due_date,
                status="pending",
            )
        )
    session.commit()
    session.refresh(roadmap)
    return roadmap


def list_milestones(session: Session, roadmap_id: UUID) -> list[Milestone]:
    return list(
        session.scalars(
            select(Milestone)
            .where(Milestone.roadmap_id == roadmap_id)
            .order_by(Milestone.order_no)
        ).all()
    )


def get_milestone_for_tenant(
    session: Session, milestone_id: UUID, tenant_id: UUID
) -> tuple[Milestone, Roadmap] | None:
    row = session.execute(
        select(Milestone, Roadmap)
        .join(Roadmap, Roadmap.id == Milestone.roadmap_id)
        .where(Milestone.id == milestone_id, Roadmap.tenant_id == tenant_id)
    ).first()
    if row is None:
        return None
    return row[0], row[1]


def update_milestone(
    session: Session,
    milestone: Milestone,
    status: str,
    user_id: UUID,
    tenant_id: UUID,
    note: str | None,
) -> Milestone:
    milestone.status = status
    milestone.completed_at = datetime.now(UTC) if status == "done" else None
    progress_pct = 100 if status == "done" else 0
    session.add(
        ProgressLog(
            tenant_id=tenant_id,
            milestone_id=milestone.id,
            user_id=user_id,
            progress_pct=progress_pct,
            note=note,
        )
    )
    session.commit()
    session.refresh(milestone)
    return milestone
