import Link from "next/link";
import Icon from "@/components/ui/Icon";

const DEFAULT_RECIPES = [
  { name: "Spinach Rescue Bowl", icon: "restaurant_menu", recommendationId: "demo-spinach" },
  { name: "Quick Green Stir Fry", icon: "soup_kitchen", recommendationId: "demo-green" },
  { name: "15-min Protein Plate", icon: "skillet", recommendationId: "demo-protein" },
];

export default function SmartSuggestion({
  title = "No urgent spoilage alerts",
  description = "Scan your fridge to detect expiring ingredients and get rescue recipes.",
  recipes = DEFAULT_RECIPES,
}) {
  return (
    <div className="relative overflow-hidden rounded-2xl border-l-4 border-primary bg-primary/5 p-4">
      <div className="flex items-start gap-4">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary/20 text-primary">
          <Icon name="auto_awesome" />
        </div>
        <div className="flex flex-col gap-1">
          <p className="text-sm font-bold text-slate-900 dark:text-slate-100">
            {title}
          </p>
          <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
            {description}
          </p>
          <div className="mt-3 flex gap-2 overflow-x-auto hide-scrollbar">
            {recipes.map(({ name, icon, recommendationId }) => (
              <Link
                key={`${recommendationId}-${name}`}
                href={`/dashboard/recipes/${recommendationId}`}
                className="flex items-center gap-2 whitespace-nowrap rounded-lg bg-white dark:bg-slate-800 px-3 py-2 text-xs font-semibold shadow-sm border border-primary/10 hover:border-primary/30 hover:bg-primary/5 hover:scale-[1.02] transition-all duration-200 active:scale-95"
              >
                <Icon name={icon || "restaurant_menu"} className="text-sm text-primary" />
                {name}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
