import Link from "next/link";
import { getRecipeFallbackImage } from "@/utils/recipeImages";

export default function RecipeCard({ title, kcal, time, imageUrl, href }) {
  const safeImage = imageUrl || getRecipeFallbackImage(title);

  const content = (
    <>
      <div
        className="h-32 w-full bg-cover bg-center group-hover:scale-105 transition-transform duration-200"
        style={{ backgroundImage: `url('${safeImage}')` }}
        aria-hidden
      />
      <div className="p-3">
        <h3 className="text-sm font-bold truncate">{title}</h3>
        <p className="text-xs text-slate-500">
          {kcal} kcal • {time}
        </p>
      </div>
    </>
  );

  if (href) {
    return (
      <Link
        href={href}
        className="group block overflow-hidden rounded-2xl bg-white dark:bg-slate-800 shadow-sm border border-slate-100 dark:border-slate-700 hover:shadow-md transition-shadow"
      >
        {content}
      </Link>
    );
  }

  return (
    <div className="group overflow-hidden rounded-2xl bg-white dark:bg-slate-800 shadow-sm border border-slate-100 dark:border-slate-700">
      {content}
    </div>
  );
}
