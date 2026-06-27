from __future__ import annotations

import json

from backend.schemas.checkin import DailyCheckInRequest, MultiAgentAnalysis
from backend.services.orchestration.orchestrator import CheckInOrchestrator


class FakeGeminiClient:
    async def generate_structured_output(self, prompt: str, schema: dict) -> str:  # noqa: ARG002
        payload = MultiAgentAnalysis.model_validate(
            {
                "safety_assessment": {
                    "severity_level": "moderate",
                    "crisis_detected": False,
                    "harmful_language_detected": False,
                    "safe_support_mode": False,
                    "rationale": "Stress is present but not acute.",
                    "support_message": "Gentle support is appropriate.",
                    "response_boundaries": ["No diagnosis"],
                },
                "intent_analysis": {
                    "primary_intent": "Needs help processing exam stress",
                    "secondary_intents": ["self-reflection"],
                    "reflection_depth": "deep",
                    "help_seeking_signal": "The student wants support without judgment.",
                    "exam_context": "Mock test pressure is central.",
                    "primary_exams": ["JEE", "BITSAT"],
                },
                "emotional_analysis": {
                    "primary_emotion": "anxious",
                    "secondary_emotions": ["frustrated"],
                    "emotional_tone": "tense but thoughtful",
                    "stress_level": "high",
                    "burnout_risk": "moderate",
                    "energy_state": "drained",
                    "confidence_signal": "dipping",
                    "stress_triggers": ["mock test scores"],
                    "summary": "Pressure is clustering around performance signals.",
                    "primary_exam_context": "JEE",
                    "secondary_exam_contexts": ["BITSAT"],
                },
                "memory_updates": {
                    "active_exams": [
                        {"name": "JEE", "priority": "high", "exam_date": "2026-01-15"},
                        {"name": "BITSAT", "priority": "medium", "exam_date": "2026-05-20"},
                    ],
                    "primary_stressor_exam": "JEE",
                    "study_phase": "revision",
                    "new_stress_triggers": ["mock test scores"],
                    "new_motivation_sources": ["family support"],
                    "new_coping_preferences": ["walking breaks"],
                    "recurring_patterns": ["confidence dips after score review"],
                    "emotional_trends": ["stress spikes before mock tests"],
                    "memory_summary": "Mock tests are a recurring trigger right now.",
                    "exam_specific_insights": ["JEE mock tests trigger the strongest reactions."],
                },
                "milestone_events": [
                    {
                        "event_type": "mock test crash",
                        "title": "Mock test confidence dip",
                        "description": "A recent result appears to have shaken confidence.",
                        "severity_score": 7,
                        "confidence_score": 0.82,
                        "occurred_at": "",
                        "action_signal": "Recover before overcorrecting the study plan.",
                        "exam_name": "JEE",
                    }
                ],
                "longitudinal_patterns": [
                    {
                        "pattern_name": "Score-linked stress loop",
                        "description": "Stress rises sharply when mock scores are reviewed.",
                        "direction": "worsening",
                        "confidence_score": 0.75,
                        "exam_name": "JEE",
                    }
                ],
                "recommendations": {
                    "daily_actions": [
                        "Review one weak topic only.",
                        "Take a short walk after the next study block.",
                    ],
                    "study_recovery_balance": "Reduce the scope of tonight's plan and add one recovery gap.",
                    "mindfulness_recommendation": "Try a short exhale-focused breathing cycle before restarting.",
                    "stress_reduction_technique": "Pause score checking for the rest of today.",
                    "support_nudge": "Tell one trusted person that mock test stress is building up.",
                    "target_exam": "JEE",
                    "exam_specific_guidance": "Treat JEE as the active pressure source for today.",
                },
                "conversation_response": {
                    "headline": "This looks heavy, not hopeless.",
                    "encouragement": "A bad patch does not erase the work you've already done.",
                    "grounding_note": "Handle the next block, not the whole exam season.",
                    "follow_up_prompt": "Which part of today feels most emotionally expensive?",
                    "exam_reference": "JEE",
                },
            }
        )
        return json.dumps(payload.model_dump())


def test_orchestrator_returns_valid_multi_agent_response() -> None:
    orchestrator = CheckInOrchestrator(gemini_client=FakeGeminiClient())
    payload = DailyCheckInRequest(
        journal_entry="I feel tense after my mock test score and I keep comparing myself to everyone else.",
        mood_score=4,
        energy_score=4,
        stress_score=8,
        memory={
            "active_exams": [
                {"name": "JEE", "priority": "high", "exam_date": "2026-01-15"},
                {"name": "BITSAT", "priority": "medium", "exam_date": "2026-05-20"},
            ],
            "primary_stressor_exam": "JEE",
            "study_phase": "revision",
            "stress_triggers": [],
            "motivation_sources": [],
            "recurring_patterns": [],
            "coping_preferences": [],
            "milestone_history": [],
            "emotional_trends": [],
        },
    )

    response = __import__("asyncio").run(orchestrator.run_daily_check_in(payload))

    assert response.status == "completed"
    assert response.source == "ai"
    assert response.analysis.emotional_analysis.primary_emotion == "anxious"
    assert response.updated_memory.primary_stressor_exam == "JEE"
    assert response.updated_memory.active_exams[0].name == "JEE"
