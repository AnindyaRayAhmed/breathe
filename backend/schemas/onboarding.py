from __future__ import annotations

from pydantic import BaseModel, Field

from backend.schemas.checkin import ExamContext, MemorySnapshot


class OnboardingRequest(BaseModel):
    active_exams: list[ExamContext] = Field(default_factory=list, min_length=1, max_length=8)
    primary_stressor_exam: str = Field(min_length=1, max_length=80)


class OnboardingResponse(BaseModel):
    status: str
    welcome_message: str
    memory: MemorySnapshot

