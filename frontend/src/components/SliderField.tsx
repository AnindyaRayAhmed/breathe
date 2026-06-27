type SliderFieldProps = {
  id: string;
  label: string;
  hint: string;
  value: number;
  onChange: (value: number) => void;
};

export function SliderField({ id, label, hint, value, onChange }: SliderFieldProps) {
  return (
    <label className="grid gap-2" htmlFor={id}>
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-stone-800">{label}</span>
        <span className="rounded-full bg-[#f1e4d1] px-3 py-1 text-sm font-medium text-stone-700">
          {value}/10
        </span>
      </div>
      <span className="text-sm text-stone-500">{hint}</span>
      <input
        id={id}
        type="range"
        min={1}
        max={10}
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
        className="h-2 w-full cursor-pointer appearance-none rounded-full bg-[#e1d3c1]"
      />
    </label>
  );
}
