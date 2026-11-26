from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import delete, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import (
    Assessment,
    AssessmentAnswer,
    Criterion,
    Dimension,
    DimensionScore,
    Segment,
)
from app.services.scoring import AnswerScore

SCORED_DIMENSION_CODES = ("PSY", "PAS")


def get_for_tenant(
    session: Session, assessment_id: UUID, tenant_id: UUID
) -> Assessment | None:
    return session.scalar(
        select(Assessment).where(
            Assessment.id == assessment_id,
            Assessment.tenant_id == tenant_id,
        )
    )


def get_open_draft(session: Session, profile_id: UUID) -> Assessment | None:
    return session.scalar(
        select(Assessment)
        .where(
            Assessment.umkm_profile_id == profile_id,
            Assessment.status == "draft",
        )
        .order_by(Assessment.created_at.desc())
        .limit(1)
    )


def list_for_profile(session: Session, profile_id: UUID) -> list[Assessment]:
    return list(
        session.scalars(
            select(Assessment)
            .where(Assessment.umkm_profile_id == profile_id)
            .order_by(Assessment.created_at.desc())
        ).all()
    )


def create_draft(session: Session, tenant_id: UUID, profile_id: UUID) -> Assessment:
    assessment = Assessment(
        id=uuid4(),
        tenant_id=tenant_id,
        umkm_profile_id=profile_id,
        status="draft",
        scoring_version="2026.11-v1",
    )
    session.add(assessment)
    session.commit()
    session.refresh(assessment)
    return assessment


def list_criteria(session: Session) -> list[tuple[Criterion, Dimension]]:
    rows = session.execute(
        select(Criterion, Dimension)
        .join(Dimension, Dimension.id == Criterion.dimension_id)
        .where(
            Dimension.code.in_(SCORED_DIMENSION_CODES),
            Dimension.is_scored.is_(True),
            Criterion.is_active.is_(True),
        )
        .order_by(Dimension.order_no, Criterion.order_no)
    ).all()
    return [(row[0], row[1]) for row in rows]


def get_answers(session: Session, assessment_id: UUID) -> dict[int, AssessmentAnswer]:
    rows = session.scalars(
        select(AssessmentAnswer).where(
            AssessmentAnswer.assessment_id == assessment_id
        )
    ).all()
    return {row.criterion_id: row for row in rows}


def upsert_answers(
    session: Session, assessment_id: UUID, answers: list[tuple[int, AnswerScore]]
) -> None:
    if not answers:
        return
    now = datetime.now(UTC)
    session.execute(
        insert(AssessmentAnswer)
        .values(
            [
                {
                    "assessment_id": assessment_id,
                    "criterion_id": criterion_id,
                    "raw_value": score.raw_value,
                    "numeric_value": score.numeric_value,
                    "score": score.score,
                    "answered_at": now,
                }
                for criterion_id, score in answers
            ]
        )
        .on_conflict_do_update(
            constraint="assessment_answer_unique",
            set_={
                "raw_value": insert.excluded.raw_value,
                "numeric_value": insert.excluded.numeric_value,
                "score": insert.excluded.score,
                "answered_at": insert.excluded.answered_at,
            },
        )
    )
    session.commit()


def count_scored_answers(session: Session, assessment_id: UUID) -> int:
    return int(
        session.scalar(
            select(func.count())
            .select_from(AssessmentAnswer)
            .where(
                AssessmentAnswer.assessment_id == assessment_id,
                AssessmentAnswer.score.is_not(None),
            )
        )
        or 0
    )


def count_active_criteria(session: Session) -> int:
    return int(
        session.scalar(
            select(func.count())
            .select_from(Criterion)
            .where(Criterion.is_active.is_(True))
        )
        or 0
    )


def list_segments(session: Session) -> list[Segment]:
    return list(session.scalars(select(Segment).order_by(Segment.order_no)).all())


def clear_scores(session: Session, assessment_id: UUID) -> None:
    session.execute(
        delete(DimensionScore).where(DimensionScore.assessment_id == assessment_id)
    )


def save_scores(
    session: Session,
    assessment: Assessment,
    dimension_scores: list[tuple[Dimension, float]],
    total_score: float,
    segment_id: int,
) -> None:
    now = datetime.now(UTC)
    for dimension, score in dimension_scores:
        session.add(
            DimensionScore(
                assessment_id=assessment.id,
                dimension_id=dimension.id,
                raw_score=Decimal(str(score)),
                weighted_score=Decimal(str(score)),
                is_scored=True,
                computed_at=now,
            )
        )
    assessment.status = "scored"
    assessment.total_score = Decimal(str(total_score))
    assessment.segment_id = segment_id
    assessment.submitted_at = assessment.submitted_at or now
    assessment.scored_at = now
    session.commit()


def get_dimension_scores(
    session: Session, assessment_id: UUID
) -> list[tuple[DimensionScore, Dimension]]:
    rows = session.execute(
        select(DimensionScore, Dimension)
        .join(Dimension, Dimension.id == DimensionScore.dimension_id)
        .where(DimensionScore.assessment_id == assessment_id)
        .order_by(Dimension.order_no)
    ).all()
    return [(row[0], row[1]) for row in rows]


def get_segment(session: Session, segment_id: int) -> Segment | None:
    return session.get(Segment, segment_id)
