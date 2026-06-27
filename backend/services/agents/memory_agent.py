from __future__ import annotations

from backend.schemas.checkin import (
    EmotionalAnalysis,
    LongitudinalPattern,
    MemorySnapshot,
    MemoryUpdates,
    MilestoneEvent,
)
from backend.services.ai.response_parser import merge_memory


class MemoryAgent:
    def update(
        self,
        current_memory: MemorySnapshot,
        updates: MemoryUpdates,
        milestones: list[MilestoneEvent],
        emotional_analysis: EmotionalAnalysis,
        patterns: list[LongitudinalPattern],
    ) -> MemorySnapshot:
        return merge_memory(current_memory, updates, milestones, emotional_analysis, patterns)

