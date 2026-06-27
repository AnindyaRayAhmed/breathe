import { startTransition, useEffect, useState } from "react";
import { useDocumentTitle } from "./hooks/useDocumentTitle";
import { useLocalStorage } from "./hooks/useLocalStorage";
import { AppShell } from "./layouts/AppShell";
import { DailyCheckInPage } from "./pages/DailyCheckInPage";
import { JourneyTimelinePage } from "./pages/JourneyTimelinePage";
import { OnboardingPage } from "./pages/OnboardingPage";
import { ReflectionDashboardPage } from "./pages/ReflectionDashboardPage";
import { WeeklyInsightsPage } from "./pages/WeeklyInsightsPage";
import type { JournalAnalysisResponse, MemorySnapshot } from "./types/api";

export type PageKey =
  | "onboarding"
  | "checkin"
  | "dashboard"
  | "weekly"
  | "timeline";

const pages: Record<PageKey, { label: string; description: string }> = {
  onboarding: { label: "Onboarding", description: "Set intent and support style." },
  checkin: { label: "Daily Check-In", description: "Log the day with emotional context." },
  dashboard: { label: "Reflection Dashboard", description: "See the latest AI-guided reflection." },
  weekly: { label: "Weekly Insights", description: "Review the week's patterns." },
  timeline: { label: "Journey Timeline", description: "View milestone moments over time." },
};

const initialMemory: MemorySnapshot = {
  active_exams: [
    { name: "JEE", priority: "high", exam_date: "2026-01-15" },
    { name: "BITSAT", priority: "medium", exam_date: "2026-05-20" },
  ],
  primary_stressor_exam: "JEE",
  study_phase: "revision",
  stress_triggers: ["mock tests late at night", "score comparison after review sessions"],
  motivation_sources: ["wanting a calmer home atmosphere", "seeing small progress add up"],
  recurring_patterns: ["self-criticism rises after mock tests", "stress spikes closer to revision deadlines"],
  coping_preferences: ["short breathing breaks", "writing one honest line before study"],
  milestone_history: [
    {
      event_type: "confidence rebound",
      title: "Recovered after a hard mock test week",
      severity_score: 6,
      occurred_at: "2026-05-18T08:00:00Z",
      exam_name: "JEE",
    },
    {
      event_type: "consistency streak",
      title: "Kept returning to reflection",
      severity_score: 4,
      occurred_at: "2026-05-21T08:00:00Z",
      exam_name: "BITSAT",
    },
  ],
  emotional_trends: [
    "pressure rises before mock test weeks",
    "recovery improves after short grounding pauses",
  ],
};

export default function App() {
  const [memory, setMemory] = useLocalStorage<MemorySnapshot>("breathe-memory", initialMemory);
  const [activePage, setActivePage] = useState<PageKey>("onboarding");
  const [latestResult, setLatestResult] = useLocalStorage<JournalAnalysisResponse | null>("breathe-latest-checkin", null);

  useDocumentTitle("Breathe");

  useEffect(() => {
    if (latestResult?.updated_memory) {
      setMemory(latestResult.updated_memory);
    }
  }, [latestResult, setMemory]);

  useEffect(() => {
    if (latestResult) {
      setActivePage("dashboard");
    }
  }, [latestResult]);

  function handleCheckInComplete(response: JournalAnalysisResponse) {
    startTransition(() => {
      setLatestResult(response);
      setMemory(response.updated_memory);
      setActivePage("dashboard");
    });
  }

  function handleOnboardingComplete(nextMemory: MemorySnapshot) {
    startTransition(() => {
      setMemory(nextMemory);
      setActivePage("checkin");
    });
  }

  const renderCurrentView = () => {
    switch (activePage) {
      case "onboarding":
        return <OnboardingPage memory={memory} onComplete={handleOnboardingComplete} />;
      case "checkin":
        return <DailyCheckInPage memory={memory} onComplete={handleCheckInComplete} />;
      case "dashboard":
        return <ReflectionDashboardPage result={latestResult} memory={memory} />;
      case "weekly":
        return <WeeklyInsightsPage />;
      case "timeline":
        return <JourneyTimelinePage />;
      default:
        return null;
    }
  };

  return (
    <AppShell
      activePage={activePage}
      pages={pages}
      onChangePage={setActivePage}
      currentView={renderCurrentView()}
    />
  );
}
