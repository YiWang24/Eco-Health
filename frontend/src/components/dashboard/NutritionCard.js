// 静态展示用死数据，后续可改为 props 或接口数据
const DEFAULT_CALORIES = { current: 1625, target: 2500, percent: 65 };
const DEFAULT_MACROS = [
  { name: "Protein", value: "85g", color: "bg-blue-500", width: 56 },
  { name: "Carbs", value: "180g", color: "bg-amber-500", width: 72 },
  { name: "Fats", value: "45g", color: "bg-rose-500", width: 64 },
];

export default function NutritionCard({ calories = DEFAULT_CALORIES, macros = DEFAULT_MACROS }) {
  return (
    <div className="rounded-2xl border border-primary/10 bg-white dark:bg-slate-900 p-5 shadow-sm">
      <div className="mb-4 flex items-end justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">Total Calories</p>
          <p className="text-3xl font-black text-primary">
            {calories.current.toLocaleString()}{" "}
            <span className="text-lg font-normal text-slate-400">
              / {calories.target.toLocaleString()} kcal
            </span>
          </p>
        </div>
        <p className="text-sm font-bold text-primary bg-primary/10 px-2 py-1 rounded-lg">
          {calories.percent}% Target
        </p>
      </div>
      <div className="h-3 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
        <div
          className="h-full rounded-full bg-primary transition-all"
          style={{ width: `${calories.percent}%` }}
        />
      </div>
      <div className="mt-6 grid grid-cols-3 gap-4">
        {macros.map(({ name, value, color, width }) => (
          <div key={name} className="flex flex-col gap-2">
            <div className="flex justify-between text-xs font-bold uppercase tracking-wider text-slate-500">
              <span>{name}</span>
              <span>{value}</span>
            </div>
            <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
              <div
                className={`h-full rounded-full ${color}`}
                style={{ width: `${width}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
