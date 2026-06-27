import type {
  HealthResponse,
  JournalAnalysisRequest,
  JournalAnalysisResponse,
  MemoryUpdateRequest,
  MemoryUpdateResponse,
  OnboardingRequest,
  OnboardingResponse,
  WeeklyReflectionRequest,
  WeeklyReflectionResponse,
} from "../types/api";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return (await response.json()) as T;
}

export function getHealth() {
  return request<HealthResponse>("/api/health");
}

export function submitOnboarding(payload: OnboardingRequest) {
  return request<OnboardingResponse>("/api/onboarding", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function submitJournalAnalysis(payload: JournalAnalysisRequest) {
  return request<JournalAnalysisResponse>("/api/journal-analysis", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function submitWeeklyReflection(payload: WeeklyReflectionRequest) {
  return request<WeeklyReflectionResponse>("/api/weekly-reflection", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function submitMemoryUpdate(payload: MemoryUpdateRequest) {
  return request<MemoryUpdateResponse>("/api/memory-update", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
