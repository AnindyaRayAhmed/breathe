from __future__ import annotations

from backend.schemas.checkin import IntentAnalysis


class IntentAgent:
    def process(self, intent_analysis: IntentAnalysis) -> IntentAnalysis:
        return intent_analysis

