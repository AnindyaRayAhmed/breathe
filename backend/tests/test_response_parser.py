from __future__ import annotations

import json

from backend.services.ai.response_parser import parse_agent_response


def test_response_parser_validates_milestone_payload() -> None:
    payload = {
        "safety_assessment": {
            "severity_level": "low",
            "crisis_detected": False,
            "harmful_language_detected": False,
            "safe_support_mode": False,
            "rationale": "No critical risk signals detected.",
            "support_message": "Standard support is appropriate.",
            "response_boundaries": ["No diagnosis"],
        },
        "intent_analysis": {
            "primary_intent": "Reflect on exam stress",
            "secondary_intents": [],
            "reflection_depth": "moderate",
            "help_seeking_signal": "The student wants a grounded reset.",
            "exam_context": "This relates to revision pressure.",
            "primary_exams": ["NEET", "Boards"],
        },
        "emotional_analysis": {
            "primary_emotion": "tired",
            "secondary_emotions": [],
            "emotional_tone": "quietly strained",
            "stress_level": "moderate",
            "burnout_risk": "moderate",
            "energy_state": "low",
            "confidence_signal": "stable",
            "stress_triggers": ["revision load"],
            "summary": "Stress is noticeable but still reflective.",
            "primary_exam_context": "NEET",
            "secondary_exam_contexts": ["Boards"],
        },
        "memory_updates": {
            "active_exams": [
                {"name": "NEET", "priority": "high", "exam_date": "2026-05-20"},
                {"name": "Boards", "priority": "medium", "exam_date": "2026-03-10"},
            ],
            "primary_stressor_exam": "NEET",
            "study_phase": "revision",
            "new_stress_triggers": ["revision load"],
            "new_motivation_sources": [],
            "new_coping_preferences": [],
            "recurring_patterns": [],
            "emotional_trends": [],
            "memory_summary": "Revision load is currently stressful.",
            "exam_specific_insights": ["NEET revision is carrying most of the pressure."],
        },
        "milestone_events": [
            {
                "event_type": "consistency streak",
                "title": "Returned to daily reflection",
                "description": "The student came back to check-ins after a gap.",
                "severity_score": 4,
                "confidence_score": 0.61,
                "occurred_at": "",
                "action_signal": "Reinforce the habit gently.",
                "exam_name": "NEET",
            }
        ],
        "longitudinal_patterns": [],
        "recommendations": {
            "daily_actions": ["Keep the next study block light."],
            "study_recovery_balance": "Add a break before the next revision round.",
            "mindfulness_recommendation": "Take three slow breaths before restarting.",
            "stress_reduction_technique": "Do a quick body unclench from jaw to shoulders.",
            "support_nudge": "Mention the stress build-up to someone you trust.",
            "target_exam": "NEET",
            "exam_specific_guidance": "Give NEET the softer plan today and let Boards stay lighter in the background.",
        },
        "conversation_response": {
            "headline": "Today needs softness, not force.",
            "encouragement": "You can still salvage the day without turning it into punishment.",
            "grounding_note": "Small steady actions count.",
            "follow_up_prompt": "What would make the next hour feel less loaded?",
            "exam_reference": "NEET",
        },
    }

    parsed = parse_agent_response(json.dumps(payload))

    assert parsed.milestone_events[0].event_type == "consistency streak"
    assert parsed.recommendations.daily_actions[0] == "Keep the next study block light."
