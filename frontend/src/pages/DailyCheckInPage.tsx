import type { FormEvent } from "react";
import { useState } from "react";
import { SectionCard } from "../components/SectionCard";
import { SliderField } from "../components/SliderField";
import { submitJournalAnalysis } from "../services/api";
import type { JournalAnalysisResponse, MemorySnapshot } from "../types/api";

type DailyCheckInPageProps = {
  memory: MemorySnapshot;
  onComplete: (response: JournalAnalysisResponse) => void;
};

export function DailyCheckInPage({ memory, onComplete }: DailyCheckInPageProps) {
  const [journalEntry, setJournalEntry] = useState("");
  const [moodScore, setMoodScore] = useState(5);
  const [energyScore, setEnergyScore] = useState(5);
  const [stressScore, setStressScore] = useState(5);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (journalEntry.trim().length < 8) {
      setErrorMessage("Share at least a short honest check-in so the reflection can stay useful.");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage("");

    try {
      const response = await submitJournalAnalysis({
        journal_entry: journalEntry,
        mood_score: moodScore,
        energy_score: energyScore,
        stress_score: stressScore,
        memory,
      });
      onComplete(response);
    } catch {
      setErrorMessage("The reflection did not go through. Please try again in a moment.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
      <SectionCard
        title="Daily Check-In"
        description="A soft place to log what today feels like before the pressure gets louder."
      >
        <form className="grid gap-5" onSubmit={handleSubmit}>
          <label className="grid gap-2">
            <span className="text-sm font-medium text-stone-800">Journal reflection</span>
            <span className="text-sm text-stone-500">
              Write naturally. It can be messy, short, or emotionally specific.
            </span>
            <textarea
              aria-label="Daily journal reflection"
              rows={8}
              value={journalEntry}
              onChange={(event) => setJournalEntry(event.target.value)}
              className="rounded-[1.75rem] border border-[#dccdb9] bg-[#fffaf3] px-4 py-4 text-stone-800 outline-none transition placeholder:text-stone-400 focus:border-[#b79069] focus:ring-2 focus:ring-[#ead8c3]"
              placeholder="Today felt heavier after a mock test... or maybe I am just carrying too much at once."
            />
          </label>

          <div className="grid gap-4 md:grid-cols-3">
            <SliderField
              id="mood-score"
              label="Mood"
              hint="1 means really low, 10 means steady and good."
              value={moodScore}
              onChange={setMoodScore}
            />
            <SliderField
              id="energy-score"
              label="Energy"
              hint="How much fuel you have left today."
              value={energyScore}
              onChange={setEnergyScore}
            />
            <SliderField
              id="stress-score"
              label="Stress"
              hint="How intense the pressure feels right now."
              value={stressScore}
              onChange={setStressScore}
            />
          </div>

          {errorMessage ? (
            <p role="alert" className="rounded-2xl bg-[#f8dfd6] px-4 py-3 text-sm text-[#8c3b2c]">
              {errorMessage}
            </p>
          ) : null}

          <div className="flex flex-wrap items-center justify-between gap-3">
            <p className="text-sm text-stone-500">
              Memory context stays in local storage and helps future check-ins feel more personal.
            </p>
            <button
              type="submit"
              disabled={isSubmitting}
              className="rounded-full bg-[#2d2926] px-5 py-3 text-sm font-semibold text-[#fffaf3] transition hover:bg-[#473f38] disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSubmitting ? "Reflecting..." : "Analyze check-in"}
            </button>
          </div>
        </form>
      </SectionCard>

      <SectionCard
        title="What this flow does"
        description="One structured model call powers the full orchestration pipeline behind the scenes."
      >
        <ol className="space-y-3 text-sm leading-6 text-stone-600">
          <li>Safety prescreen checks for severe distress before any model call.</li>
          <li>Gemini returns one strict JSON response for every pseudo-agent.</li>
          <li>Backend agents normalize safety, milestones, memory, and recommendations.</li>
          <li>The dashboard renders a calm summary with updated local memory.</li>
        </ol>
        <div className="mt-4 rounded-3xl bg-[#f8f1e7] px-4 py-4 text-sm leading-6 text-stone-600">
          <p className="font-medium text-stone-900">Current pressure ecosystem</p>
          <p className="mt-1">
            Primary stressor: {memory.primary_stressor_exam || "not set yet"}
          </p>
          <p className="mt-1">
            Active exams: {memory.active_exams.length > 0 ? memory.active_exams.map((exam) => exam.name).join(", ") : "none yet"}
          </p>
        </div>
      </SectionCard>
    </div>
  );
}
