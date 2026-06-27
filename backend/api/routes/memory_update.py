from __future__ import annotations

from fastapi import APIRouter

from backend.schemas.memory import MemoryUpdateRequest, MemoryUpdateResponse
from backend.utils.validators import clean_text

router = APIRouter(tags=["memory-update"])


@router.post("/memory-update", response_model=MemoryUpdateResponse)
def memory_update(payload: MemoryUpdateRequest) -> MemoryUpdateResponse:
    event_key = clean_text(payload.event_type).lower().replace(" ", "_")
    return MemoryUpdateResponse(
        status="accepted",
        memory_key=f"{event_key}_memory",
        note="Memory update accepted by placeholder architecture.",
    )

