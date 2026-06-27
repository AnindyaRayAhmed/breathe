type StatusBadgeProps = {
  label: string;
};

export function StatusBadge({ label }: StatusBadgeProps) {
  return (
    <span className="inline-flex items-center rounded-full border border-[#dbc9b3] bg-[#f6eadb] px-3 py-1 text-xs font-medium tracking-wide text-stone-700">
      {label}
    </span>
  );
}
