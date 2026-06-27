from __future__ import annotations

from pydantic import BaseModel, Field


class MemoryUpdateRequest(BaseModel):
    event_type: str = Field(min_length=1, max_length=50)
    detail: str = Field(min_length=1, max_length=4000)


class MemoryUpdateResponse(BaseModel):
    status: str
    memory_key: str
    note: str

