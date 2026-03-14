import Link from "next/link";
import Icon from "@/components/ui/Icon";

export const metadata = {
  title: "LiveLarder - Agentic Dietitian",
};

const FRIDGE_IMAGE =
  "https://lh3.googleusercontent.com/aida-public/AB6AXuDLgYvJbKOw6jSOoW8hpqd4W0uEfNL_sOuOnL8qfZf5wg4-FSNN3pq81nE50AnNnPaVBeAy4SUe7qlYeOd2kIeQYqtymDaZ7hlb05cSF3xXacpMZTXcR_w7WoENljvIWDkbZ5bUC3u4YFUZhBDZ5ojLYJkvAREjBpItluqiE5Ar-13GcxSQOsnTttEhvJMPBnZvu2QvOGOEol9fxXZbsLC2a07dSJWJiGbTUtDMCsDAYQFa_ZgupJPG9OioKTGp3fs1EJMmYDRmUQxr";

export default function LivelarderPage() {
  return (
    <div className="max-w-[1200px] mx-auto flex flex-1 flex-col gap-8 py-8 px-4 w-full">
      <nav className="flex items-center gap-6 border-b border-primary/5 pb-2">
        <span className="text-primary border-b-2 border-primary pb-2 font-semibold text-sm flex items-center gap-2">
          <Icon name="visibility" className="text-sm" /> LiveLarder
        </span>
        <Link
          href="#"
          className="text-slate-500 dark:text-slate-400 pb-2 font-medium text-sm flex items-center gap-2 hover:text-primary transition-colors"
        >
          <Icon name="inventory_2" className="text-sm" /> Inventory
        </Link>
        <Link
          href="#"
          className="text-slate-500 dark:text-slate-400 pb-2 font-medium text-sm flex items-center gap-2 hover:text-primary transition-colors"
        >
          <Icon name="menu_book" className="text-sm" /> Recipes
        </Link>
      </nav>
      <div className="relative group">
        <div className="relative aspect-[16/9] w-full overflow-hidden rounded-xl bg-slate-200 dark:bg-slate-800 shadow-2xl">
          <div
            className="absolute inset-0 bg-cover bg-center"
            style={{ backgroundImage: `url("${FRIDGE_IMAGE}")` }}
          />
          <div className="absolute inset-0 bg-primary/5 mix-blend-overlay backdrop-blur-[1px]" />
          {/* Overlays */}
          <div className="absolute top-[15%] left-[25%] w-32 h-40">
            <div className="absolute inset-0 border-2 border-red-500 rounded bg-red-500/10 backdrop-blur-[2px] shadow-[0_0_15px_rgba(239,68,68,0.5)]" />
            <div className="absolute -top-10 left-0 bg-red-600 text-white px-3 py-1.5 rounded-t-lg flex flex-col min-w-[140px]">
              <div className="flex items-center gap-1">
                <span className="text-xs">⏰</span>
                <span className="text-[10px] font-black uppercase tracking-wider">
                  Critical
                </span>
              </div>
              <div className="text-[11px] font-bold">
                Spinach: Expiring Tomorrow
              </div>
              <div className="text-[9px] font-medium opacity-90 italic mt-0.5">
                Status: Opened
              </div>
            </div>
          </div>
          <div className="absolute bottom-[20%] left-[20%] w-24 h-24">
            <div className="absolute inset-0 border-2 border-orange-400 rounded bg-orange-400/10 backdrop-blur-[1px]" />
            <div className="absolute -top-10 left-0 bg-orange-500 text-white px-3 py-1.5 rounded-t-lg flex flex-col min-w-[100px]">
              <div className="text-[11px] font-bold">Eggs: Eat Soon</div>
              <div className="text-[9px] font-medium opacity-90 italic">
                Status: Sealed
              </div>
            </div>
          </div>
          <div className="absolute bottom-[25%] right-[25%] w-28 h-20">
            <div className="absolute inset-0 border-2 border-primary rounded bg-primary/10 backdrop-blur-[1px]" />
            <div className="absolute -top-10 left-0 bg-primary text-white px-3 py-1.5 rounded-t-lg flex flex-col min-w-[100px]">
              <div className="text-[11px] font-bold">Greek Yogurt</div>
              <div className="text-[9px] font-medium opacity-90 italic">
                Status: Sealed
              </div>
            </div>
          </div>
          <div className="absolute inset-0 p-6 flex flex-col justify-between pointer-events-none">
            <div className="flex justify-between items-start">
              <div className="bg-black/70 backdrop-blur-xl text-white text-[10px] uppercase tracking-[0.2em] px-3 py-1.5 rounded border border-white/20 flex items-center gap-2">
                <span className="size-2 bg-primary rounded-full animate-pulse" />
                Digital Twin Stream Active
              </div>
              <div className="flex gap-2 pointer-events-auto">
                <button
                  type="button"
                  className="bg-black/40 backdrop-blur-md text-white/90 px-3 py-1.5 rounded border border-white/20 text-[10px] font-bold uppercase tracking-wider flex items-center gap-2 hover:bg-black/60 transition-all"
                >
                  <Icon name="recenter" className="text-sm" />
                  Recalibrate
                </button>
              </div>
            </div>
            <div className="flex justify-center gap-4 pointer-events-auto">
              <button
                type="button"
                className="bg-white/20 backdrop-blur-2xl border border-white/30 text-white rounded-full size-12 flex items-center justify-center hover:bg-white/40 transition-all"
              >
                <Icon name="layers" />
              </button>
              <button
                type="button"
                className="bg-primary text-white px-10 py-4 rounded-full font-bold shadow-[0_0_30px_rgba(76,174,79,0.4)] flex items-center gap-3 hover:scale-105 transition-all"
              >
                <Icon name="sync_alt" />
                Update Inventory
              </button>
              <button
                type="button"
                className="bg-white/20 backdrop-blur-2xl border border-white/30 text-white rounded-full size-12 flex items-center justify-center hover:bg-white/40 transition-all"
              >
                <Icon name="info" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
