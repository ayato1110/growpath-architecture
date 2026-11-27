from app.models import (
    AIAnswerLog,
    Assessment,
    AssessmentAnswer,
    Consultation,
    Criterion,
    Dimension,
    DimensionScore,
    Milestone,
    Segment,
)
from app.schemas.assessment import (
    AnswerOut,
    AssessmentOut,
    CriterionOption,
    CriterionOut,
    DimensionScoreOut,
    SegmentOut,
)
from app.schemas.consultation import ConsultationAnswerOut, ConsultationOut
from app.schemas.plan import MilestoneOut


def assessment_out(row: Assessment) -> AssessmentOut:
    return AssessmentOut(
        id=row.id,
        tenant_id=row.tenant_id,
        umkm_profile_id=row.umkm_profile_id,
        status=row.status,
        scoring_version=row.scoring_version,
        total_score=float(row.total_score) if row.total_score is not None else None,
        segment_id=row.segment_id,
        started_at=row.started_at,
        submitted_at=row.submitted_at,
        scored_at=row.scored_at,
    )


def criterion_out(criterion: Criterion, dimension: Dimension) -> CriterionOut:
    rule = criterion.scoring_rule or {}
    options = [
        CriterionOption(code=str(item["code"]), label=str(item["label"]))
        for item in rule.get("options", [])
    ]
    return CriterionOut(
        id=criterion.id,
        dimension_id=dimension.id,
        dimension_code=dimension.code,
        dimension_name=dimension.name,
        code=criterion.code,
        question=criterion.question,
        input_type=criterion.input_type,
        weight=float(criterion.weight),
        order_no=criterion.order_no,
        options=options,
        unit=rule.get("unit"),
    )


def answer_out(row: AssessmentAnswer) -> AnswerOut:
    return AnswerOut(
        criterion_id=row.criterion_id,
        raw_value=row.raw_value,
        numeric_value=float(row.numeric_value) if row.numeric_value is not None else None,
        score=float(row.score) if row.score is not None else None,
    )


def dimension_score_out(row: DimensionScore, dimension: Dimension) -> DimensionScoreOut:
    return DimensionScoreOut(
        dimension_id=dimension.id,
        dimension_code=dimension.code,
        dimension_name=dimension.name,
        raw_score=float(row.raw_score) if row.raw_score is not None else None,
        weighted_score=float(row.weighted_score or 0),
        is_scored=row.is_scored,
    )


def segment_out(row: Segment) -> SegmentOut:
    return SegmentOut(id=row.id, code=row.code, name=row.name)


def milestone_out(row: Milestone) -> MilestoneOut:
    return MilestoneOut(
        id=row.id,
        roadmap_id=row.roadmap_id,
        order_no=row.order_no,
        title=row.title,
        description=row.description,
        action_items=list(row.action_items or []),
        due_date=row.due_date,
        status=row.status,
        completed_at=row.completed_at,
    )


def consultation_out(
    row: Consultation, log: AIAnswerLog | None
) -> ConsultationOut:
    answer = None
    if log is not None and log.status != "failed":
        answer = ConsultationAnswerOut(
            id=log.id,
            answer=log.answer or "",
            sources=list(log.sources or []),
            status=log.status,
            model=log.model,
            prompt_version=log.prompt_version,
            created_at=log.created_at,
        )
    return ConsultationOut(
        id=row.id,
        assessment_id=row.assessment_id,
        question=row.question,
        status=row.status,
        answer=answer,
        feedback=log.feedback if log is not None else None,
        created_at=row.created_at,
    )
