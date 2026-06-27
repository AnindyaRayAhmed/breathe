from __future__ import annotations

from fastapi import APIRouter

from backend.schemas.onboarding import OnboardingRequest, OnboardingResponse
from backend.schemas.checkin import MemorySnapshot
from backend.utils.validators import clean_text

router = APIRouter(tags=["onboarding"])


@router.post("/onboarding", response_model=OnboardingResponse)
def onboarding(payload: OnboardingRequest) -> OnboardingResponse:
    primary_stressor = clean_text(payload.primary_stressor_exam)
    normalized_exams = [
        exam.model_copy(update={"name": clean_text(exam.name)})
        for exam in payload.active_exams
        if clean_text(exam.name)
    ]
    return OnboardingResponse(
        status="accepted",
        welcome_message=(
            f"Breathe is ready to support your exam ecosystem, centered on {primary_stressor or 'your current priorities'}."
        ),
        memory=MemorySnapshot(
            active_exams=normalized_exams,
            primary_stressor_exam=primary_stressor,
        ),
    )
