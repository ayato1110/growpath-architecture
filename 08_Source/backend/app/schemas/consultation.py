from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field

ConsultationStatus = Literal["pending", "processing", "completed", "failed"]
AnswerStatus = Literal["succeeded", "blocked", "failed"]
FeedbackValue = Literal["helpful", "not_helpful"]


class ConsultationRequest(BaseModel):
    assessment_id: UUID
    question: str = Field(min_length=3, max_length=1000)


class ConsultationAnswerOut(BaseModel):
    id: UUID
    answer: str
    sources: list[dict[str, Any]] = Field(default_factory=list)
    status: AnswerStatus
    model: str
    prompt_version: str
    created_at: datetime


class ConsultationOut(BaseModel):
    id: UUID
    assessment_id: UUID
    question: str
    status: ConsultationStatus
    answer: ConsultationAnswerOut | None
    feedback: FeedbackValue | None
    created_at: datetime


class ConsultationListOut(BaseModel):
    items: list[ConsultationOut]
    page: int
    limit: int
    total: int


class FeedbackRequest(BaseModel):
    value: FeedbackValue
