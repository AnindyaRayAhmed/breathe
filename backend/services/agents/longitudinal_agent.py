from __future__ import annotations

from backend.schemas.checkin import LongitudinalPattern


class LongitudinalAgent:
    def process(self, patterns: list[LongitudinalPattern]) -> list[LongitudinalPattern]:
        return patterns[:5]

