from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

Gender = Literal["male", "female", "undisclosed"]
Sector = Literal[
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
]

WHATSAPP_PATTERN = r"^(\+62|62|0)[0-9]{8,14}$"


class ProfileRequest(BaseModel):
    business_name: str = Field(min_length=1, max_length=160)
    owner_name: str = Field(min_length=1, max_length=120)
    gender: Gender | None = None
    age: int | None = Field(default=None, ge=15, le=100)
    whatsapp: str | None = Field(default=None, pattern=WHATSAPP_PATTERN)
    email: EmailStr | None = None
    address: str | None = Field(default=None, max_length=500)
    sector: Sector
    established_year: int = Field(ge=1900, le=2100)
    operation_months: int = Field(ge=0, le=1200)
    business_description: str | None = Field(default=None, max_length=1000)


class ProfileOut(BaseModel):
    id: UUID
    user_id: UUID
    tenant_id: UUID
    business_name: str
    owner_name: str
    gender: Gender | None
    age: int | None
    whatsapp: str | None
    email: str | None
    address: str | None
    sector: Sector
    established_year: int
    operation_months: int
    business_description: str | None
    completeness_pct: float
    created_at: datetime
    updated_at: datetime
