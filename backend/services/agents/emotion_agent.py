from __future__ import annotations

from backend.schemas.checkin import DailyCheckInRequest, EmotionalAnalysis


class EmotionAgent:
    def process(self, analysis: EmotionalAnalysis, payload: DailyCheckInRequest) -> EmotionalAnalysis:
        stress_level = analysis.stress_level
        burnout_risk = analysis.burnout_risk

        if payload.stress_score >= 9 and stress_level in {"low", "moderate"}:
            stress_level = "high"
        if payload.energy_score <= 2 and burnout_risk == "low":
            burnout_risk = "moderate"

        return analysis.model_copy(
            update={
                "stress_level": stress_level,
                "burnout_risk": burnout_risk,
            }
        )

