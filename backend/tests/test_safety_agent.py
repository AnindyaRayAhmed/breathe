from __future__ import annotations

from backend.schemas.checkin import ConversationResponse, Recommendations
from backend.services.agents.safety_agent import SafetyAgent


def test_safety_prescreen_triggers_safe_support_mode() -> None:
    agent = SafetyAgent()

    result = agent.pre_screen("I want to die because this exam pressure is too much.")

    assert result.crisis_detected is True
    assert result.safe_support_mode is True
    assert result.severity_level == "critical"


def test_safety_softening_rewrites_output() -> None:
    agent = SafetyAgent()
    recommendations = Recommendations(
        daily_actions=["Keep studying harder."],
        study_recovery_balance="Push one more hour.",
        mindfulness_recommendation="Ignore the feelings.",
        stress_reduction_technique="Scroll and distract yourself.",
        support_nudge="Stay here only.",
    )
    conversation = ConversationResponse(
        headline="You can fix this alone.",
        encouragement="Stay with me only.",
        grounding_note="Do not tell anyone.",
        follow_up_prompt="Why trust anyone else?",
    )

    safer_recommendations = agent.soften_recommendations(recommendations)
    safer_conversation = agent.soften_conversation(conversation)

    assert "trusted person" in safer_recommendations.support_nudge
    assert "support" in safer_conversation.encouragement.lower()
