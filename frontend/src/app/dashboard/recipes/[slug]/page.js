import Link from "next/link";
import Icon from "@/components/ui/Icon";

export async function generateMetadata({ params }) {
  const title = decodeURIComponent(params.slug || "").replace(/-/g, " ");
  return { title: `${title} - Recipe - Agentic Dietitian` };
}

export default function RecipeDetailPage({ params }) {
  const slug = params.slug || "";
  const title = decodeURIComponent(slug).replace(/-/g, " ");

  return (
    <div className="mx-auto w-full max-w-[640px] flex flex-col gap-6 py-8 px-4">
      <Link
        href="/dashboard/recipes"
        className="inline-flex items-center gap-2 text-sm font-medium text-primary hover:underline w-fit"
      >
        <Icon name="arrow_back" className="text-lg" />
        Back to Recipes
      </Link>
      <h1 className="text-2xl font-black tracking-tight capitalize">
        {title}
      </h1>
      <div className="rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-6">
        <p className="text-slate-600 dark:text-slate-400">
          Recipe details and steps will be loaded here after connecting to the
          backend.
        </p>
      </div>
    </div>
  );
}
