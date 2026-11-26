from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field

InputType = Literal["boolean", "scale", "enum", "number", "text", "multi_select"]
AssessmentStatus = Literal["draft", "submitted", "scored", "archived"]


class AssessmentCreateRequest(BaseModel):
    profile_id: UUID | None = None


class AssessmentOut(BaseModel):
    id: UUID
    tenant_id: UUID
    umkm_profile_id: UUID
    status: AssessmentStatus
    scoring_version: str
    total_score: float | None
    segment_id: int | None
    started_at: datetime
    submitted_at: datetime | None
    scored_at: datetime | None


class AnswerIn(BaseModel):
    criterion_id: int
    raw_value: dict[str, Any]


class AnswersRequest(BaseModel):
    answers: list[AnswerIn] = Field(min_length=1)


class AnswerOut(BaseModel):
    criterion_id: int
    raw_value: dict[str, Any]
    numeric_value: float | None
    score: float | None


class CriterionOption(BaseModel):
    code: str
    label: str


class CriterionOut(BaseModel):
    id: int
    dimension_id: int
    dimension_code: str
    dimension_name: str
    code: str
    question: str
    input_type: InputType
    weight: float
    order_no: int
    options: list[CriterionOption] = Field(default_factory=list)
    unit: str | None = None


class AssessmentDraft(BaseModel):
    assessment: AssessmentOut
    criteria: list[CriterionOut]
    answers: list[AnswerOut]


class AssessmentListOut(BaseModel):
    items: list[AssessmentOut]


class SegmentOut(BaseModel):
    id: int
    code: str
    name: str


class DimensionScoreOut(BaseModel):
    dimension_id: int
    dimension_code: str
    dimension_name: str
    raw_score: float | None
    weighted_score: float
    is_scored: bool


class AssessmentDetail(BaseModel):
    assessment: AssessmentOut
    criteria: list[CriterionOut]
    answers: list[AnswerOut]
    scores: list[DimensionScoreOut]
    segment: SegmentOut | None


class ScoreResult(BaseModel):
    assessment_id: UUID
    total_score: float
    segment: SegmentOut
    dimensions: list[DimensionScoreOut]
    criteria_answered: int
    criteria_total: int


class JobAccepted(BaseModel):
    job_id: UUID
    status: str = "accepted"
