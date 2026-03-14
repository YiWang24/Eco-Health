import Link from "next/link";
import Button from "@/components/ui/Button";
import { ROUTES } from "@/lib/constants";

export default function HeroSection() {
  return (
    <section className="px-6 lg:px-20 py-12 lg:py-24 max-w-7xl mx-auto">
      <div className="grid lg:grid-cols-2 gap-12 items-center">
        <div className="flex flex-col gap-8 order-2 lg:order-1">
          <div className="flex flex-col gap-4">
            <span className="text-primary font-bold tracking-widest text-xs uppercase bg-primary/10 w-fit px-3 py-1 rounded-full">
              AI-Powered Nutrition
            </span>
            <h1 className="text-slate-900 dark:text-slate-100 text-5xl lg:text-6xl font-black leading-tight tracking-tight">
              Your AI Dietitian that plans meals from{" "}
              <span className="text-primary">what you have.</span>
            </h1>
            <p className="text-slate-600 dark:text-slate-400 text-lg lg:text-xl leading-relaxed max-w-lg">
              Transform your ingredients into healthy, personalized meal plans
              with the power of agentic AI. Stop wondering what&apos;s for
              dinner.
            </p>
          </div>
          <div className="flex flex-wrap gap-4">
            <Button href={ROUTES.onboarding} variant="primaryLarge" size="lg">
              Get Started Free
            </Button>
            <Button variant="outline" size="lg">
              See Demo
            </Button>
          </div>
          <div className="flex items-center gap-4 text-slate-500 dark:text-slate-500 text-sm">
            <div className="flex -space-x-2">
              <div className="w-8 h-8 rounded-full border-2 border-white dark:border-background-dark bg-slate-300" />
              <div className="w-8 h-8 rounded-full border-2 border-white dark:border-background-dark bg-slate-400" />
              <div className="w-8 h-8 rounded-full border-2 border-white dark:border-background-dark bg-slate-500" />
            </div>
            <span>Joined by 5,000+ health enthusiasts</span>
          </div>
        </div>
        <div className="order-1 lg:order-2">
          <div className="relative aspect-square w-full rounded-3xl bg-primary/5 p-4 overflow-hidden border border-primary/10 shadow-2xl">
            <div className="absolute inset-0 bg-gradient-to-tr from-primary/20 to-transparent opacity-50" />
            <div
              className="relative w-full h-full rounded-2xl bg-white dark:bg-slate-900 shadow-inner flex items-center justify-center bg-cover bg-center"
              style={{
                backgroundImage: `url("https://lh3.googleusercontent.com/aida-public/AB6AXuAyA2qLza7BS_4AMh0s3FxvWwj-93X6kigRLx3joK5csXzw1UHi2wsNVX9LklQTv8PLW6ENBKXoYAbZWjI1GVaQw6bUvHTF4w1r3kx0gAIzj-ai7s79c4GgOZjaJD7MpGtc6VCFMnbLD3vZvluR_xYtIdphZCBzLvuFYSvAlhvJYZrXEuT3njwc17RRPRidSi1uhNoSx2vtGCIn6fOFxvn5zW8HmWzF3v-UTNfOHrQSFpF3CaxchSx56aeZJm3RdwzSi9l_k4kD4z0P")`,
              }}
              aria-hidden
            >
              <div className="absolute top-4 right-4 bg-white/90 dark:bg-slate-800/90 p-4 rounded-xl shadow-lg border border-primary/20 backdrop-blur">
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined text-primary">
                    nutrition
                  </span>
                  <div>
                    <div className="text-[10px] text-slate-500 font-bold uppercase">
                      Daily Goal
                    </div>
                    <div className="text-sm font-bold text-slate-900 dark:text-slate-100">
                      85% Complete
                    </div>
                  </div>
                </div>
              </div>
              <div className="absolute bottom-4 left-4 right-4 bg-primary p-4 rounded-xl shadow-lg text-white">
                <div className="flex items-center gap-3">
                  <span className="material-symbols-outlined">
                    chip_extraction
                  </span>
                  <span className="text-sm font-medium">
                    Found: 12 recipes using your current stock
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
