from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.errors import ApiError
from app.dependencies import get_umkm_user
from app.repositories import assessments as assessment_repo
from app.repositories import profiles as profile_repo
from app.schemas.assessment import (
    AnswersRequest,
    AssessmentCreateRequest,
    AssessmentDetail,
    AssessmentDraft,
    AssessmentListOut,
    ScoreResult,
)
from app.schemas.auth import User
from app.services.assessment import build_result, submit_assessment
from app.services.presenters import (
    answer_out,
    assessment_out,
    criterion_out,
    dimension_score_out,
    segment_out,
)
from app.services.profile import is_ready_for_assessment
from app.services.scoring import ScoringError, score_answer

router = APIRouter(tags=["assessment"])


def _draft(session: Session, assessment) -> AssessmentDraft:
    rows = assessment_repo.list_criteria(session)
    answers = assessment_repo.get_answers(session, assessment.id)
    return AssessmentDraft(
        assessment=assessment_out(assessment),
        criteria=[criterion_out(criterion, dimension) for criterion, dimension in rows],
        answers=[answer_out(row) for row in answers.values()],
    )


def _owned_assessment(session: Session, assessment_id, tenant_id):
    assessment = assessment_repo.get_for_tenant(session, assessment_id, tenant_id)
    if assessment is None:
        raise ApiError(
            404,
            "ASSESSMENT_NOT_FOUND",
            "Asesmen tidak ditemukan",
            "Asesmen ini tidak ada pada akun Anda.",
        )
    return assessment


@router.get("/assessments", response_model=AssessmentListOut)
def list_assessments(
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> AssessmentListOut:
    profile = profile_repo.get_by_user(session, user.tenant_id, user.id)
    if profile is None:
        return AssessmentListOut(items=[])
    rows = assessment_repo.list_for_profile(session, profile.id)
    return AssessmentListOut(items=[assessment_out(row) for row in rows])


@router.post("/assessments", response_model=AssessmentDraft, status_code=201)
def create_assessment(
    payload: AssessmentCreateRequest,
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> AssessmentDraft:
    profile = profile_repo.get_by_user(session, user.tenant_id, user.id)
    if profile is None:
        raise ApiError(
            404,
            "PROFILE_NOT_FOUND",
            "Data usaha belum diisi",
            "Lengkapi data usaha sebelum memulai asesmen.",
        )
    if payload.profile_id is not None and payload.profile_id != profile.id:
        raise ApiError(
            403,
            "PROFILE_FORBIDDEN",
            "Data usaha bukan milik akun ini",
            "Asesmen hanya dapat dibuat untuk data usaha Anda sendiri.",
        )
    if not is_ready_for_assessment(profile):
        raise ApiError(
            409,
            "PROFILE_INCOMPLETE",
            "Data usaha belum lengkap",
            "Isi nama usaha, nama pemilik, sektor, tahun berdiri, dan lama usaha.",
        )
    draft = assessment_repo.get_open_draft(session, profile.id)
    if draft is None:
        draft = assessment_repo.create_draft(session, user.tenant_id, profile.id)
    return _draft(session, draft)


@router.get("/assessments/{assessment_id}", response_model=AssessmentDetail)
def read_assessment(
    assessment_id: UUID,
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> AssessmentDetail:
    assessment = _owned_assessment(session, assessment_id, user.tenant_id)
    answers = assessment_repo.get_answers(session, assessment.id)
    scores = assessment_repo.get_dimension_scores(session, assessment.id)
    segment = (
        assessment_repo.get_segment(session, assessment.segment_id)
        if assessment.segment_id is not None
        else None
    )
    criteria_rows = assessment_repo.list_criteria(session)
    return AssessmentDetail(
        assessment=assessment_out(assessment),
        criteria=[
            criterion_out(criterion, dimension)
            for criterion, dimension in criteria_rows
        ],
        answers=[answer_out(row) for row in answers.values()],
        scores=[dimension_score_out(row, dimension) for row, dimension in scores],
        segment=segment_out(segment) if segment is not None else None,
    )


@router.put("/assessments/{assessment_id}/answers", response_model=AssessmentDraft)
def save_answers(
    assessment_id: UUID,
    payload: AnswersRequest,
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> AssessmentDraft:
    assessment = _owned_assessment(session, assessment_id, user.tenant_id)
    if assessment.status != "draft":
        raise ApiError(
            409,
            "ASSESSMENT_LOCKED",
            "Asesmen sudah dikirim",
            "Jawaban tidak dapat diubah setelah asesmen dinilai.",
        )
    rows = {criterion.id: (criterion, dimension) for criterion, dimension in assessment_repo.list_criteria(session)}
    scored = []
    for item in payload.answers:
        pair = rows.get(item.criterion_id)
        if pair is None:
            raise ApiError(
                422,
                "CRITERION_NOT_ASSESSED",
                "Kriteria tidak termasuk asesmen ini",
                f"Kriteria {item.criterion_id} tidak termasuk aspek P14.",
            )
        criterion, _ = pair
        try:
            scored.append(
                (
                    criterion.id,
                    score_answer(
                        criterion.input_type, criterion.scoring_rule, item.raw_value
                    ),
                )
            )
        except ScoringError as exc:
            raise ApiError(
                422,
                "ANSWER_INVALID",
                "Jawaban tidak valid",
                f"{criterion.code}: {exc}",
            ) from exc
    assessment_repo.upsert_answers(session, assessment.id, scored)
    session.refresh(assessment)
    return _draft(session, assessment)


@router.post("/assessments/{assessment_id}/submit", response_model=ScoreResult)
def submit(
    assessment_id: UUID,
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> ScoreResult:
    assessment = _owned_assessment(session, assessment_id, user.tenant_id)
    if assessment.status == "archived":
        raise ApiError(
            409,
            "ASSESSMENT_ARCHIVED",
            "Asesmen diarsipkan",
            "Asesmen ini tidak dapat dikirim lagi.",
        )
    criteria_rows = assessment_repo.list_criteria(session)
    answers = assessment_repo.get_answers(session, assessment.id)
    return submit_assessment(session, assessment, criteria_rows, answers)


@router.get("/assessments/{assessment_id}/scores", response_model=ScoreResult)
def read_scores(
    assessment_id: UUID,
    user: User = Depends(get_umkm_user),
    session: Session = Depends(get_db),
) -> ScoreResult:
    assessment = _owned_assessment(session, assessment_id, user.tenant_id)
    return build_result(session, assessment)
