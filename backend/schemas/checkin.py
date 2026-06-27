from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


SeverityLevel = Literal["low", "moderate", "high", "critical"]
TrendDirection = Literal["worsening", "stable", "improving", "mixed"]
ConfidenceSignal = Literal["dipping", "stable", "recovering"]
ReflectionDepth = Literal["surface", "moderate", "deep"]
StudyPhase = Literal["starting", "building", "revision", "exam-near", "recovery", "unknown"]
ExamPriority = Literal["low", "medium", "high"]


class ExamContext(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    priority: ExamPriority
    exam_date: str = Field(default="", max_length=20)


class MemoryMilestone(BaseModel):
    event_type: str = Field(min_length=1, max_length=60)
    title: str = Field(min_length=1, max_length=120)
    severity_score: int = Field(ge=1, le=10)
    occurred_at: str = Field(default="")
    exam_name: str = Field(default="", max_length=80)


class MemorySnapshot(BaseModel):
    active_exams: list[ExamContext] = Field(default_factory=list, max_length=8)
    primary_stressor_exam: str = Field(default="", max_length=80)
    study_phase: StudyPhase = "unknown"
    stress_triggers: list[str] = Field(default_factory=list, max_length=8)
    motivation_sources: list[str] = Field(default_factory=list, max_length=8)
    recurring_patterns: list[str] = Field(default_factory=list, max_length=8)
    coping_preferences: list[str] = Field(default_factory=list, max_length=8)
    milestone_history: list[MemoryMilestone] = Field(default_factory=list, max_length=12)
    emotional_trends: list[str] = Field(default_factory=list, max_length=8)


class SafetyAssessment(BaseModel):
    severity_level: SeverityLevel
    crisis_detected: bool
    harmful_language_detected: bool
    safe_support_mode: bool
    rationale: str = Field(min_length=1, max_length=500)
    support_message: str = Field(min_length=1, max_length=500)
    response_boundaries: list[str] = Field(default_factory=list, max_length=6)


class IntentAnalysis(BaseModel):
    primary_intent: str = Field(min_length=1, max_length=120)
    secondary_intents: list[str] = Field(default_factory=list, max_length=5)
    reflection_depth: ReflectionDepth
    help_seeking_signal: str = Field(min_length=1, max_length=160)
    exam_context: str = Field(min_length=1, max_length=160)
    primary_exams: list[str] = Field(default_factory=list, max_length=4)


class EmotionalAnalysis(BaseModel):
    primary_emotion: str = Field(min_length=1, max_length=60)
    secondary_emotions: list[str] = Field(default_factory=list, max_length=6)
    emotional_tone: str = Field(min_length=1, max_length=120)
    stress_level: SeverityLevel
    burnout_risk: SeverityLevel
    energy_state: str = Field(min_length=1, max_length=60)
    confidence_signal: ConfidenceSignal
    stress_triggers: list[str] = Field(default_factory=list, max_length=6)
    summary: str = Field(min_length=1, max_length=500)
    primary_exam_context: str = Field(default="", max_length=80)
    secondary_exam_contexts: list[str] = Field(default_factory=list, max_length=4)


class MemoryUpdates(BaseModel):
    active_exams: list[ExamContext] = Field(default_factory=list, max_length=8)
    primary_stressor_exam: str = Field(default="", max_length=80)
    study_phase: StudyPhase = "unknown"
    new_stress_triggers: list[str] = Field(default_factory=list, max_length=6)
    new_motivation_sources: list[str] = Field(default_factory=list, max_length=6)
    new_coping_preferences: list[str] = Field(default_factory=list, max_length=6)
    recurring_patterns: list[str] = Field(default_factory=list, max_length=6)
    emotional_trends: list[str] = Field(default_factory=list, max_length=6)
    memory_summary: str = Field(min_length=1, max_length=400)
    exam_specific_insights: list[str] = Field(default_factory=list, max_length=6)


class MilestoneEvent(BaseModel):
    event_type: str = Field(min_length=1, max_length=60)
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=280)
    severity_score: int = Field(ge=1, le=10)
    confidence_score: float = Field(ge=0.0, le=1.0)
    occurred_at: str = Field(default="")
    action_signal: str = Field(min_length=1, max_length=200)
    exam_name: str = Field(default="", max_length=80)


class LongitudinalPattern(BaseModel):
    pattern_name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=240)
    direction: TrendDirection
    confidence_score: float = Field(ge=0.0, le=1.0)
    exam_name: str = Field(default="", max_length=80)


class Recommendations(BaseModel):
    daily_actions: list[str] = Field(default_factory=list, max_length=4)
    study_recovery_balance: str = Field(min_length=1, max_length=220)
    mindfulness_recommendation: str = Field(min_length=1, max_length=220)
    stress_reduction_technique: str = Field(min_length=1, max_length=220)
    support_nudge: str = Field(min_length=1, max_length=220)
    target_exam: str = Field(default="", max_length=80)
    exam_specific_guidance: str = Field(default="", max_length=260)


class ConversationResponse(BaseModel):
    headline: str = Field(min_length=1, max_length=120)
    encouragement: str = Field(min_length=1, max_length=320)
    grounding_note: str = Field(min_length=1, max_length=220)
    follow_up_prompt: str = Field(min_length=1, max_length=220)
    exam_reference: str = Field(default="", max_length=80)


class MultiAgentAnalysis(BaseModel):
    safety_assessment: SafetyAssessment
    intent_analysis: IntentAnalysis
    emotional_analysis: EmotionalAnalysis
    memory_updates: MemoryUpdates
    milestone_events: list[MilestoneEvent] = Field(default_factory=list, max_length=6)
    longitudinal_patterns: list[LongitudinalPattern] = Field(default_factory=list, max_length=5)
    recommendations: Recommendations
    conversation_response: ConversationResponse


class DailyCheckInRequest(BaseModel):
    journal_entry: str = Field(min_length=8, max_length=5000)
    mood_score: int = Field(ge=1, le=10)
    energy_score: int = Field(ge=1, le=10)
    stress_score: int = Field(ge=1, le=10)
    memory: MemorySnapshot = Field(default_factory=MemorySnapshot)


class DailyCheckInResponse(BaseModel):
    status: Literal["completed"]
    source: Literal["ai", "fallback"]
    analysis: MultiAgentAnalysis
    updated_memory: MemorySnapshot
