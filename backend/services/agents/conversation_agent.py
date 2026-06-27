from __future__ import annotations

from backend.schemas.checkin import ConversationResponse, EmotionalAnalysis, SafetyAssessment


class ConversationAgent:
    def process(
        self,
        response: ConversationResponse,
        safety_assessment: SafetyAssessment,
        emotional_analysis: EmotionalAnalysis,
    ) -> ConversationResponse:
        if safety_assessment.safe_support_mode:
            return response

        if emotional_analysis.confidence_signal == "recovering":
            return response.model_copy(
                update={
                    "headline": "There is still some steadiness here.",
                }
            )
        return response

