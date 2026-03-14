import Icon from "@/components/ui/Icon";

export const metadata = {
  title: "Recipes - Agentic Dietitian",
};

export default function RecipesPage() {
  return (
    <div className="mx-auto w-full max-w-[640px] flex flex-col gap-6 py-8 px-4">
      <h1 className="text-2xl font-black tracking-tight">Recipes</h1>
      <div className="flex flex-col items-center justify-center py-16 rounded-2xl border-2 border-dashed border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/30 text-center">
        <Icon name="menu_book" className="text-5xl text-slate-300 dark:text-slate-600 mb-4" />
        <p className="text-slate-600 dark:text-slate-400 font-medium">
          Recipe recommendations will appear here after you chat with your AI
          dietitian or scan your fridge.
        </p>
        <p className="text-sm text-slate-500 dark:text-slate-500 mt-2">
          Go to Chat or Scan to get started.
        </p>
      </div>
    </div>
  );
}
