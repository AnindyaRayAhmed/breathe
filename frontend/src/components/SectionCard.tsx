import type { ReactNode } from "react";

type SectionCardProps = {
  title: string;
  description: string;
  children: ReactNode;
  className?: string;
};

export function SectionCard({ title, description, children, className }: SectionCardProps) {
  return (
    <section className={["rounded-[2rem] border border-[#eadccc] bg-[#fffdf8] p-5 shadow-soft", className].filter(Boolean).join(" ")}>
      <header className="mb-4 space-y-1">
        <h2 className="font-serif text-xl tracking-tight text-stone-900 sm:text-[1.35rem]">{title}</h2>
        <p className="text-sm leading-6 text-stone-500">{description}</p>
      </header>
      {children}
    </section>
  );
}
