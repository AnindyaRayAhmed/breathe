import { SectionCard } from "../components/SectionCard";
import { StatusBadge } from "../components/StatusBadge";
import type { JournalAnalysisResponse } from "../types/api";

type ReflectionDashboardPageProps = {
  result: JournalAnalysisResponse | null;
};

function formatSeverity(label: string) {
  return label.replace("-", " ");
}

export function ReflectionDashboardPage({ result }: ReflectionDashboardPageProps) {
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

  return (
    <div className="grid gap-6">
      {analysis.safety_assessment.safe_support_mode ? (
        <section className="rounded-[1.75rem] border border-[#e6c6bd] bg-[#fff3ef] p-5 text-[#7d3f34]">
          <h2 className="text-lg font-semibold">Gentle support mode is on</h2>
          <p className="mt-2 text-sm leading-6">{analysis.safety_assessment.support_message}</p>
        </section>
      ) : null}

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <SectionCard title="Reflection Dashboard" description="A composed read of the emotional pattern inside today's check-in.">
          <div className="flex flex-wrap gap-2">
            <StatusBadge label={`Source: ${source}`} />
            <StatusBadge label={`Stress: ${formatSeverity(analysis.emotional_analysis.stress_level)}`} />
            <StatusBadge label={`Burnout risk: ${formatSeverity(analysis.emotional_analysis.burnout_risk)}`} />
            {analysis.recommendations.target_exam ? (
              <StatusBadge label={`Focus: ${analysis.recommendations.target_exam}`} />
            ) : null}
          </div>
          <h3 className="mt-5 text-2xl font-semibold text-stone-900">
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
        </SectionCard>

        <SectionCard title="Current signals" description="A quick snapshot of what the orchestration system sees.">
          <dl className="space-y-3 text-sm">
            <div className="rounded-3xl bg-[#f8f1e7] px-4 py-3">
              <dt className="text-stone-500">Primary emotion</dt>
              <dd className="mt-1 font-medium text-stone-900">{analysis.emotional_analysis.primary_emotion}</dd>
            </div>
            <div className="rounded-3xl bg-[#f8f1e7] px-4 py-3">
              <dt className="text-stone-500">Energy state</dt>
              <dd className="mt-1 font-medium text-stone-900">{analysis.emotional_analysis.energy_state}</dd>
            </div>
            <div className="rounded-3xl bg-[#f8f1e7] px-4 py-3">
              <dt className="text-stone-500">Confidence signal</dt>
              <dd className="mt-1 font-medium text-stone-900">{analysis.emotional_analysis.confidence_signal}</dd>
            </div>
            <div className="rounded-3xl bg-[#f8f1e7] px-4 py-3">
              <dt className="text-stone-500">Intent</dt>
              <dd className="mt-1 font-medium text-stone-900">{analysis.intent_analysis.primary_intent}</dd>
            </div>
          </dl>
        </SectionCard>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <SectionCard title="Stress triggers" description="Signals that may be pushing the nervous system harder than usual.">
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
        <SectionCard title="Encouragement" description="Supportive language shaped to the emotional moment.">
          <p className="text-sm leading-7 text-stone-600">{analysis.conversation_response.grounding_note}</p>
          <p className="mt-4 rounded-3xl bg-[#f8f1e7] px-4 py-3 text-sm leading-7 text-stone-700">
            {analysis.conversation_response.follow_up_prompt}
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
                <p className="mt-2 text-stone-500">
                  Severity {milestone.severity_score}/10
                </p>
              </li>
            ))}
          </ul>
        </SectionCard>
        <SectionCard title="Hidden patterns" description="Longitudinal signals that standard trackers often miss.">
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
