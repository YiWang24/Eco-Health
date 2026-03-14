import Link from "next/link";
import Icon from "@/components/ui/Icon";

export const metadata = {
  title: "Profile - Agentic Dietitian",
};

export default function ProfilePage() {
  return (
    <div className="mx-auto w-full max-w-[640px] flex flex-col gap-6 py-8 px-4">
      <h1 className="text-2xl font-black tracking-tight">Profile</h1>

      <Link
        href="/onboarding"
        className="flex items-center gap-4 p-4 rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 shadow-sm hover:border-primary/30 hover:bg-primary/5 transition-colors"
      >
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <Icon name="person" className="text-2xl" />
        </div>
        <div className="flex-1 text-left">
          <p className="font-bold text-slate-900 dark:text-slate-100">
            Personal info & nutrition profile
          </p>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Age, goals, dietary preferences, allergies
          </p>
        </div>
        <Icon name="chevron_right" className="text-slate-400" />
      </Link>

      <div className="flex flex-col items-center justify-center py-12 rounded-2xl border-2 border-dashed border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/30 text-center">
        <Icon name="settings" className="text-4xl text-slate-300 dark:text-slate-600 mb-3" />
        <p className="text-slate-600 dark:text-slate-400 font-medium text-sm">
          More profile and account settings will appear here after login is
          connected.
        </p>
      </div>
    </div>
  );
}
