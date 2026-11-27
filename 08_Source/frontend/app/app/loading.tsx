export default function AppLoading() {
  return (
    <div className="grid gap-6" aria-busy="true" aria-live="polite">
      <div>
        <p className="eyebrow">Memuat</p>
        <div className="mt-3 h-8 w-2/3 rounded bg-[var(--rule)]" />
        <div className="mt-3 h-4 w-1/2 rounded bg-[var(--rule)]" />
      </div>
      <div className="sheet h-40 p-6" />
      <div className="sheet h-24 p-6" />
    </div>
  );
}
