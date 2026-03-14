"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Icon from "@/components/ui/Icon";
import { ROUTES } from "@/lib/constants";

const items = [
  { href: ROUTES.dashboard, label: "Home", icon: "home" },
  { href: ROUTES.scanFridge, label: "Scan", icon: "qr_code_scanner" },
  { href: ROUTES.chat, label: "Chat", icon: "chat_bubble" },
  { href: ROUTES.recipes, label: "Recipes", icon: "menu_book" },
  { href: ROUTES.profile, label: "Profile", icon: "account_circle" },
];

export default function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 z-50 flex w-full justify-center bg-white/90 dark:bg-slate-900/90 px-4 py-3 backdrop-blur-lg border-t border-slate-200 dark:border-slate-800">
      <div className="flex w-full max-w-[640px] items-center justify-between">
        {items.map(({ href, label, icon }) => {
          const isActive = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              aria-label={label}
              className={`flex flex-col items-center gap-1 ${
                isActive ? "text-primary" : "text-slate-400 hover:text-primary"
              }`}
            >
              <Icon
                name={icon}
                className={isActive ? "font-variation-fill" : ""}
              />
              <span className="text-[10px] font-bold">{label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
