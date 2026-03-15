import Link from "next/link";
import Icon from "@/components/ui/Icon";
import { APP_NAME, ROUTES } from "@/lib/constants";

export default function Header({ variant = "welcome" }) {
  if (variant === "welcome") {
    return (
      <header className="flex items-center justify-between border-b border-primary/10 px-6 py-4 lg:px-20 bg-white/80 dark:bg-background-dark/80 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <div className="text-primary">
            <Icon name="auto_awesome" className="text-3xl" />
          </div>
          <h2 className="text-slate-900 dark:text-slate-100 text-xl font-bold tracking-tight">
            {APP_NAME}
          </h2>
        </div>
        <nav className="hidden md:flex items-center gap-8">
          <a
            href="#features"
            className="text-slate-600 dark:text-slate-400 text-sm font-medium hover:text-primary transition-colors"
          >
            Features
          </a>
          <a
            href="#"
            className="text-slate-600 dark:text-slate-400 text-sm font-medium hover:text-primary transition-colors"
          >
            How it Works
          </a>
          <a
            href="#"
            className="text-slate-600 dark:text-slate-400 text-sm font-medium hover:text-primary transition-colors"
          >
            Pricing
          </a>
        </nav>
        <div className="flex gap-3">
          <Link
            href={`${ROUTES.auth}?mode=login`}
            className="hidden sm:flex min-w-[84px] cursor-pointer items-center justify-center rounded-lg h-10 px-4 bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm font-bold hover:bg-slate-200 transition-colors"
            aria-label="Go to login"
          >
            Log In
          </Link>
          <Link
            href={`${ROUTES.auth}?mode=register`}
            className="flex min-w-[84px] cursor-pointer items-center justify-center rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold shadow-lg shadow-primary/20 hover:opacity-90 transition-all"
          >
            Sign Up
          </Link>
        </div>
      </header>
    );
  }

  // Dashboard variant
  return (
    <header className="sticky top-0 z-50 flex items-center justify-between border-b border-primary/10 bg-background-light/80 dark:bg-background-dark/80 px-6 py-4 backdrop-blur-md">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-white">
          <Icon name="nutrition" className="text-2xl" />
        </div>
        <Link href={ROUTES.dashboard}>
          <h1 className="text-xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            {APP_NAME}
          </h1>
        </Link>
      </div>
      <div className="flex items-center gap-4">
        <button
          type="button"
          className="relative flex h-10 w-10 items-center justify-center rounded-full bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400"
          aria-label="Notifications"
        >
          <Icon name="notifications" />
          <span className="absolute right-2.5 top-2.5 flex h-2 w-2 rounded-full bg-primary" aria-hidden />
        </button>
        <Link
          href={ROUTES.profile}
          className="h-10 w-10 rounded-full border-2 border-primary bg-cover bg-center block"
          style={{
            backgroundImage:
              "url('https://lh3.googleusercontent.com/aida-public/AB6AXuAk5van6JcyYxc9_oqse1l8LOBCwmLiQpx1Kb05SIwwSuZinAnlfycgO2bnhqwmsdu8-TxNUWlJHpZISWRAyfrkT6YcqoWYmYcbmtpEW3JzlAToUud6LJEEAzBEc-XPvxDrzImRixgg07Tgkuj1fnZ_72qnh2XMyzkWfU-86J1enwkPqodKi2xjoBMcIHV5pbjsPMPl2clHGYU3AkZVJqoTx4i2nM9yirsOyRCd_EYj6sG8d6ibw3UoafaV5PDM5JHiLvXFoRpjIXik')",
          }}
          aria-label="Go to profile"
        />
      </div>
    </header>
  );
}
