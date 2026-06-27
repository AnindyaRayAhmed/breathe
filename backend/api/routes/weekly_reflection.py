from __future__ import annotations

from fastapi import APIRouter

from backend.schemas.weekly import WeeklyReflectionRequest, WeeklyReflectionResponse
from backend.services.memory.summarization import MemorySummarizationService

router = APIRouter(tags=["weekly-reflection"])
service = MemorySummarizationService()


@router.post("/weekly-reflection", response_model=WeeklyReflectionResponse)
def weekly_reflection(payload: WeeklyReflectionRequest) -> WeeklyReflectionResponse:
    insight = service.summarize(payload.week_summary)
    return WeeklyReflectionResponse(
        status="accepted",
        insight=insight,
        next_step="Continue your reflection streak with one short check-in tomorrow.",
    )

