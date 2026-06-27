import { SectionCard } from "../components/SectionCard";

export function JourneyTimelinePage() {
  return (
    <SectionCard
      title="Journey Timeline"
      description="A milestone view for emotionally meaningful events across the preparation journey."
    >
      <ol className="space-y-4 text-sm leading-6 text-stone-600">
        <li className="rounded-2xl bg-[#f8f1e7] p-4">Start of preparation</li>
        <li className="rounded-2xl bg-[#f8f1e7] p-4">First high-pressure week</li>
        <li className="rounded-2xl bg-[#f8f1e7] p-4">Recovery and reset milestones</li>
      </ol>
    </SectionCard>
  );
}
