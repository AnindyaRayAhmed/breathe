export type HealthResponse = {
  status: string;
  service: string;
};

export type ExamPriority = "low" | "medium" | "high";

export type ExamContext = {
  name: string;
  priority: ExamPriority;
  exam_date: string;
};

export type StudyPhase =
  | "starting"
  | "building"
  | "revision"
  | "exam-near"
  | "recovery"
  | "unknown";

export type SeverityLevel = "low" | "moderate" | "high" | "critical";
export type ConfidenceSignal = "dipping" | "stable" | "recovering";
export type TrendDirection = "worsening" | "stable" | "improving" | "mixed";

export type OnboardingRequest = {
  active_exams: ExamContext[];
  primary_stressor_exam: string;
};

export type OnboardingResponse = {
  status: string;
  welcome_message: string;
  memory: MemorySnapshot;
};

export type MemoryMilestone = {
  event_type: string;
  title: string;
  severity_score: number;
  occurred_at: string;
  exam_name: string;
};

export type MemorySnapshot = {
  active_exams: ExamContext[];
  primary_stressor_exam: string;
  study_phase: StudyPhase;
  stress_triggers: string[];
  motivation_sources: string[];
  recurring_patterns: string[];
  coping_preferences: string[];
  milestone_history: MemoryMilestone[];
  emotional_trends: string[];
};

export type JournalAnalysisRequest = {
  journal_entry: string;
  mood_score: number;
  energy_score: number;
  stress_score: number;
  memory: MemorySnapshot;
};

export type SafetyAssessment = {
  severity_level: SeverityLevel;
  crisis_detected: boolean;
  harmful_language_detected: boolean;
  safe_support_mode: boolean;
  rationale: string;
  support_message: string;
  response_boundaries: string[];
};

export type IntentAnalysis = {
  primary_intent: string;
  secondary_intents: string[];
  reflection_depth: "surface" | "moderate" | "deep";
  help_seeking_signal: string;
  exam_context: string;
  primary_exams: string[];
};

export type EmotionalAnalysis = {
  primary_emotion: string;
  secondary_emotions: string[];
  emotional_tone: string;
  stress_level: SeverityLevel;
  burnout_risk: SeverityLevel;
  energy_state: string;
  confidence_signal: ConfidenceSignal;
  stress_triggers: string[];
  summary: string;
  primary_exam_context: string;
  secondary_exam_contexts: string[];
};

export type MemoryUpdates = {
  active_exams: ExamContext[];
  primary_stressor_exam: string;
  study_phase: StudyPhase;
  new_stress_triggers: string[];
  new_motivation_sources: string[];
  new_coping_preferences: string[];
  recurring_patterns: string[];
  emotional_trends: string[];
  memory_summary: string;
  exam_specific_insights: string[];
};

export type MilestoneEvent = {
  event_type: string;
  title: string;
  description: string;
  severity_score: number;
  confidence_score: number;
  occurred_at: string;
  action_signal: string;
  exam_name: string;
};

export type LongitudinalPattern = {
  pattern_name: string;
  description: string;
  direction: TrendDirection;
  confidence_score: number;
  exam_name: string;
};

export type Recommendations = {
  daily_actions: string[];
  study_recovery_balance: string;
  mindfulness_recommendation: string;
  stress_reduction_technique: string;
  support_nudge: string;
  target_exam: string;
  exam_specific_guidance: string;
};

export type ConversationResponse = {
  headline: string;
  encouragement: string;
  grounding_note: string;
  follow_up_prompt: string;
  exam_reference: string;
};

export type MultiAgentAnalysis = {
  safety_assessment: SafetyAssessment;
  intent_analysis: IntentAnalysis;
  emotional_analysis: EmotionalAnalysis;
  memory_updates: MemoryUpdates;
  milestone_events: MilestoneEvent[];
  longitudinal_patterns: LongitudinalPattern[];
  recommendations: Recommendations;
  conversation_response: ConversationResponse;
};

export type JournalAnalysisResponse = {
  status: "completed";
  source: "ai" | "fallback";
  analysis: MultiAgentAnalysis;
  updated_memory: MemorySnapshot;
};

export type WeeklyReflectionRequest = {
  week_summary: string;
};

export type WeeklyReflectionResponse = {
  status: string;
  insight: string;
  next_step: string;
};

export type MemoryUpdateRequest = {
  event_type: string;
  detail: string;
};

export type MemoryUpdateResponse = {
  status: string;
  memory_key: string;
  note: string;
};
