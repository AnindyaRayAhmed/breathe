export function PageHeader() {
  return (
    <div className="flex flex-col items-center gap-4 text-center">
      <img
        src="/logo.svg"
        alt="Breathe logo"
        className="h-12 w-auto sm:h-14"
      />
      <div className="max-w-3xl space-y-3">
        <p className="text-xs uppercase tracking-[0.35em] text-[#9a7452]">Breathe</p>
        <h1 className="font-serif text-3xl tracking-tight text-stone-900 sm:text-5xl">
          A calmer emotional support layer for intense exam seasons
        </h1>
        <p className="mx-auto max-w-2xl text-sm leading-6 text-stone-600 sm:text-base">
          Structured reflection, gentle guidance, and emotionally aware AI for students carrying serious pressure.
        </p>
      </div>
    </div>
  );
}
