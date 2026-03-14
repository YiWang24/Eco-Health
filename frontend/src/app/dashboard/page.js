import Link from "next/link";
import NutritionCard from "@/components/dashboard/NutritionCard";
import QuickActions from "@/components/dashboard/QuickActions";
import SmartSuggestion from "@/components/dashboard/SmartSuggestion";
import RecipeCard from "@/components/dashboard/RecipeCard";
import EmptyState from "@/components/ui/EmptyState";

export const metadata = {
  title: "Dashboard - Agentic Dietitian",
};

const recommendedRecipes = [
  {
    title: "Mediterranean Bowl",
    kcal: "450",
    time: "20m",
    slug: "mediterranean-bowl",
    imageUrl:
      "https://lh3.googleusercontent.com/aida-public/AB6AXuB-ycXDahb11ZiwREUq2iX5NEsug3ybaK0P7i4MgA5PEIUzlSq1BKEIwBy70GhxoerUU54WM3c0ZaGHA7By5Gdn4E46D2Jj51ya7SQo22hvUCOwm2l1GBRV8HW6bT6Dt1iM5wRSntijOdaLBG-JmCqGziBVDpFsprmx4qbOVoZ2jtj29kFo3Kg9pQLKA4R7_W0hCG1Rxtl9S_ANRSWkIbSgadwK_pAIPgm1C3lvwyA5krdUB4aSshlHY0aja8fBv2a7HFNg0LH-cV6Q",
  },
  {
    title: "Avocado & Egg Toast",
    kcal: "320",
    time: "10m",
    slug: "avocado-egg-toast",
    imageUrl:
      "https://lh3.googleusercontent.com/aida-public/AB6AXuAEx89ZHQpAq8TBf-1ajm42D0PdXij7mP5uz76pZ47_Xv5EHLyh4WVTDX0nd5HVls6-jhEkaTnimj6yvaHitYqbn6prsiFkwiY8vSnwNvTJxnQBPp-UnEvcxnemushsNJzLF9FIRmDh6ZOsH4LJzQQrdG_PBKMHYpSQteBI62DrXhZN71QqNLfHhU_MFiTPWXxSAdgXDKx0fZvWjjN_csLh-uhbEg0XNVMHGbXPGLBM2jN64fDcGGTaBRcE0Csyar9-n0zFzHUXceCc",
  },
];

export default function DashboardPage() {
  return (
    <div className="mx-auto w-full max-w-[640px] flex flex-col gap-6">
      <section className="flex flex-col gap-2">
        <h2 className="text-2xl font-black tracking-tight">
          Today&apos;s Nutrition
        </h2>
        <NutritionCard />
      </section>
      <QuickActions />
      <section className="flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold">Smart Suggestions</h2>
          <Link
            href="/dashboard/recipes"
            className="text-sm font-medium text-primary hover:underline"
          >
            View All
          </Link>
        </div>
        <SmartSuggestion />
      </section>
      <section className="flex flex-col gap-4">
        <h2 className="text-lg font-bold">Recommended for You</h2>
        {recommendedRecipes.length === 0 ? (
          <EmptyState
            icon="restaurant"
            title="No recommendations yet"
            description="Scan your fridge or ask in Chat to get personalized recipe ideas."
            action={
              <Link
                href="/dashboard/scan/fridge"
                className="text-primary font-semibold text-sm hover:underline"
              >
                Scan Fridge
              </Link>
            }
          />
        ) : (
          <div className="grid grid-cols-2 gap-4">
            {recommendedRecipes.map((recipe) => (
              <RecipeCard
                key={recipe.title}
                {...recipe}
                href={`/dashboard/recipes/${recipe.slug}`}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
