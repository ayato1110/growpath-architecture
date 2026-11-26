from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

MilestoneStatus = Literal["pending", "in_progress", "done", "skipped"]


class MilestoneOut(BaseModel):
    id: UUID
    roadmap_id: UUID
    order_no: int
    title: str
    description: str | None
    action_items: list[str] = Field(default_factory=list)
    due_date: date | None
    status: MilestoneStatus
    completed_at: datetime | None


class RoadmapOut(BaseModel):
    id: UUID
    assessment_id: UUID
    version: int
    status: str
    title: str
    summary: str | None
    generated_by: str
    generated_at: datetime
    milestones: list[MilestoneOut]


class MilestoneUpdateRequest(BaseModel):
    status: MilestoneStatus
    note: str | None = Field(default=None, max_length=500)
