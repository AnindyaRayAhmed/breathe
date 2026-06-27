import { SectionCard } from "../components/SectionCard";

export function WeeklyInsightsPage() {
  return (
    <SectionCard
      title="Weekly Insights"
      description="A weekly summary surface for trends, milestones, and support suggestions."
    >
      <p className="max-w-2xl text-sm leading-6 text-stone-600">
        This page is intentionally minimal for now. It will later display a model-assisted reflection summary, milestone moments, and practical next steps.
      </p>
    </SectionCard>
  );
}
