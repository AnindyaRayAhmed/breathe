from __future__ import annotations

from pydantic import BaseModel, Field


class WeeklyReflectionRequest(BaseModel):
    week_summary: str = Field(min_length=1, max_length=8000)


class WeeklyReflectionResponse(BaseModel):
    status: str
    insight: str
    next_step: str

