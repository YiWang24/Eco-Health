import Link from "next/link";
import Icon from "@/components/ui/Icon";
import ProgressStepper from "@/components/onboarding/ProgressStepper";

export default function OnboardingPage() {
  return (
    <div className="layout-content-container flex flex-col max-w-4xl w-full">
      <ProgressStepper step={1} totalSteps={4} />

            <div className="bg-white dark:bg-slate-900 shadow-sm border border-primary/5 rounded-xl overflow-hidden">
              {/* Section 1: Personal Info */}
              <div className="p-8 border-b border-slate-100 dark:border-slate-800">
                <div className="flex items-center gap-3 mb-6">
                  <Icon name="person" className="text-primary" />
                  <h3 className="text-2xl font-bold">Tell us about yourself</h3>
                </div>
                <p className="text-slate-500 dark:text-slate-400 mb-8">
                  This data helps our AI calculate your BMR and TDEE.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <label className="flex flex-col gap-2" htmlFor="onboarding-age">
                    <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      Age
                    </span>
                    <input
                      id="onboarding-age"
                      type="number"
                      placeholder="e.g. 28"
                      className="rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 focus:ring-primary focus:border-primary p-3"
                    />
                  </label>
                  <label className="flex flex-col gap-2" htmlFor="onboarding-sex">
                    <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      Biological Sex
                    </span>
                    <select id="onboarding-sex" className="rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 focus:ring-primary focus:border-primary p-3">
                      <option>Male</option>
                      <option>Female</option>
                      <option>Other</option>
                      <option>Prefer not to say</option>
                    </select>
                  </label>
                  <label className="flex flex-col gap-2">
                    <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      Height (cm)
                    </span>
                    <input
                      type="number"
                      placeholder="175"
                      className="rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 focus:ring-primary focus:border-primary p-3"
                    />
                  </label>
                  <label className="flex flex-col gap-2">
                    <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      Current Weight (kg)
                    </span>
                    <input
                      type="number"
                      placeholder="72"
                      className="rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 focus:ring-primary focus:border-primary p-3"
                    />
                  </label>
                  <label className="flex flex-col gap-2 md:col-span-2">
                    <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      Activity Level
                    </span>
                    <select className="rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 focus:ring-primary focus:border-primary p-3">
                      <option>Sedentary (Office job, little exercise)</option>
                      <option>Lightly Active (1-2 days/week)</option>
                      <option>Moderately Active (3-5 days/week)</option>
                      <option>Very Active (6-7 days/week)</option>
                      <option>Extra Active (Physical job + intense training)</option>
                    </select>
                  </label>
                </div>
              </div>

              {/* Section 2: Health Goals */}
              <div className="p-8 border-b border-slate-100 dark:border-slate-800">
                <div className="flex items-center gap-3 mb-6">
                  <Icon name="target" className="text-primary" />
                  <h3 className="text-2xl font-bold">Health Goals</h3>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {[
                    {
                      icon: "trending_down",
                      title: "Lose Weight",
                      sub: "Fat loss focus",
                    },
                    {
                      icon: "fitness_center",
                      title: "Gain Muscle",
                      sub: "Hypertrophy & strength",
                    },
                    {
                      icon: "balance",
                      title: "Maintenance",
                      sub: "Stability & health",
                    },
                  ].map(({ icon, title, sub }) => (
                    <label
                      key={title}
                      className="relative flex flex-col p-4 border-2 border-slate-100 dark:border-slate-800 rounded-xl cursor-pointer hover:border-primary/50 transition-all has-[:checked]:border-primary has-[:checked]:bg-primary/5"
                    >
                      <input
                        type="radio"
                        name="goal"
                        defaultChecked={title === "Lose Weight"}
                        className="absolute right-4 top-4 text-primary focus:ring-primary"
                      />
                      <Icon name={icon} className="text-primary mb-2" />
                      <span className="font-bold">{title}</span>
                      <span className="text-xs text-slate-500">{sub}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Section 3: Dietary Preferences */}
              <div className="p-8 border-b border-slate-100 dark:border-slate-800">
                <div className="flex items-center gap-3 mb-6">
                  <Icon name="restaurant" className="text-primary" />
                  <h3 className="text-2xl font-bold">Dietary Preferences</h3>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div>
                    <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-4">
                      Diet Type
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {["Vegetarian", "Vegan", "Keto", "Paleo", "No Restrictions"].map(
                        (diet) => (
                          <button
                            key={diet}
                            type="button"
                            className={`px-4 py-2 rounded-full border transition-colors ${
                              diet === "No Restrictions"
                                ? "bg-primary text-white border-primary"
                                : "border-slate-200 dark:border-slate-700 hover:bg-primary hover:text-white"
                            }`}
                          >
                            {diet}
                          </button>
                        )
                      )}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-4">
                      Allergies & Restrictions
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {["Dairy-Free", "Gluten-Free", "Nut-Free", "Shellfish"].map(
                        (item) => (
                          <label
                            key={item}
                            className="flex items-center gap-2 px-3 py-1 bg-slate-100 dark:bg-slate-800 rounded-md text-sm"
                          >
                            <input
                              type="checkbox"
                              className="rounded text-primary focus:ring-primary"
                            />
                            {item}
                          </label>
                        )
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Section 4: Lifestyle */}
              <div className="p-8">
                <div className="flex items-center gap-3 mb-6">
                  <Icon name="schedule" className="text-primary" />
                  <h3 className="text-2xl font-bold">Lifestyle & Logistics</h3>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <label className="flex flex-col gap-2">
                    <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      Max Cooking Time (mins/meal)
                    </span>
                    <input
                      type="range"
                      min="5"
                      max="120"
                      step="5"
                      defaultValue="30"
                      className="accent-primary w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer"
                    />
                    <div className="flex justify-between text-xs text-slate-500">
                      <span>5 mins</span>
                      <span className="font-bold text-primary">30 mins</span>
                      <span>2 hours</span>
                    </div>
                  </label>
                  <label className="flex flex-col gap-2">
                    <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      Weekly Grocery Budget
                    </span>
                    <select className="rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 focus:ring-primary focus:border-primary p-3">
                      <option>Budget-Friendly ($)</option>
                      <option defaultChecked>Moderate ($$)</option>
                      <option>Premium / Gourmet ($$$)</option>
                    </select>
                  </label>
                  <div className="md:col-span-2 p-6 bg-primary/5 rounded-xl border border-primary/10">
                    <p className="text-sm font-bold text-primary mb-4 flex items-center gap-2">
                      <Icon name="auto_awesome" className="text-sm" />
                      AI Predicted Daily Targets
                    </p>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                      <div className="flex flex-col">
                        <span className="text-xs text-slate-500 uppercase">
                          Calories
                        </span>
                        <span className="text-xl font-bold">2,150</span>
                      </div>
                      <div className="flex flex-col">
                        <span className="text-xs text-slate-500 uppercase">
                          Protein
                        </span>
                        <span className="text-xl font-bold">160g</span>
                      </div>
                      <div className="flex flex-col">
                        <span className="text-xs text-slate-500 uppercase">
                          Carbs
                        </span>
                        <span className="text-xl font-bold">210g</span>
                      </div>
                      <div className="flex flex-col">
                        <span className="text-xs text-slate-500 uppercase">
                          Fats
                        </span>
                        <span className="text-xl font-bold">72g</span>
                      </div>
                    </div>
                    <p className="text-[10px] text-slate-400 mt-4 italic">
                      *Preliminary estimates. You can adjust after profile
                      creation.
                    </p>
                  </div>
                </div>
              </div>

              {/* Form Footer */}
              <div className="p-8 bg-slate-50 dark:bg-slate-800/50 flex flex-col md:flex-row items-center justify-between gap-6">
                <div className="flex items-center gap-3">
                  <div className="size-2 rounded-full bg-primary animate-pulse" />
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    Your agent is ready to design your first meal plan.
                  </p>
                </div>
                <Link
                  href="/dashboard"
                  className="w-full md:w-auto px-10 py-4 bg-primary text-white rounded-xl font-bold text-lg hover:shadow-lg hover:shadow-primary/30 transition-all flex items-center justify-center gap-2 group"
                >
                  Create My Nutrition Profile
                  <Icon
                    name="arrow_forward"
                    className="group-hover:translate-x-1 transition-transform"
                  />
                </Link>
              </div>
            </div>

            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8 px-4">
              {[
                {
                  icon: "security",
                  title: "Privacy First",
                  desc: "Your biometric data is encrypted and never sold.",
                },
                {
                  icon: "science",
                  title: "Science Based",
                  desc: "Mifflin-St Jeor equation and WHO guidelines.",
                },
                {
                  icon: "support_agent",
                  title: "24/7 Agent",
                  desc: "Modify your plan anytime by chatting with your dietitian.",
                },
              ].map(({ icon, title, desc }) => (
                <div key={title} className="flex gap-4">
                  <div className="text-primary">
                    <Icon name={icon} />
                  </div>
                  <div>
                    <h4 className="font-bold text-sm">{title}</h4>
                    <p className="text-xs text-slate-500">{desc}</p>
                  </div>
                </div>
              ))}
            </div>
    </div>
  );
}
