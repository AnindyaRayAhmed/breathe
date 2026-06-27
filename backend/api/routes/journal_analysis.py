from __future__ import annotations

from fastapi import APIRouter

from backend.schemas.checkin import DailyCheckInRequest, DailyCheckInResponse
from backend.services.orchestration.orchestrator import CheckInOrchestrator

router = APIRouter(tags=["journal-analysis"])
orchestrator = CheckInOrchestrator()


@router.post("/journal-analysis", response_model=DailyCheckInResponse)
async def analyze_journal(payload: DailyCheckInRequest) -> DailyCheckInResponse:
    return await orchestrator.run_daily_check_in(payload)
