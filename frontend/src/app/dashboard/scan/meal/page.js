import Link from "next/link";
import Icon from "@/components/ui/Icon";
import CameraFrame from "@/components/scan/CameraFrame";

export const metadata = {
  title: "Meal Scan - Agentic Dietitian",
};

const MEAL_IMAGE =
  "https://lh3.googleusercontent.com/aida-public/AB6AXuDWB2x_cScu99a1J3BQlTo4N42MQY2XrFESv1Nvl4USC3zUW2P91Ya_S9mdtm8lm58PgW3ATmVRm29imdeW2beUsOiCkKOzLYnt1AKBxHqxHbcipkNwWfQI6HXdKj6u43Nd2g4Gd0i2jX1A3Jmvd828UpDv0edULadLYEfEd1EHYBecbzDqPvPuJWKIjjeWEim9KVGzNOy7tG7b4-a88gvA7YkrubODzMKp29gN5nHyTswZwxvVcbuHZ_aAWqmghzEYygkhSV-ABdH9";

export default function MealScanPage() {
  return (
    <div className="flex flex-1 flex-col gap-6 py-8 px-4">
      <div className="flex flex-col max-w-[480px] flex-1 gap-6 mx-auto w-full">
        <CameraFrame imageUrl={MEAL_IMAGE}>
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute top-6 left-6 w-12 h-12 border-t-4 border-l-4 border-primary rounded-tl-xl opacity-80" />
            <div className="absolute top-6 right-6 w-12 h-12 border-t-4 border-r-4 border-primary rounded-tr-xl opacity-80" />
            <div className="absolute bottom-6 left-6 w-12 h-12 border-b-4 border-l-4 border-primary rounded-bl-xl opacity-80" />
            <div className="absolute bottom-6 right-6 w-12 h-12 border-b-4 border-r-4 border-primary rounded-br-xl opacity-80" />
            <div className="absolute top-1/3 left-0 right-0 h-0.5 bg-primary opacity-50 shadow-[0_0_15px_#4cae4f]" />
            <div className="absolute top-1/4 left-1/4 bg-primary/90 text-white text-[10px] font-bold px-2 py-0.5 rounded backdrop-blur-sm">
              PROTEIN: CHICKEN BREAST 94%
            </div>
            <div className="absolute bottom-1/3 right-1/4 bg-primary/90 text-white text-[10px] font-bold px-2 py-0.5 rounded backdrop-blur-sm">
              FIBER: FRESH GREENS 98%
            </div>
          </div>
        </CameraFrame>
        <div className="flex gap-3">
          <button
            type="button"
            className="flex-1 flex items-center justify-center gap-2 py-4 rounded-xl bg-primary text-white font-bold shadow-lg"
          >
            <Icon name="camera_alt" />
            Confirm & Log Meal
          </button>
          <Link
            href="/dashboard"
            className="flex items-center justify-center rounded-xl bg-slate-200 dark:bg-slate-700 p-4"
            aria-label="Close and return to dashboard"
          >
            <Icon name="close" />
          </Link>
        </div>
      </div>
    </div>
  );
}
