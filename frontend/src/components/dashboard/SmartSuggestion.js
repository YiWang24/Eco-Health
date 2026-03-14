import Link from "next/link";
import Icon from "@/components/ui/Icon";

const recipes = [
  { name: "Spinach Salad", icon: "restaurant_menu", slug: "spinach-salad" },
  { name: "Green Smoothie", icon: "soup_kitchen", slug: "green-smoothie" },
  { name: "Sauteed Greens", icon: "skillet", slug: "sauteed-greens" },
];

export default function SmartSuggestion() {
  return (
    <div className="relative overflow-hidden rounded-2xl border-l-4 border-primary bg-primary/5 p-4">
      <div className="flex items-start gap-4">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary/20 text-primary">
          <Icon name="auto_awesome" />
        </div>
        <div className="flex flex-col gap-1">
          <p className="text-sm font-bold text-slate-900 dark:text-slate-100">
            Your spinach will expire tomorrow!
          </p>
          <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
            Let&apos;s avoid waste. Here are 3 recipes you can make tonight
            using spinach and chicken.
          </p>
          <div className="mt-3 flex gap-2 overflow-x-auto hide-scrollbar">
            {recipes.map(({ name, icon, slug }) => (
              <Link
                key={name}
                href={`/dashboard/recipes/${slug}`}
                className="flex items-center gap-2 whitespace-nowrap rounded-lg bg-white dark:bg-slate-800 px-3 py-2 text-xs font-semibold shadow-sm border border-primary/10 hover:border-primary/30 hover:bg-primary/5 hover:scale-[1.02] transition-all duration-200 active:scale-95"
              >
                <Icon name={icon} className="text-sm text-primary" />
                {name}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
