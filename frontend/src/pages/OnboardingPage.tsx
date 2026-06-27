import type { FormEvent } from "react";
import { useMemo, useState } from "react";
import { SectionCard } from "../components/SectionCard";
import { StatusBadge } from "../components/StatusBadge";
import { submitOnboarding } from "../services/api";
import type { ExamContext, MemorySnapshot } from "../types/api";

type OnboardingPageProps = {
  memory: MemorySnapshot;
  onComplete: (memory: MemorySnapshot) => void;
};

const suggestedExams: Array<{ name: string; priority: ExamContext["priority"] }> = [
  { name: "JEE", priority: "high" },
  { name: "BITSAT", priority: "medium" },
  { name: "NEET", priority: "high" },
  { name: "Boards", priority: "medium" },
  { name: "CAT", priority: "high" },
  { name: "OMETs", priority: "medium" },
  { name: "UPSC", priority: "high" },
  { name: "State PSC", priority: "medium" },
  { name: "GATE", priority: "high" },
  { name: "Placements", priority: "medium" },
];

function createExam(name: string, priority: ExamContext["priority"] = "medium", examDate = ""): ExamContext {
  return { name, priority, exam_date: examDate };
}

export function OnboardingPage({ memory, onComplete }: OnboardingPageProps) {
  const [activeExams, setActiveExams] = useState<ExamContext[]>(
    memory.active_exams.length > 0 ? memory.active_exams : [createExam("JEE", "high")],
  );
  const [primaryStressorExam, setPrimaryStressorExam] = useState(
    memory.primary_stressor_exam || memory.active_exams[0]?.name || activeExams[0]?.name || "",
  );
  const [customExamName, setCustomExamName] = useState("");
  const [customExamDate, setCustomExamDate] = useState("");
  const [customExamPriority, setCustomExamPriority] = useState<ExamContext["priority"]>("medium");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const normalizedNames = useMemo(
    () => activeExams.map((exam) => exam.name.trim().toLowerCase()),
    [activeExams],
  );
  const isSeededDemo = memory.active_exams.length > 0 && memory.milestone_history.length > 0;

  function addExam(exam: ExamContext) {
    const normalized = exam.name.trim().toLowerCase();
    if (!normalized || normalizedNames.includes(normalized)) {
      return;
    }

    setActiveExams((current) => [...current, exam]);
    if (!primaryStressorExam) {
      setPrimaryStressorExam(exam.name);
    }
  }

  function removeExam(name: string) {
    setActiveExams((current) => {
      const remaining = current.filter((exam) => exam.name !== name);
      if (primaryStressorExam === name) {
        setPrimaryStressorExam(remaining[0]?.name ?? "");
      }
      return remaining;
    });
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const cleanedExams = activeExams
      .map((exam) => ({
        ...exam,
        name: exam.name.trim(),
        exam_date: exam.exam_date.trim(),
      }))
      .filter((exam) => exam.name.length > 0);

    if (cleanedExams.length === 0) {
      setErrorMessage("Add at least one active exam so Breathe can understand the pressure context.");
      return;
    }

    if (!primaryStressorExam.trim()) {
      setErrorMessage("Choose the exam that feels most emotionally overwhelming right now.");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage("");

    try {
      const response = await submitOnboarding({
        active_exams: cleanedExams,
        primary_stressor_exam: primaryStressorExam.trim(),
      });
      onComplete(response.memory);
    } catch {
      setErrorMessage("We could not save the onboarding profile right now. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="grid gap-6">
      <section className="grid gap-6 rounded-[2.25rem] border border-[#eadccc] bg-[#fffaf4] p-6 shadow-soft lg:grid-cols-[1.2fr_0.8fr] lg:p-8">
        <div className="grid gap-4">
          <div className="flex items-center gap-3">
            <img src="/logo.svg" alt="Breathe logo" className="h-10 w-auto" />
            <div>
              <p className="text-xs uppercase tracking-[0.35em] text-[#9a7452]">Breathe onboarding</p>
              <p className="text-sm text-stone-500">Multiple exams. One calmer emotional map.</p>
            </div>
          </div>
          <div className="max-w-2xl space-y-3">
            <h2 className="font-serif text-3xl tracking-tight text-stone-900 sm:text-4xl">
              What are you currently preparing for?
            </h2>
            <p className="text-sm leading-7 text-stone-600 sm:text-base">
              Add all active exams, then mark the one that feels most emotionally overwhelming right now.
              Breathe will keep track of pressure distribution instead of flattening everything into one label.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <StatusBadge label="Multiple exams supported" />
            <StatusBadge label="Chip-based editing" />
            <StatusBadge label="Emotionally safe memory" />
          </div>
          {isSeededDemo ? (
            <div className="rounded-[1.75rem] border border-[#e4d2bf] bg-[#f7eee2] p-4">
              <p className="text-sm font-medium text-stone-900">Demo memory is already seeded</p>
              <p className="mt-2 text-sm leading-6 text-stone-600">
                This first-time view includes a small memory trail so the dashboard can immediately show recurring patterns, milestone continuity, and exam-specific pressure.
              </p>
            </div>
          ) : null}
        </div>

        <aside className="grid gap-3 rounded-[1.75rem] border border-[#eadccc] bg-[#fffdf8] p-5">
          <p className="text-sm font-medium text-stone-900">Why this matters</p>
          <ul className="space-y-3 text-sm leading-6 text-stone-600">
            <li>Students often carry multiple exam contexts at once, each with different pressure patterns.</li>
            <li>One exam can be the emotional center without being the only one that matters.</li>
            <li>Breathe remembers the pressure ecosystem, not just a single exam label.</li>
          </ul>
        </aside>
      </section>

      <div className="grid gap-6 lg:grid-cols-[1.25fr_0.75fr]">
        <SectionCard
          title="Build your exam context"
          description="Add one or more exams, then mark the one that feels most emotionally overwhelming."
        >
          <form className="grid gap-6" onSubmit={handleSubmit}>
            <div className="space-y-3">
              <p className="text-sm leading-6 text-stone-600">
                You can add custom exams, mix major and secondary prep tracks, and remove anything that no longer fits.
              </p>
              <div className="flex flex-wrap gap-2">
                {activeExams.map((exam) => {
                  const isPrimary = primaryStressorExam === exam.name;
                  return (
                    <div
                      key={`${exam.name}-${exam.exam_date}`}
                      className={[
                        "inline-flex items-center gap-2 rounded-full border px-4 py-2 text-sm transition",
                        isPrimary
                          ? "border-[#a97b54] bg-[#f3e4d4] text-stone-900"
                          : "border-[#dccdb9] bg-[#fffaf3] text-stone-700 hover:bg-[#f7efe5]",
                      ].join(" ")}
                    >
                      <button
                        type="button"
                        aria-pressed={isPrimary}
                        onClick={() => setPrimaryStressorExam(exam.name)}
                        className="flex items-center gap-2"
                      >
                        <span className="font-medium">{exam.name}</span>
                        {exam.exam_date ? (
                          <span className="text-xs lowercase tracking-wide text-stone-500">
                            {exam.exam_date}
                          </span>
                        ) : null}
                        <span className="text-xs uppercase tracking-wide text-stone-500">
                          {exam.priority}
                        </span>
                      </button>
                      <button
                        type="button"
                        aria-label={`Remove ${exam.name}`}
                        onClick={() => removeExam(exam.name)}
                        className="rounded-full bg-white/70 px-2 py-0.5 text-xs text-stone-500 transition hover:bg-white"
                      >
                        x
                      </button>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="grid gap-4 rounded-[1.75rem] border border-[#eadbca] bg-[#fffdf9] p-4">
              <div className="grid gap-3 md:grid-cols-[1.4fr_0.8fr_0.8fr_0.6fr]">
                <label className="grid gap-2">
                  <span className="text-sm font-medium text-stone-800">Custom exam</span>
                  <input
                    value={customExamName}
                    onChange={(event) => setCustomExamName(event.target.value)}
                    className="rounded-xl border border-[#dccdb9] bg-[#fffaf3] px-4 py-3 text-stone-800 outline-none placeholder:text-stone-400 focus:border-[#b79069]"
                    placeholder="e.g. JEE Mains"
                  />
                </label>
                <label className="grid gap-2">
                  <span className="text-sm font-medium text-stone-800">Priority</span>
                  <select
                    value={customExamPriority}
                    onChange={(event) => setCustomExamPriority(event.target.value as ExamContext["priority"])}
                    className="rounded-xl border border-[#dccdb9] bg-[#fffaf3] px-4 py-3 text-stone-800 outline-none focus:border-[#b79069]"
                  >
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>
                </label>
                <label className="grid gap-2">
                  <span className="text-sm font-medium text-stone-800">Exam date</span>
                  <input
                    type="date"
                    value={customExamDate}
                    onChange={(event) => setCustomExamDate(event.target.value)}
                    className="rounded-xl border border-[#dccdb9] bg-[#fffaf3] px-4 py-3 text-stone-800 outline-none focus:border-[#b79069]"
                  />
                </label>
                <button
                  type="button"
                  onClick={() => {
                    addExam(createExam(customExamName, customExamPriority, customExamDate));
                    setCustomExamName("");
                    setCustomExamDate("");
                    setCustomExamPriority("medium");
                  }}
                  className="mt-auto rounded-full bg-[#2d2926] px-4 py-3 text-sm font-semibold text-[#fffaf3] transition hover:bg-[#473f38]"
                >
                  Add
                </button>
              </div>

              <div className="flex flex-wrap gap-2">
                {suggestedExams.map((exam) => (
                  <button
                    key={exam.name}
                    type="button"
                    onClick={() => addExam(createExam(exam.name, exam.priority))}
                    className="rounded-full border border-[#dccdb9] bg-[#fffaf3] px-3 py-2 text-sm text-stone-700 transition hover:bg-[#f7efe5]"
                  >
                    + {exam.name}
                  </button>
                ))}
              </div>
            </div>

            <label className="grid gap-2">
              <span className="text-sm font-medium text-stone-800">
                Which one feels the most emotionally overwhelming right now?
              </span>
              <select
                value={primaryStressorExam}
                onChange={(event) => setPrimaryStressorExam(event.target.value)}
                className="rounded-xl border border-[#dccdb9] bg-[#fffaf3] px-4 py-3 text-stone-800 outline-none focus:border-[#b79069]"
              >
                <option value="">Select the primary stressor</option>
                {activeExams.map((exam) => (
                  <option key={exam.name} value={exam.name}>
                    {exam.name}
                  </option>
                ))}
              </select>
            </label>

            {errorMessage ? (
              <p role="alert" className="rounded-2xl bg-[#f8dfd6] px-4 py-3 text-sm text-[#8c3b2c]">
                {errorMessage}
              </p>
            ) : null}

            <div className="flex flex-wrap items-center justify-between gap-3">
              <p className="text-sm leading-6 text-stone-600">
                This setup teaches Breathe which exam contexts matter, which one is carrying the heaviest emotional load, and how pressure should be distributed.
              </p>
              <button
                type="submit"
                disabled={isSubmitting}
                className="rounded-full bg-[#2d2926] px-5 py-3 text-sm font-semibold text-[#fffaf3] transition hover:bg-[#473f38] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isSubmitting ? "Saving..." : "Save onboarding"}
              </button>
            </div>
          </form>
        </SectionCard>

        <SectionCard
          title="Pressure ecosystem"
          description="A small reminder of the emotional terrain already in memory."
        >
          <div className="space-y-4 text-sm leading-6 text-stone-600">
            <div className="rounded-3xl bg-[#f8f1e7] px-4 py-4">
              <p className="text-stone-500">Highest current pressure source</p>
              <p className="mt-1 font-medium text-stone-900">{memory.primary_stressor_exam || "not set yet"}</p>
            </div>
            <div className="rounded-3xl bg-[#f8f1e7] px-4 py-4">
              <p className="text-stone-500">Recurring emotional trigger</p>
              <p className="mt-1 font-medium text-stone-900">
                {memory.stress_triggers[0] || "This will appear once a few check-ins are saved."}
              </p>
            </div>
            <div className="rounded-3xl bg-[#f8f1e7] px-4 py-4">
              <p className="text-stone-500">Resilience signal</p>
              <p className="mt-1 font-medium text-stone-900">
                {memory.coping_preferences[0] || "Small grounding habits are already part of the story."}
              </p>
            </div>
            <div className="rounded-3xl bg-[#f8f1e7] px-4 py-4">
              <p className="text-stone-500">Recovery trend</p>
              <p className="mt-1 font-medium text-stone-900">
                {memory.emotional_trends[0] || "Recovery grows through short pauses, not perfection."}
              </p>
            </div>
          </div>
        </SectionCard>
      </div>
    </div>
  );
}
