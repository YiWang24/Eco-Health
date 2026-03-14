export default function ProgressStepper({ step = 1, totalSteps = 4 }) {
  const percent = (step / totalSteps) * 100;
  return (
    <div className="flex flex-col gap-4 mb-10 px-4">
      <div className="flex gap-6 justify-between items-center">
        <span className="bg-primary/10 text-primary px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          Step {step} of {totalSteps}
        </span>
        <p className="text-slate-500 dark:text-slate-400 text-sm font-medium">
          Profile Construction: {Math.round(percent)}% Complete
        </p>
      </div>
      <div className="w-full h-3 rounded-full bg-slate-200 dark:bg-slate-800 overflow-hidden">
        <div
          className="h-full bg-primary rounded-full transition-all duration-300"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
