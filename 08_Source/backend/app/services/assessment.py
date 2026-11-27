from datetime import date

from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models import Assessment, Criterion, Dimension
from app.repositories import assessments as assessment_repo
from app.repositories import plans as plan_repo
from app.schemas.assessment import ScoreResult
from app.services.presenters import dimension_score_out, segment_out
from app.services.recommendation import CriterionScore, build_plan, build_summary
from app.services.scoring import round_score, segment_for, weighted_average


def submit_assessment(
    session: Session,
    assessment: Assessment,
    criteria_rows: list[tuple[Criterion, Dimension]],
    answers,
) -> ScoreResult:
    if assessment.status != "scored":
        missing = [
            criterion.code
            for criterion, _ in criteria_rows
            if criterion.id not in answers or answers[criterion.id].score is None
        ]
        if missing:
            raise ApiError(
                422,
                "ASSESSMENT_INCOMPLETE",
                "Asesmen belum lengkap",
                "Kriteria berikut belum dijawab: " + ", ".join(missing),
            )

        total = round_score(
            weighted_average(
                [
                    (float(criterion.weight), float(answers[criterion.id].score))
                    for criterion, _ in criteria_rows
                ]
            )
        )
        segments = assessment_repo.list_segments(session)
        segment = segment_for(
            total,
            [
                (row.id, row.code, float(row.min_score), float(row.max_score))
                for row in segments
            ],
        )

        grouped: dict[int, tuple[Dimension, list[tuple[float, float]]]] = {}
        for criterion, dimension in criteria_rows:
            _, pairs = grouped.setdefault(dimension.id, (dimension, []))
            pairs.append(
                (float(criterion.weight), float(answers[criterion.id].score))
            )
        dimension_scores = [
            (dimension, round_score(weighted_average(pairs)))
            for dimension, pairs in grouped.values()
        ]

        assessment_repo.clear_scores(session, assessment.id)
        assessment_repo.save_scores(
            session, assessment, dimension_scores, total, segment[0]
        )

    if plan_repo.get_active_roadmap(session, assessment.id) is None:
        plans = build_plan(
            [
                CriterionScore(
                    criterion_id=criterion.id,
                    code=criterion.code,
                    question=criterion.question,
                    dimension_name=dimension.name,
                    score=float(answers[criterion.id].score),
                    order_no=criterion.order_no,
                )
                for criterion, dimension in criteria_rows
                if criterion.id in answers
            ],
            scored_on=date.today(),
        )
        plan_repo.create_roadmap(
            session,
            assessment.tenant_id,
            assessment.id,
            title="Rencana prioritas 30 hari",
            summary=build_summary(
                plans, [dimension.name for _, dimension in criteria_rows]
            ),
            plans=plans,
        )

    return build_result(session, assessment)


def build_result(session: Session, assessment: Assessment) -> ScoreResult:
    scores = assessment_repo.get_dimension_scores(session, assessment.id)
    segment = (
        assessment_repo.get_segment(session, assessment.segment_id)
        if assessment.segment_id is not None
        else None
    )
    if assessment.total_score is None or segment is None:
        raise ApiError(
            409,
            "ASSESSMENT_NOT_SCORED",
            "Asesmen belum dinilai",
            "Kirim asesmen terlebih dahulu sebelum membaca skor.",
        )
    return ScoreResult(
        assessment_id=assessment.id,
        total_score=float(assessment.total_score),
        segment=segment_out(segment),
        dimensions=[dimension_score_out(row, dimension) for row, dimension in scores],
        criteria_answered=assessment_repo.count_scored_answers(
            session, assessment.id
        ),
        criteria_total=assessment_repo.count_active_criteria(session),
    )
