from app.schemas.profile import ProfileRequest

DEMOGRAPHIC_FIELDS = (
    "business_name",
    "owner_name",
    "gender",
    "age",
    "whatsapp",
    "email",
    "address",
    "sector",
    "established_year",
    "operation_months",
)


def completeness_pct(payload: ProfileRequest) -> float:
    filled = sum(
        1 for field in DEMOGRAPHIC_FIELDS if getattr(payload, field) not in (None, "")
    )
    return round(filled / len(DEMOGRAPHIC_FIELDS) * 100, 2)


def is_ready_for_assessment(profile) -> bool:
    required = (
        profile.business_name,
        profile.owner_name,
        profile.sector,
        profile.established_year,
        profile.operation_months,
    )
    return all(value is not None and value != "" for value in required)
