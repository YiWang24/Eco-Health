import Icon from "@/components/ui/Icon";
import { APP_NAME } from "@/lib/constants";

export default function Footer() {
  return (
    <footer className="px-6 lg:px-20 py-12 border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-background-dark">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
        <div className="flex items-center gap-2">
          <div className="text-primary">
            <Icon name="auto_awesome" className="text-2xl" />
          </div>
          <h2 className="text-slate-900 dark:text-slate-100 text-lg font-bold">
            {APP_NAME}
          </h2>
        </div>
        <div className="flex flex-wrap items-center justify-center gap-8">
          <a
            href="#"
            className="text-slate-500 dark:text-slate-400 text-sm hover:text-primary transition-colors"
          >
            Privacy Policy
          </a>
          <a
            href="#"
            className="text-slate-500 dark:text-slate-400 text-sm hover:text-primary transition-colors"
          >
            Terms of Service
          </a>
          <a
            href="#"
            className="text-slate-500 dark:text-slate-400 text-sm hover:text-primary transition-colors"
          >
            Contact
          </a>
        </div>
        <p className="text-slate-400 text-sm">© 2024 Agentic Personal Dietitian.</p>
      </div>
    </footer>
  );
}
