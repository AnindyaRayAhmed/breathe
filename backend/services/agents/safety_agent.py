from __future__ import annotations

from backend.schemas.checkin import (
    ConversationResponse,
    Recommendations,
    SafetyAssessment,
)


class SafetyAgent:
    _CRISIS_KEYWORDS = {
        "suicide",
        "self-harm",
        "kill myself",
        "want to die",
        "end my life",
        "hurt myself",
        "can't go on",
    }

    def pre_screen(self, text: str) -> SafetyAssessment:
        lowered = text.lower()
        crisis_detected = any(keyword in lowered for keyword in self._CRISIS_KEYWORDS)
        severity = "critical" if crisis_detected else "moderate"

        return SafetyAssessment(
            severity_level=severity,
            crisis_detected=crisis_detected,
            harmful_language_detected=crisis_detected,
            safe_support_mode=crisis_detected,
            rationale=(
                "Local safety prescreen detected crisis language."
                if crisis_detected
                else "Local safety prescreen did not detect crisis language."
            ),
            support_message=(
                "You deserve immediate human support right now. Please contact a trusted person or local emergency support."
                if crisis_detected
                else "No immediate crisis signals were detected in the local prescreen."
            ),
            response_boundaries=[
                "No medical diagnosis",
                "No manipulative attachment language",
                "Encourage trusted human support when risk is elevated",
            ],
        )

    def enforce(self, local_result: SafetyAssessment, model_result: SafetyAssessment) -> SafetyAssessment:
        if local_result.crisis_detected:
            return local_result

        high_risk = model_result.severity_level in {"high", "critical"} or model_result.crisis_detected
        return model_result.model_copy(
            update={
                "safe_support_mode": model_result.safe_support_mode or high_risk,
                "response_boundaries": list(dict.fromkeys(model_result.response_boundaries + local_result.response_boundaries)),
            }
        )

    def soften_recommendations(self, recommendations: Recommendations) -> Recommendations:
        return recommendations.model_copy(
            update={
                "daily_actions": [
                    "Pause the study sprint and choose one grounding action first.",
                    "Drink water and step away from performance tracking for ten minutes.",
                    "Reach out to one trusted person before returning to exam work.",
                ],
                "study_recovery_balance": "Shift today's goal from pushing harder to stabilizing your nervous system first.",
                "mindfulness_recommendation": "Try a two-minute inhale-exhale count while keeping both feet on the floor.",
                "stress_reduction_technique": "Use a 5-4-3-2-1 grounding reset before making any study decision.",
                "support_nudge": "Please involve a trusted person such as a friend, family member, mentor, counselor, or local support service today.",
            }
        )

    def soften_conversation(self, response: ConversationResponse) -> ConversationResponse:
        return response.model_copy(
            update={
                "headline": "You do not need to hold this alone right now.",
                "encouragement": (
                    "What you're feeling matters, and the next best step is gentle, real-world support, not more pressure."
                ),
                "grounding_note": "Stay with the next safe action and bring another person into the loop if you can.",
                "follow_up_prompt": "Who is the safest person you can contact right now for steady support?",
            }
        )
