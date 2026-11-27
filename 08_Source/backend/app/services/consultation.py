from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.errors import ApiError
from app.models import Assessment, Consultation
from app.repositories import assessments as assessment_repo
from app.repositories import consultations as consultation_repo
from app.repositories import plans as plan_repo
from app.repositories import profiles as profile_repo
from app.schemas.auth import User
from app.services import ai

JAKARTA = ZoneInfo("Asia/Jakarta")


def _check_quota(
    session: Session, user: User, settings: Settings, now: datetime
) -> None:
    local_now = now.astimezone(JAKARTA)
    day_start = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
    reset_at = day_start + timedelta(days=1)
    daily = consultation_repo.count_since(
        session, user.id, day_start.astimezone(UTC)
    )
    if daily >= settings.ai_daily_quota:
        raise ApiError(
            429,
            "AI_QUOTA_EXCEEDED",
            "Kuota konsultasi habis",
            f"Kuota harian {settings.ai_daily_quota} pertanyaan sudah terpakai.",
            {"reset_at": reset_at.isoformat()},
        )
    burst = consultation_repo.count_since(
        session, user.id, now - timedelta(minutes=1)
    )
    if burst >= settings.ai_burst_limit:
        raise ApiError(
            429,
            "AI_RATE_LIMITED",
            "Terlalu banyak pertanyaan",
            f"Maksimal {settings.ai_burst_limit} pertanyaan per menit.",
            {"reset_at": (now + timedelta(minutes=1)).isoformat()},
        )


def _context(session: Session, assessment: Assessment) -> dict:
    profile = profile_repo.get_by_id(session, assessment.umkm_profile_id)
    segment = (
        assessment_repo.get_segment(session, assessment.segment_id)
        if assessment.segment_id is not None
        else None
    )
    dimensions = []
    sources = []
    for row, dimension in assessment_repo.get_dimension_scores(
        session, assessment.id
    ):
        dimensions.append(
            {
                "name": dimension.name,
                "score": float(row.weighted_score or 0),
            }
        )
        sources.append(
            {
                "source_id": f"dimension:{dimension.code}",
                "label": f"Skor aspek {dimension.name}",
            }
        )

    priorities = []
    roadmap = plan_repo.get_active_roadmap(session, assessment.id)
    if roadmap is not None:
        for milestone in plan_repo.list_milestones(session, roadmap.id):
            priorities.append(milestone.title)
            sources.append(
                {
                    "source_id": f"milestone:{milestone.order_no}",
                    "label": milestone.title,
                }
            )

    return {
        "business_name": profile.business_name if profile else "-",
        "sector": profile.sector if profile else "-",
        "operation_months": profile.operation_months if profile else 0,
        "total_score": float(assessment.total_score or 0),
        "segment": segment.name if segment else "-",
        "dimensions": dimensions,
        "priorities": priorities,
        "sources": sources,
    }


def _log_failure(
    session: Session,
    consultation: Consultation,
    settings: Settings,
    guardrail: dict,
    latency_ms: int | None = None,
) -> None:
    consultation_repo.add_log(
        session,
        consultation,
        model=settings.gemini_model,
        prompt_version=ai.PROMPT_VERSION,
        answer=None,
        sources=[],
        guardrail_result=guardrail,
        token_count=None,
        latency_ms=latency_ms,
        status="failed",
    )
    consultation_repo.update_status(session, consultation, "failed")


def answer(
    session: Session,
    settings: Settings,
    user: User,
    assessment_id,
    question: str,
    now: datetime | None = None,
) -> Consultation:
    now = now or datetime.now(UTC)
    assessment = assessment_repo.get_for_tenant(session, assessment_id, user.tenant_id)
    if assessment is None:
        raise ApiError(
            404,
            "ASSESSMENT_NOT_FOUND",
            "Asesmen tidak ditemukan",
            "Asesmen ini tidak ada pada akun Anda.",
        )
    if assessment.status != "scored":
        raise ApiError(
            409,
            "ASSESSMENT_NOT_SCORED",
            "Asesmen belum dinilai",
            "Kirim asesmen terlebih dahulu sebelum bertanya.",
        )

    _check_quota(session, user, settings, now)

    precheck = ai.precheck(question)
    consultation = consultation_repo.create(
        session,
        user.tenant_id,
        user.id,
        assessment.id,
        precheck.question,
    )

    if precheck.blocked:
        consultation_repo.add_log(
            session,
            consultation,
            model=settings.gemini_model,
            prompt_version=ai.PROMPT_VERSION,
            answer=precheck.message,
            sources=[],
            guardrail_result={
                **precheck.flags,
                "refusal_code": precheck.code,
                "model_called": False,
            },
            token_count=None,
            latency_ms=None,
            status="blocked",
        )
        consultation_repo.update_status(session, consultation, "completed")
        return consultation

    if not settings.gemini_api_key:
        _log_failure(
            session,
            consultation,
            settings,
            {**precheck.flags, "error": "GEMINI_API_KEY belum diisi"},
        )
        raise ApiError(
            503,
            "AI_NOT_CONFIGURED",
            "Layanan AI belum dikonfigurasi",
            "GEMINI_API_KEY belum diisi di backend.",
            {"consultation_id": str(consultation.id)},
        )

    context = _context(session, assessment)
    prompt = ai.build_prompt(context, precheck.question)
    provider = ai.GeminiProvider(
        api_key=settings.gemini_api_key,
        model=settings.gemini_model,
        base_url=settings.gemini_base_url,
        timeout_seconds=settings.ai_timeout_seconds,
    )
    try:
        result = provider.generate(prompt)
        payload = ai.parse_answer(result.raw_text)
    except ai.AIConfigError as exc:
        _log_failure(session, consultation, settings, {**precheck.flags, "error": str(exc)})
        raise ApiError(
            503,
            "AI_NOT_CONFIGURED",
            "Layanan AI belum dikonfigurasi",
            str(exc),
            {"consultation_id": str(consultation.id)},
        ) from exc
    except ai.AIProviderError as exc:
        _log_failure(session, consultation, settings, {**precheck.flags, "error": str(exc)})
        raise ApiError(
            502,
            "AI_PROVIDER_ERROR",
            "Model gagal menjawab",
            "Pertanyaan tersimpan. Coba lagi beberapa saat lagi.",
            {"consultation_id": str(consultation.id)},
        ) from exc

    checked = ai.postcheck(payload, context["sources"], settings.ai_max_answer_words)
    guardrail = {
        **precheck.flags,
        **checked.guardrail,
        "prompt_injection_suspected": precheck.flags.get(
            "prompt_injection_suspected", False
        )
        or checked.guardrail.get("prompt_injection_suspected", False),
        "model_called": True,
        "steps": checked.steps,
    }
    consultation_repo.add_log(
        session,
        consultation,
        model=settings.gemini_model,
        prompt_version=ai.PROMPT_VERSION,
        answer=checked.answer,
        sources=checked.sources,
        guardrail_result=guardrail,
        token_count=result.token_count,
        latency_ms=result.latency_ms,
        status=checked.status,
    )
    consultation_repo.update_status(session, consultation, "completed")
    return consultation
