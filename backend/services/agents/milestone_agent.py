from __future__ import annotations

from backend.schemas.checkin import MilestoneEvent


class MilestoneAgent:
    def process(self, milestones: list[MilestoneEvent]) -> list[MilestoneEvent]:
        normalized: list[MilestoneEvent] = []
        for item in milestones:
            normalized.append(
                item.model_copy(
                    update={
                        "severity_score": max(1, min(10, item.severity_score)),
                        "confidence_score": max(0.0, min(1.0, item.confidence_score)),
                    }
                )
            )
        return normalized[:6]

