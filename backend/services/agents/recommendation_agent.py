from __future__ import annotations

from backend.schemas.checkin import EmotionalAnalysis, Recommendations, SafetyAssessment


class RecommendationAgent:
    def process(
        self,
        recommendations: Recommendations,
        safety_assessment: SafetyAssessment,
        emotional_analysis: EmotionalAnalysis,
    ) -> Recommendations:
        if safety_assessment.safe_support_mode:
            return recommendations

        daily_actions = recommendations.daily_actions[:]
        if emotional_analysis.burnout_risk in {"high", "critical"} and len(daily_actions) < 4:
            daily_actions.append("Cap the next study block and schedule recovery before the following one.")

        return recommendations.model_copy(update={"daily_actions": daily_actions[:4]})

