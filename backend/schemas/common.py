from __future__ import annotations

from pydantic import BaseModel, Field


class StatusResponse(BaseModel):
    status: str = Field(default="ok")

