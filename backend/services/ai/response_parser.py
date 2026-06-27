from __future__ import annotations

import json

from pydantic import ValidationError

from backend.schemas.checkin import (
    ConversationResponse,
    DailyCheckInRequest,
    EmotionalAnalysis,
    IntentAnalysis,
    LongitudinalPattern,
    MemorySnapshot,
    MemoryUpdates,
    MilestoneEvent,
    MultiAgentAnalysis,
    Recommendations,
    SafetyAssessment,
)


class StructuredResponseError(ValueError):
    pass


def _get_primary_exam_name(payload: DailyCheckInRequest) -> str:
    if payload.memory.primary_stressor_exam.strip():
        return payload.memory.primary_stressor_exam.strip()
    if payload.memory.active_exams:
        return payload.memory.active_exams[0].name
    return ""


def parse_agent_response(raw_text: str) -> MultiAgentAnalysis:
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise StructuredResponseError("Gemini response was not valid JSON.") from exc

    try:
        return MultiAgentAnalysis.model_validate(parsed)
    except ValidationError as exc:
        raise StructuredResponseError("Gemini response did not match the expected schema.") from exc


def build_fallback_analysis(payload: DailyCheckInRequest, safe_support_mode: bool) -> MultiAgentAnalysis:
    primary_exam = _get_primary_exam_name(payload)
    active_exam_names = [exam.name for exam in payload.memory.active_exams if exam.name.strip()]
    elevated_stress = payload.stress_score >= 8
    low_energy = payload.energy_score <= 3
    low_mood = payload.mood_score <= 3

    burnout_risk = "high" if elevated_stress and low_energy else "moderate" if elevated_stress else "low"
    stress_level = "high" if elevated_stress else "moderate" if payload.stress_score >= 5 else "low"
    confidence_signal = "dipping" if low_mood else "recovering" if payload.mood_score >= 7 else "stable"

    return MultiAgentAnalysis(
        safety_assessment=SafetyAssessment(
            severity_level="high" if safe_support_mode else "moderate" if elevated_stress else "low",
            crisis_detected=safe_support_mode,
            harmful_language_detected=False,
            safe_support_mode=safe_support_mode,
            rationale="Fallback safety guard was used because live structured analysis was unavailable.",
            support_message=(
                "Please slow the day down and lean on trusted human support if things feel too heavy."
                if safe_support_mode
                else "You're safe to continue with a softer check-in response."
            ),
            response_boundaries=[
                "No medical diagnosis",
                "No manipulative dependency language",
                "Grounding-first tone",
            ],
        ),
        intent_analysis=IntentAnalysis(
            primary_intent="Emotional check-in during exam preparation",
            secondary_intents=["stress relief", "self-reflection"],
            reflection_depth="deep" if len(payload.journal_entry.split()) > 50 else "moderate",
            help_seeking_signal="The student is looking for calm reflection and useful support.",
            exam_context=(
                f"Pressure seems most connected to {primary_exam}."
                if primary_exam
                else "Exam-related pressure is likely shaping the current emotional state."
            ),
            primary_exams=active_exam_names[:4],
        ),
        emotional_analysis=EmotionalAnalysis(
            primary_emotion="overwhelmed" if elevated_stress else "mixed",
            secondary_emotions=["tired"] if low_energy else ["hopeful"],
            emotional_tone="strained but reflective" if elevated_stress else "honest and observant",
            stress_level=stress_level,
            burnout_risk=burnout_risk,
            energy_state="low energy" if low_energy else "steady energy",
            confidence_signal=confidence_signal,
            stress_triggers=["exam pressure", "performance uncertainty"],
            summary=(
                f"A fallback summary was generated from the student's self-reported check-in signals, with {primary_exam or 'the current exam load'} carrying the most pressure."
            ),
            primary_exam_context=primary_exam,
            secondary_exam_contexts=active_exam_names[1:4],
        ),
        memory_updates=MemoryUpdates(
            active_exams=payload.memory.active_exams,
            primary_stressor_exam=primary_exam,
            study_phase=payload.memory.study_phase,
            new_stress_triggers=["exam pressure"] if elevated_stress else [],
            new_motivation_sources=[],
            new_coping_preferences=["short reset breaks"] if low_energy else [],
            recurring_patterns=[
                f"pressure spikes around {primary_exam} performance tracking" if primary_exam else "pressure spikes around performance tracking"
            ]
            if elevated_stress
            else [],
            emotional_trends=[
                f"stress rises when {primary_exam or 'exam load'} deadlines feel closer" if elevated_stress else "stress rises when energy drops"
            ]
            if low_energy or elevated_stress
            else [],
            memory_summary=(
                f"Fallback memory update created from the current check-in signals, centered on {primary_exam or 'the active exam set'}."
            ),
            exam_specific_insights=[
                f"{primary_exam} appears to be the current pressure driver." if primary_exam else "Multiple exams are shaping the emotional load."
            ],
        ),
        milestone_events=[
            MilestoneEvent(
                event_type="panic spike" if elevated_stress else "consistency streak",
                title="Stress spike detected" if elevated_stress else "Steady reflection maintained",
                description=(
                    "Today's signals suggest a sharper pressure spike than usual."
                    if elevated_stress
                    else "The student is continuing to reflect consistently."
                ),
                severity_score=8 if elevated_stress else 4,
                confidence_score=0.62,
                occurred_at="",
                action_signal="Prioritize recovery before pushing harder today.",
                exam_name=primary_exam,
            )
        ],
        longitudinal_patterns=[
            LongitudinalPattern(
                pattern_name="Energy-stress coupling",
                description=(
                    f"Stress likely intensifies when energy is already low, especially around {primary_exam}."
                    if primary_exam
                    else "Stress likely intensifies when energy is already low."
                ),
                direction="worsening" if low_energy and elevated_stress else "mixed",
                confidence_score=0.58,
                exam_name=primary_exam,
            )
        ],
        recommendations=Recommendations(
            daily_actions=[
                f"Write one honest line about what feels heaviest about {primary_exam or 'today'} right now.",
                "Take a 10-minute screen-off pause before the next study block.",
                "Choose one priority topic instead of trying to rescue the whole day.",
            ],
            study_recovery_balance=(
                f"Shrink the next study goal around {primary_exam or 'the current pressure point'} and build one recovery pause into the hour."
            ),
            mindfulness_recommendation="Try a slow exhale cycle for two minutes before restarting work.",
            stress_reduction_technique="Do a grounding reset: name five things you can see and three you can feel.",
            support_nudge=(
                "Please reach out to a trusted friend, family member, mentor, or counselor today."
                if safe_support_mode
                else "Let someone supportive know this week has been heavier than usual."
            ),
            target_exam=primary_exam,
            exam_specific_guidance=(
                f"Treat {primary_exam} as the active pressure source and keep {', '.join(active_exam_names[1:3]) or 'other exams'} lighter today."
                if primary_exam
                else "Keep the recommendation tied to the current emotional load."
            ),
        ),
        conversation_response=ConversationResponse(
            headline="You do not need to force a perfect day.",
            encouragement=(
                "This looks like a heavy moment, and it makes sense that your system is asking for breathing room."
                if safe_support_mode
                else "You are carrying pressure, but you are also noticing it clearly, which gives us something real to work with."
            ),
            grounding_note="Focus on the next gentle step, not the whole exam timeline.",
            follow_up_prompt="What feels most salvageable about today if we make the plan smaller?",
            exam_reference=primary_exam,
        ),
    )


def merge_memory(
    current_memory: MemorySnapshot,
    updates: MemoryUpdates,
    milestones: list[MilestoneEvent],
    emotional_summary: EmotionalAnalysis,
    patterns: list[LongitudinalPattern],
) -> MemorySnapshot:
    def unique_compact(existing: list[str], additions: list[str], limit: int = 8) -> list[str]:
        seen: list[str] = []
        for item in [*existing, *additions]:
            normalized = item.strip()
            if normalized and normalized not in seen:
                seen.append(normalized)
        return seen[:limit]

    milestone_history = current_memory.milestone_history[:]
    existing_keys = {(item.event_type, item.title) for item in milestone_history}
    for milestone in milestones:
        key = (milestone.event_type, milestone.title)
        if key not in existing_keys:
            milestone_history.append(
                {
                    "event_type": milestone.event_type,
                    "title": milestone.title,
                    "severity_score": milestone.severity_score,
                    "occurred_at": milestone.occurred_at,
                    "exam_name": milestone.exam_name,
                }
            )
            existing_keys.add(key)

    trend_additions = updates.emotional_trends + [emotional_summary.summary] + [pattern.description for pattern in patterns]

    return MemorySnapshot(
        active_exams=updates.active_exams or current_memory.active_exams,
        primary_stressor_exam=updates.primary_stressor_exam or current_memory.primary_stressor_exam,
        study_phase=updates.study_phase if updates.study_phase != "unknown" else current_memory.study_phase,
        stress_triggers=unique_compact(current_memory.stress_triggers, updates.new_stress_triggers),
        motivation_sources=unique_compact(current_memory.motivation_sources, updates.new_motivation_sources),
        recurring_patterns=unique_compact(current_memory.recurring_patterns, updates.recurring_patterns),
        coping_preferences=unique_compact(current_memory.coping_preferences, updates.new_coping_preferences),
        milestone_history=MemorySnapshot.model_validate(
            {"milestone_history": milestone_history},
        ).milestone_history[:12],
        emotional_trends=unique_compact(current_memory.emotional_trends, trend_additions),
    )
