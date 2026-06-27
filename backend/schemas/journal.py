from __future__ import annotations

from pydantic import BaseModel, Field


class JournalAnalysisRequest(BaseModel):
    entry: str = Field(min_length=1, max_length=5000)


class JournalAnalysisResponse(BaseModel):
    status: str
    emotional_tone: str
    stress_level: str
    note: str

