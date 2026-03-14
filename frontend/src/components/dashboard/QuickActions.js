import Link from "next/link";
import Icon from "@/components/ui/Icon";
import { ROUTES } from "@/lib/constants";

const actions = [
  { href: ROUTES.scanFridge, label: "Scan Fridge", icon: "kitchen", primary: true },
  { href: ROUTES.scanMeal, label: "Scan Meal", icon: "photo_camera", primary: false },
  { href: ROUTES.scanReceipt, label: "Scan Receipt", icon: "receipt", primary: false },
  { href: ROUTES.chat, label: "Ask AI", icon: "smart_toy", primary: false },
];

export default function QuickActions() {
  return (
    <section className="grid gap-3 grid-cols-4">
      {actions.map(({ href, label, icon, primary }) => (
        <Link
          key={href}
          href={href}
          className={`flex flex-col items-center justify-center gap-2 rounded-2xl p-4 shadow-sm border transition-all duration-200 active:scale-95 ${
            primary
              ? "bg-primary text-white shadow-lg shadow-primary/20 border-primary hover:opacity-90 hover:scale-[1.02]"
              : "bg-white dark:bg-slate-800 text-slate-900 dark:text-white border-slate-100 dark:border-slate-700 hover:border-primary/30 hover:bg-primary/5 hover:scale-[1.02]"
          }`}
        >
          <Icon
            name={icon}
            className={`text-3xl ${!primary ? "text-primary" : ""}`}
          />
          <span className="text-xs font-bold">{label}</span>
        </Link>
      ))}
    </section>
  );
}
