from __future__ import annotations

import json

from backend.schemas.checkin import DailyCheckInRequest


class PromptBuilder:
    def build_daily_check_in_prompt(self, payload: DailyCheckInRequest) -> str:
        active_exams = [exam.model_dump() for exam in payload.memory.active_exams]
        request_context = {
            "journal_entry": payload.journal_entry,
            "mood_score": payload.mood_score,
            "energy_score": payload.energy_score,
            "stress_score": payload.stress_score,
            "memory": {
                **payload.memory.model_dump(),
                "active_exams": active_exams,
                "primary_stressor_exam": payload.memory.primary_stressor_exam,
            },
        }
        instructions = {
            "role": "You are Breathe, an emotionally intelligent academic pressure analysis system.",
            "goal": (
                "Produce a single structured JSON object for a student check-in. "
                "Understand that a student may be carrying multiple exam contexts at once."
            ),
            "rules": [
                "Return valid JSON only.",
                "Do not include markdown, prose outside JSON, or code fences.",
                "Do not diagnose medical conditions.",
                "Avoid manipulative, dependency-forming, or overly intense wording.",
                "If distress looks severe, set safe_support_mode true and soften the response.",
                "Distinguish pressure between active exams and prioritize the current stressor exam.",
                "Recommendations must be specific, practical, and suitable for today's situation.",
                "Keep all text concise and grounded.",
            ],
            "analysis_focus": [
                "active_exams",
                "primary_stressor_exam",
                "exam-specific stress patterns",
                "pressure distribution",
                "longitudinal emotional cycles by exam",
            ],
            "milestone_examples": [
                "mock test crash",
                "burnout episode",
                "confidence rebound",
                "panic spike",
                "recovery phase",
                "consistency streak",
                "comparison spiral",
            ],
            "study_phase_options": [
                "starting",
                "building",
                "revision",
                "exam-near",
                "recovery",
                "unknown",
            ],
            "output_notes": [
                "Populate exam-aware fields when possible.",
                "Use the primary stressor exam for the most emotionally important insights.",
                "If multiple exams matter, explain the distinction explicitly in the JSON fields.",
            ],
        }
        return "\n\n".join(
            [
                "SYSTEM INSTRUCTIONS:",
                json.dumps(instructions, ensure_ascii=False),
                "STUDENT CHECK-IN INPUT:",
                json.dumps(request_context, ensure_ascii=False),
            ]
        )
