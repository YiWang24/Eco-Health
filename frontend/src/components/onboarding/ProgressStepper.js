const DEFAULT_STEP_LABELS = ["Fill Form", "Complete"];

export default function ProgressStepper({ step = 1, totalSteps = 2, labels = DEFAULT_STEP_LABELS }) {
  const safeStep = Math.min(Math.max(step, 1), totalSteps);
  const visibleLabels =
    Array.isArray(labels) && labels.length === totalSteps
      ? labels
      : Array.from({ length: totalSteps }, (_, index) => `Step ${index + 1}`);

  return (
    <div className="flex flex-col gap-4 mb-10 px-4">
      <div className="flex gap-6 justify-between items-center">
        <span className="bg-primary/10 text-primary px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          Step {safeStep} of {totalSteps}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {visibleLabels.map((label, index) => {
          const active = index + 1 <= safeStep;
          return (
            <div
              key={label}
              className={`rounded-xl border px-3 py-2 text-xs font-semibold uppercase tracking-wide text-center ${
                active
                  ? "bg-primary text-white border-primary"
                  : "bg-slate-100 text-slate-500 border-slate-200"
              }`}
            >
              {label}
            </div>
          );
        })}
      </div>
    </div>
  );
}
