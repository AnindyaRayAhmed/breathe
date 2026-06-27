from __future__ import annotations

import json

from fastapi.testclient import TestClient

from backend.main import app
from backend.schemas.checkin import MultiAgentAnalysis
from backend.services.orchestration.orchestrator import CheckInOrchestrator


class FakeGeminiClient:
    async def generate_structured_output(self, prompt: str, schema: dict) -> str:  # noqa: ARG002
        payload = MultiAgentAnalysis.model_validate(
            {
                "safety_assessment": {
                    "severity_level": "low",
                    "crisis_detected": False,
                    "harmful_language_detected": False,
                    "safe_support_mode": False,
                    "rationale": "No critical risk signals detected.",
                    "support_message": "Normal support is appropriate.",
                    "response_boundaries": ["No diagnosis"],
                },
                "intent_analysis": {
                    "primary_intent": "Process a stressful study day",
                    "secondary_intents": ["self-reflection"],
                    "reflection_depth": "moderate",
                    "help_seeking_signal": "The student wants grounded support.",
                    "exam_context": "This relates to exam revision pressure.",
                    "primary_exams": ["UPSC", "State PSC"],
                },
                "emotional_analysis": {
                    "primary_emotion": "anxious",
                    "secondary_emotions": ["tired"],
                    "emotional_tone": "tense but reflective",
                    "stress_level": "high",
                    "burnout_risk": "moderate",
                    "energy_state": "low",
                    "confidence_signal": "stable",
                    "stress_triggers": ["revision pressure"],
                    "summary": "Stress is elevated but the student is still reflective.",
                    "primary_exam_context": "UPSC",
                    "secondary_exam_contexts": ["State PSC"],
                },
                "memory_updates": {
                    "active_exams": [
                        {"name": "UPSC", "priority": "high", "exam_date": "2026-10-10"},
                        {"name": "State PSC", "priority": "medium", "exam_date": "2026-09-01"},
                    ],
                    "primary_stressor_exam": "UPSC",
                    "study_phase": "revision",
                    "new_stress_triggers": ["revision pressure"],
                    "new_motivation_sources": ["future stability"],
                    "new_coping_preferences": ["short walks"],
                    "recurring_patterns": ["stress rises late in the day"],
                    "emotional_trends": ["afternoon fatigue increases pressure"],
                    "memory_summary": "Revision pressure is intensifying later in the day.",
                    "exam_specific_insights": ["UPSC deadlines drive the strongest emotional spikes."],
                },
                "milestone_events": [
                    {
                        "event_type": "burnout episode",
                        "title": "Late-day overload",
                        "description": "The student is hitting a heavier wall later in the day.",
                        "severity_score": 6,
                        "confidence_score": 0.71,
                        "occurred_at": "",
                        "action_signal": "Protect energy before the last study block.",
                        "exam_name": "UPSC",
                    }
                ],
                "longitudinal_patterns": [
                    {
                        "pattern_name": "Late-day pressure build",
                        "description": "Stress seems to climb when energy fades in the evening.",
                        "direction": "worsening",
                        "confidence_score": 0.68,
                        "exam_name": "UPSC",
                    }
                ],
                "recommendations": {
                    "daily_actions": ["Shorten the final study block."],
                    "study_recovery_balance": "Reduce tonight's load and add one real pause.",
                    "mindfulness_recommendation": "Take three slower exhales before restarting.",
                    "stress_reduction_technique": "Step away from the desk for five minutes without your phone.",
                    "support_nudge": "Tell someone today felt heavier than expected.",
                    "target_exam": "UPSC",
                    "exam_specific_guidance": "Keep the current revision load narrow so UPSC pressure does not spill everywhere.",
                },
                "conversation_response": {
                    "headline": "You are allowed to downshift a little.",
                    "encouragement": "A smaller plan can still be a strong plan on a heavy day.",
                    "grounding_note": "Protect your nervous system before asking it for more output.",
                    "follow_up_prompt": "What part of tonight's plan can become lighter?",
                    "exam_reference": "UPSC",
                },
            }
        )
        return json.dumps(payload.model_dump())


def test_journal_analysis_endpoint_returns_dashboard_payload(monkeypatch) -> None:
    from backend.api.routes import journal_analysis as journal_analysis_route

    monkeypatch.setattr(
        journal_analysis_route,
        "orchestrator",
        CheckInOrchestrator(gemini_client=FakeGeminiClient()),
    )
    client = TestClient(app)

    response = client.post(
        "/api/journal-analysis",
        json={
            "journal_entry": "I am getting more stressed in the evening and my revision blocks feel messy.",
            "mood_score": 4,
            "energy_score": 3,
            "stress_score": 8,
            "memory": {
                "active_exams": [
                    {"name": "UPSC", "priority": "high", "exam_date": "2026-10-10"},
                    {"name": "State PSC", "priority": "medium", "exam_date": "2026-09-01"},
                ],
                "primary_stressor_exam": "UPSC",
                "study_phase": "unknown",
                "stress_triggers": [],
                "motivation_sources": [],
                "recurring_patterns": [],
                "coping_preferences": [],
                "milestone_history": [],
                "emotional_trends": [],
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["analysis"]["milestone_events"][0]["event_type"] == "burnout episode"
