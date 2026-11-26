from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Identity,
    Numeric,
    SmallInteger,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

user_role = ENUM(
    "umkm",
    "pendamping",
    "mentor",
    "admin_b2g",
    "admin_platform",
    name="user_role",
    create_type=False,
)
user_status = ENUM(
    "active", "invited", "suspended", "deleted", name="user_status", create_type=False
)
tenant_type = ENUM(
    "platform", "institution", "partner", name="tenant_type", create_type=False
)
tenant_status = ENUM(
    "active", "suspended", "inactive", name="tenant_status", create_type=False
)
gender_value = ENUM(
    "male", "female", "undisclosed", name="gender_value", create_type=False
)
profile_sector = ENUM(
    "kuliner",
    "fashion",
    "kriya",
    "pertanian",
    "perdagangan",
    "jasa",
    "teknologi",
    "kesehatan",
    "pendidikan",
    "lainnya",
    name="profile_sector",
    create_type=False,
)
assessment_status = ENUM(
    "draft", "submitted", "scored", "archived",
    name="assessment_status",
    create_type=False,
)
input_type = ENUM(
    "boolean", "scale", "enum", "number", "text", "multi_select",
    name="input_type",
    create_type=False,
)
roadmap_status = ENUM(
    "draft", "active", "completed", "superseded",
    name="roadmap_status",
    create_type=False,
)
roadmap_generated_by = ENUM(
    "rule", "llm", "hybrid", "manual", name="roadmap_generated_by", create_type=False
)
milestone_status = ENUM(
    "pending", "in_progress", "done", "skipped",
    name="milestone_status",
    create_type=False,
)


class Base(DeclarativeBase):
    pass


class Tenant(Base):
    __tablename__ = "tenant"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    slug: Mapped[str] = mapped_column(String(80))
    type: Mapped[str] = mapped_column(tenant_type, default="partner")
    status: Mapped[str] = mapped_column(tenant_status, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenant.id", ondelete="CASCADE"))
    email: Mapped[str] = mapped_column(String(320))
    full_name: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str | None] = mapped_column(String(20))
    role: Mapped[str] = mapped_column(user_role, default="umkm")
    status: Mapped[str] = mapped_column(user_status, default="active")
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UmkmProfile(Base):
    __tablename__ = "umkm_profile"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenant.id", ondelete="CASCADE"))
    business_name: Mapped[str] = mapped_column(String(160))
    owner_name: Mapped[str] = mapped_column(String(120))
    gender: Mapped[str | None] = mapped_column(gender_value)
    age: Mapped[int | None] = mapped_column(SmallInteger)
    whatsapp: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(320))
    address: Mapped[str | None] = mapped_column(Text)
    sector: Mapped[str] = mapped_column(profile_sector)
    established_year: Mapped[int] = mapped_column(SmallInteger)
    operation_months: Mapped[int] = mapped_column(SmallInteger)
    business_description: Mapped[str | None] = mapped_column(Text)
    completeness_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Dimension(Base):
    __tablename__ = "dimension"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    code: Mapped[str] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(80))
    weight: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    is_scored: Mapped[bool] = mapped_column(Boolean, default=True)
    order_no: Mapped[int] = mapped_column(SmallInteger)


class Criterion(Base):
    __tablename__ = "criterion"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    dimension_id: Mapped[int] = mapped_column(ForeignKey("dimension.id"))
    code: Mapped[str] = mapped_column(String(16))
    question: Mapped[str] = mapped_column(Text)
    input_type: Mapped[str] = mapped_column(input_type)
    weight: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=1)
    scoring_rule: Mapped[dict] = mapped_column(JSONB)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    version: Mapped[str] = mapped_column(String(16), default="1.0")
    order_no: Mapped[int] = mapped_column(SmallInteger)


class Segment(Base):
    __tablename__ = "segment"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    code: Mapped[str] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(80))
    min_score: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    max_score: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    order_no: Mapped[int] = mapped_column(SmallInteger)


class Assessment(Base):
    __tablename__ = "assessment"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenant.id", ondelete="CASCADE"))
    umkm_profile_id: Mapped[UUID] = mapped_column(ForeignKey("umkm_profile.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(assessment_status, default="draft")
    scoring_version: Mapped[str] = mapped_column(String(16), default="2026.11-v1")
    total_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    segment_id: Mapped[int | None] = mapped_column(ForeignKey("segment.id"))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    scored_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AssessmentAnswer(Base):
    __tablename__ = "assessment_answer"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    assessment_id: Mapped[UUID] = mapped_column(ForeignKey("assessment.id", ondelete="CASCADE"))
    criterion_id: Mapped[int] = mapped_column(ForeignKey("criterion.id"))
    raw_value: Mapped[dict] = mapped_column(JSONB)
    numeric_value: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class DimensionScore(Base):
    __tablename__ = "dimension_score"

    assessment_id: Mapped[UUID] = mapped_column(ForeignKey("assessment.id", ondelete="CASCADE"), primary_key=True)
    dimension_id: Mapped[int] = mapped_column(ForeignKey("dimension.id"), primary_key=True)
    raw_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    weighted_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    is_scored: Mapped[bool] = mapped_column(Boolean, default=True)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Roadmap(Base):
    __tablename__ = "roadmap"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenant.id", ondelete="CASCADE"))
    assessment_id: Mapped[UUID] = mapped_column(ForeignKey("assessment.id", ondelete="CASCADE"))
    version: Mapped[int] = mapped_column(SmallInteger, default=1)
    status: Mapped[str] = mapped_column(roadmap_status, default="draft")
    title: Mapped[str] = mapped_column(String(160))
    summary: Mapped[str | None] = mapped_column(Text)
    generated_by: Mapped[str] = mapped_column(roadmap_generated_by, default="rule")
    model_name: Mapped[str | None] = mapped_column(String(80))
    prompt_version: Mapped[str | None] = mapped_column(String(32))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Milestone(Base):
    __tablename__ = "milestone"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    roadmap_id: Mapped[UUID] = mapped_column(ForeignKey("roadmap.id", ondelete="CASCADE"))
    order_no: Mapped[int] = mapped_column(SmallInteger)
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str | None] = mapped_column(Text)
    action_items: Mapped[list | None] = mapped_column(JSONB)
    due_date: Mapped[date | None] = mapped_column(Date)
    estimated_cost: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    status: Mapped[str] = mapped_column(milestone_status, default="pending")
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ProgressLog(Base):
    __tablename__ = "progress_log"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenant.id", ondelete="CASCADE"))
    milestone_id: Mapped[UUID] = mapped_column(ForeignKey("milestone.id", ondelete="CASCADE"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    progress_pct: Mapped[int] = mapped_column(SmallInteger)
    note: Mapped[str | None] = mapped_column(Text)
    evidence_url: Mapped[str | None] = mapped_column(Text)
    logged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
