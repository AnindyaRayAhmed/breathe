import type { ReactNode } from "react";
import type { PageKey } from "../App";
import { PageHeader } from "../components/PageHeader";

type PageMeta = Record<PageKey, { label: string; description: string }>;

type AppShellProps = {
  activePage: PageKey;
  pages: PageMeta;
  onChangePage: (page: PageKey) => void;
  currentView: ReactNode;
};

export function AppShell({ activePage, pages, onChangePage, currentView }: AppShellProps) {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(214,177,138,0.28),_transparent_38%),linear-gradient(180deg,#f7f1e7_0%,#faf6ef_48%,#f1e8da_100%)] text-stone-900">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:rounded-md focus:bg-stone-900 focus:px-4 focus:py-2 focus:text-[#fffaf3]"
      >
        Skip to content
      </a>
      <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-5 sm:px-6 lg:px-8">
        <header className="mb-6 rounded-[2.25rem] border border-[#eadcc9] bg-[#fffaf3]/92 px-4 py-5 shadow-soft backdrop-blur sm:px-6">
          <PageHeader />
          <nav aria-label="Primary" className="mt-6 flex flex-wrap justify-center gap-2">
            {Object.entries(pages).map(([pageKey, page]) => {
              const key = pageKey as PageKey;
              const isActive = key === activePage;
              return (
                <button
                  key={key}
                  type="button"
                  aria-pressed={isActive}
                  onClick={() => onChangePage(key)}
                  className={[
                    "rounded-full border px-4 py-2 text-left text-sm transition shadow-[0_1px_0_rgba(255,255,255,0.6)]",
                    isActive
                      ? "border-[#c89b73] bg-[#f2e4d3] text-stone-900"
                      : "border-[#eadbca] bg-[#fffcf8] text-stone-700 hover:bg-[#f7efe5]",
                  ].join(" ")}
                >
                  <span className="block font-medium">{page.label}</span>
                  <span className="block text-xs leading-5 text-stone-500">{page.description}</span>
                </button>
              );
            })}
          </nav>
        </header>
        <main id="main-content" className="flex-1 pb-6">
          {currentView}
        </main>
      </div>
    </div>
  );
}
