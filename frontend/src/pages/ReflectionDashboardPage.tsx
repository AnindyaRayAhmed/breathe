import { SectionCard } from "../components/SectionCard";
import { StatusBadge } from "../components/StatusBadge";
import type { JournalAnalysisResponse, MemorySnapshot } from "../types/api";

type ReflectionDashboardPageProps = {
  result: JournalAnalysisResponse | null;
  memory: MemorySnapshot;
};

function formatSeverity(label: string) {
  return label.replace("-", " ");
}

export function ReflectionDashboardPage({ result, memory }: ReflectionDashboardPageProps) {
  if (!result) {
    return (
      <SectionCard
        title="Reflection Dashboard"
        description="Your latest emotional analysis will appear here after a Daily Check-In."
      >
        <p className="text-sm leading-6 text-stone-600">
          Start with the check-in page and the dashboard will render emotional signals, recommendations, milestones, and encouragement here.
        </p>
      </SectionCard>
    );
  }

  const { analysis, source } = result;
  const pressureSource =
    analysis.recommendations.target_exam ||
    memory.primary_stressor_exam ||
    memory.active_exams[0]?.name ||
    "the current exam mix";
  const recurringTrigger =
    analysis.emotional_analysis.stress_triggers[0] ||
    memory.stress_triggers[0] ||
    "your system is still learning the pattern";
  const resilienceSignal =
    memory.coping_preferences[0] || analysis.emotional_analysis.confidence_signal;
  const recoveryTrend =
    memory.emotional_trends[0] ||
    analysis.longitudinal_patterns[0]?.description ||
    "Recovery is built through small, steady pauses.";
  const consistencyCount = memory.milestone_history.length;
  const streakLabel =
    consistencyCount >= 3
      ? "You’ve been keeping a steady breathing streak."
      : consistencyCount > 0
        ? "Your breathing streak is taking shape."
        : "Your breathing streak starts with this kind of check-in.";

  return (
    <div className="grid gap-6">
      {source === "fallback" ? (
        <section className="rounded-[1.75rem] border border-[#ebdcb9] bg-[#fffbf0] p-5 text-[#856404]">
          <h2 className="text-lg font-semibold">Operating in Local Fallback Mode</h2>
          <p className="mt-2 text-sm leading-6">
            Real-time AI analysis is currently unavailable or not configured. You are seeing a locally computed safety-first assessment and reflection guidance.
          </p>
        </section>
      ) : null}

      {analysis.safety_assessment.safe_support_mode ? (
        <section className="rounded-[1.75rem] border border-[#e6c6bd] bg-[#fff3ef] p-5 text-[#7d3f34]">
          <h2 className="text-lg font-semibold">Gentle support mode is on</h2>
          <p className="mt-2 text-sm leading-6">{analysis.safety_assessment.support_message}</p>
        </section>
      ) : null}

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <SectionCard
          title="Reflection Dashboard"
          description="A composed read of the emotional pattern inside today's check-in."
        >
          <div className="flex flex-wrap gap-2">
            <StatusBadge label={`Source: ${source}`} />
            <StatusBadge label={`Stress: ${formatSeverity(analysis.emotional_analysis.stress_level)}`} />
            <StatusBadge label={`Burnout risk: ${formatSeverity(analysis.emotional_analysis.burnout_risk)}`} />
            {analysis.recommendations.target_exam ? (
              <StatusBadge label={`Focus: ${analysis.recommendations.target_exam}`} />
            ) : null}
          </div>
          <h3 className="mt-5 font-serif text-3xl tracking-tight text-stone-900">
            {analysis.conversation_response.headline}
          </h3>
          <p className="mt-3 text-sm leading-7 text-stone-600">
            {analysis.emotional_analysis.summary}
          </p>
          <p className="mt-4 rounded-3xl bg-[#f6eee3] px-4 py-4 text-sm leading-7 text-stone-700">
            {analysis.conversation_response.encouragement}
          </p>
          {analysis.recommendations.exam_specific_guidance ? (
            <p className="mt-4 rounded-3xl bg-[#f8f1e7] px-4 py-4 text-sm leading-7 text-stone-700">
              {analysis.recommendations.exam_specific_guidance}
            </p>
          ) : null}
          <div className="mt-5 grid gap-3 rounded-[1.75rem] border border-[#eadccc] bg-[#fffaf4] p-4 sm:grid-cols-2">
            <div>
              <p className="text-xs uppercase tracking-[0.25em] text-[#9a7452]">Breathing streak</p>
              <p className="mt-2 font-serif text-2xl tracking-tight text-stone-900">
                {consistencyCount}
                <span className="ml-2 text-sm font-sans text-stone-500">reflections remembered</span>
              </p>
              <p className="mt-2 text-sm leading-6 text-stone-600">{streakLabel}</p>
              <p className="mt-2 text-sm leading-6 text-stone-600">
                Consistency matters more than perfection.
              </p>
            </div>
            <div className="rounded-[1.5rem] bg-[#f8f1e7] p-4 text-sm leading-6 text-stone-600">
              <p className="font-medium text-stone-900">Demo continuity</p>
              <p className="mt-2">
                Memory holds {memory.active_exams.length} active exam context
                {memory.active_exams.length === 1 ? "" : "s"} so the reflection can stay personal.
              </p>
            </div>
          </div>
        </SectionCard>

        <SectionCard
          title="Current signals"
          description="A quick snapshot of what the orchestration system sees."
        >
          <div className="space-y-3 text-sm">
            <div className="rounded-3xl bg-[#f8f1e7] px-4 py-3">
              <p className="text-stone-500">Primary emotion</p>
              <p className="mt-1 font-medium text-stone-900">{analysis.emotional_analysis.primary_emotion}</p>
            </div>
            <div className="rounded-3xl bg-[#f8f1e7] px-4 py-3">
              <p className="text-stone-500">Energy state</p>
              <p className="mt-1 font-medium text-stone-900">{analysis.emotional_analysis.energy_state}</p>
            </div>
            <div className="rounded-3xl bg-[#f8f1e7] px-4 py-3">
              <p className="text-stone-500">Confidence signal</p>
              <p className="mt-1 font-medium text-stone-900">{analysis.emotional_analysis.confidence_signal}</p>
            </div>
            <div className="rounded-3xl bg-[#f8f1e7] px-4 py-3">
              <p className="text-stone-500">Intent</p>
              <p className="mt-1 font-medium text-stone-900">{analysis.intent_analysis.primary_intent}</p>
            </div>
          </div>
        </SectionCard>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1fr_1fr_1.05fr]">
        <SectionCard
          title="Stress triggers"
          description="Signals that may be pushing the nervous system harder than usual."
        >
          <ul className="space-y-3 text-sm leading-6 text-stone-600">
            {analysis.emotional_analysis.stress_triggers.map((trigger) => (
              <li key={trigger} className="rounded-3xl bg-[#f8f1e7] px-4 py-3">
                {trigger}
              </li>
            ))}
          </ul>
        </SectionCard>
        <SectionCard title="Recommendations" description="Specific, exam-aware support for the rest of today.">
          <ul className="space-y-3 text-sm leading-6 text-stone-600">
            {analysis.recommendations.daily_actions.map((action) => (
              <li key={action} className="rounded-3xl bg-[#f8f1e7] px-4 py-3">
                {action}
              </li>
            ))}
          </ul>
          <p className="mt-4 text-sm leading-6 text-stone-600">
            {analysis.recommendations.study_recovery_balance}
          </p>
        </SectionCard>
        <SectionCard
          title="Encouragement"
          description="Supportive language shaped to the emotional moment."
        >
          <p className="text-sm leading-7 text-stone-600">{analysis.conversation_response.grounding_note}</p>
          <p className="mt-4 rounded-3xl bg-[#f8f1e7] px-4 py-3 text-sm leading-7 text-stone-700">
            {analysis.conversation_response.follow_up_prompt}
          </p>
          <p className="mt-4 text-sm leading-6 text-stone-500">
            You tend to become self-critical after mock tests, so the tone stays deliberately gentle.
          </p>
        </SectionCard>
      </div>

      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <SectionCard title="Milestone events" description="Moments worth noticing, even if they are messy.">
          <ul className="space-y-3 text-sm leading-6 text-stone-600">
            {analysis.milestone_events.map((milestone) => (
              <li key={`${milestone.event_type}-${milestone.title}`} className="rounded-3xl bg-[#f8f1e7] px-4 py-4">
                <p className="font-medium text-stone-900">{milestone.title}</p>
                <p className="mt-1">{milestone.description}</p>
                <p className="mt-2 text-stone-500">Severity {milestone.severity_score}/10</p>
              </li>
            ))}
          </ul>
        </SectionCard>
        <SectionCard title="Hidden patterns" description="Longitudinal signals that standard trackers often miss.">
          <div className="mb-4 rounded-[1.75rem] border border-[#eadccc] bg-[#fffaf4] px-4 py-4 text-sm leading-6 text-stone-600">
            <p className="font-medium text-stone-900">Pressure ecosystem</p>
            <p className="mt-2">
              Highest current pressure source: <span className="text-stone-900">{pressureSource}</span>
            </p>
            <p className="mt-1">
              Recurring emotional trigger: <span className="text-stone-900">{recurringTrigger}</span>
            </p>
            <p className="mt-1">
              Resilience signal: <span className="text-stone-900">{resilienceSignal}</span>
            </p>
            <p className="mt-1">
              Recovery trend: <span className="text-stone-900">{recoveryTrend}</span>
            </p>
          </div>
          <ul className="space-y-3 text-sm leading-6 text-stone-600">
            {analysis.longitudinal_patterns.map((pattern) => (
              <li key={pattern.pattern_name} className="rounded-3xl bg-[#f8f1e7] px-4 py-4">
                <p className="font-medium text-stone-900">{pattern.pattern_name}</p>
                <p className="mt-1">{pattern.description}</p>
                <p className="mt-2 text-stone-500">Direction: {pattern.direction}</p>
              </li>
            ))}
          </ul>
        </SectionCard>
      </div>
    </div>
  );
}
