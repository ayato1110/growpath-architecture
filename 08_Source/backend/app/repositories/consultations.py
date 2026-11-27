from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import AIAnswerLog, Consultation


def count_since(session: Session, user_id: UUID, since: datetime) -> int:
    return int(
        session.scalar(
            select(func.count())
            .select_from(Consultation)
            .where(
                Consultation.user_id == user_id,
                Consultation.created_at >= since,
            )
        )
        or 0
    )


def create(
    session: Session,
    tenant_id: UUID,
    user_id: UUID,
    assessment_id: UUID,
    question: str,
) -> Consultation:
    consultation = Consultation(
        id=uuid4(),
        tenant_id=tenant_id,
        user_id=user_id,
        assessment_id=assessment_id,
        question=question,
        status="processing",
    )
    session.add(consultation)
    session.commit()
    session.refresh(consultation)
    return consultation


def add_log(
    session: Session,
    consultation: Consultation,
    model: str,
    prompt_version: str,
    answer: str | None,
    sources: list[dict],
    guardrail_result: dict,
    token_count: int | None,
    latency_ms: int | None,
    status: str,
) -> AIAnswerLog:
    log = AIAnswerLog(
        id=uuid4(),
        consultation_id=consultation.id,
        model=model,
        prompt_version=prompt_version,
        answer=answer,
        sources=sources,
        guardrail_result=guardrail_result,
        token_count=token_count,
        latency_ms=latency_ms,
        status=status,
    )
    session.add(log)
    session.commit()
    session.refresh(log)
    return log


def update_status(
    session: Session, consultation: Consultation, status: str
) -> None:
    consultation.status = status
    session.commit()
    session.refresh(consultation)


def get_for_tenant(
    session: Session, consultation_id: UUID, tenant_id: UUID
) -> Consultation | None:
    return session.scalar(
        select(Consultation).where(
            Consultation.id == consultation_id,
            Consultation.tenant_id == tenant_id,
        )
    )


def latest_log(session: Session, consultation_id: UUID) -> AIAnswerLog | None:
    return session.scalar(
        select(AIAnswerLog)
        .where(AIAnswerLog.consultation_id == consultation_id)
        .order_by(AIAnswerLog.created_at.desc())
        .limit(1)
    )


def list_for_user(
    session: Session,
    tenant_id: UUID,
    user_id: UUID,
    from_at: datetime | None,
    to_at: datetime | None,
    page: int,
    limit: int,
) -> tuple[list[Consultation], int]:
    conditions = [
        Consultation.tenant_id == tenant_id,
        Consultation.user_id == user_id,
    ]
    if from_at is not None:
        conditions.append(Consultation.created_at >= from_at)
    if to_at is not None:
        conditions.append(Consultation.created_at <= to_at)

    total = int(
        session.scalar(
            select(func.count()).select_from(Consultation).where(*conditions)
        )
        or 0
    )
    rows = list(
        session.scalars(
            select(Consultation)
            .where(*conditions)
            .order_by(Consultation.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        ).all()
    )
    return rows, total


def set_feedback(
    session: Session, log: AIAnswerLog, value: str, at: datetime
) -> None:
    log.feedback = value
    log.feedback_at = at
    session.commit()
    session.refresh(log)
