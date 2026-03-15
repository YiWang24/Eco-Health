"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Icon from "@/components/ui/Icon";
import ProgressStepper from "@/components/onboarding/ProgressStepper";
import {
  getCurrentUserId,
  getGoals,
  getProfile,
  hasAuthSession,
  upsertGoals,
  upsertProfile,
} from "@/lib/api";
import { ROUTES } from "@/lib/constants";

const GOAL_TEMPLATES = {
  lose_weight: { calories_target: 1700, protein_g_target: 120, carbs_g_target: 150, fat_g_target: 55 },
  gain_muscle: { calories_target: 2400, protein_g_target: 160, carbs_g_target: 250, fat_g_target: 70 },
  maintenance: { calories_target: 2100, protein_g_target: 130, carbs_g_target: 220, fat_g_target: 65 },
};

const DIET_OPTIONS = [
  { value: "no_specific_diet", label: "No specific diet" },
  { value: "vegetarian", label: "Vegetarian" },
  { value: "vegan", label: "Vegan" },
  { value: "pescatarian", label: "Pescatarian" },
  { value: "halal", label: "Halal" },
  { value: "kosher", label: "Kosher" },
  { value: "gluten_free", label: "Gluten-free" },
  { value: "dairy_free", label: "Dairy-free" },
  { value: "low_sodium", label: "Low sodium" },
  { value: "mediterranean", label: "Mediterranean" },
];

const ALLERGY_OPTIONS = [
  { value: "peanut", label: "Peanut" },
  { value: "tree_nut", label: "Tree nut" },
  { value: "milk", label: "Milk" },
  { value: "egg", label: "Egg" },
  { value: "fish", label: "Fish" },
  { value: "shellfish", label: "Shellfish" },
  { value: "sesame", label: "Sesame" },
  { value: "soy", label: "Soy" },
  { value: "wheat", label: "Wheat/Gluten" },
  { value: "mustard", label: "Mustard" },
  { value: "sulphites", label: "Sulphites" },
];

export default function OnboardingPage() {
  const router = useRouter();
  const userId = getCurrentUserId();
  const [goalType, setGoalType] = useState("lose_weight");
  const [form, setForm] = useState({
    age: "",
    height_cm: "",
    weight_kg: "",
    activity_level: "moderate",
    dietary_preferences: [],
    allergies: [],
    cook_time_preference_minutes: 30,
    budget_limit: 30,
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    if (!hasAuthSession()) {
      router.replace(`${ROUTES.auth}?mode=login`);
      return;
    }
    setAuthorized(true);
  }, [router]);

  useEffect(() => {
    if (!authorized) return;
    let active = true;
    async function load() {
      setLoading(true);
      setError("");
      try {
        const [profile, goals] = await Promise.all([
          getProfile(userId).catch(() => null),
          getGoals(userId).catch(() => null),
        ]);
        if (!active) return;

        if (profile) {
          setForm((prev) => ({
            ...prev,
            age: profile.age ?? "",
            height_cm: profile.height_cm ?? "",
            weight_kg: profile.weight_kg ?? "",
            activity_level: profile.activity_level || prev.activity_level,
            dietary_preferences: profile.dietary_preferences || [],
            allergies: profile.allergies || [],
            cook_time_preference_minutes:
              profile.cook_time_preference_minutes || prev.cook_time_preference_minutes,
          }));
        }

        if (goals) {
          const detectGoalType = Object.entries(GOAL_TEMPLATES).find(([, value]) => {
            return value.calories_target === goals.calories_target;
          })?.[0];
          if (detectGoalType) setGoalType(detectGoalType);
          setForm((prev) => ({
            ...prev,
            dietary_preferences:
              prev.dietary_preferences.length > 0
                ? prev.dietary_preferences
                : goals.dietary_restrictions || [],
            allergies: prev.allergies.length > 0 ? prev.allergies : goals.allergies || [],
            budget_limit: goals.budget_limit ?? prev.budget_limit,
            cook_time_preference_minutes:
              goals.max_cook_time_minutes ?? prev.cook_time_preference_minutes,
          }));
        }
      } catch (err) {
        if (!active) return;
        setError(err.message || "Failed to load onboarding data");
      } finally {
        if (active) setLoading(false);
      }
    }
    load();
    return () => {
      active = false;
    };
  }, [authorized, userId]);

  const targets = useMemo(() => GOAL_TEMPLATES[goalType], [goalType]);

  function toggleInList(field, value) {
    setForm((prev) => {
      const exists = prev[field].includes(value);
      return {
        ...prev,
        [field]: exists ? prev[field].filter((item) => item !== value) : [...prev[field], value],
      };
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (saving) return;

    setSaving(true);
    setError("");
    try {
      const profilePayload = {
        age: form.age ? Number(form.age) : null,
        height_cm: form.height_cm ? Number(form.height_cm) : null,
        weight_kg: form.weight_kg ? Number(form.weight_kg) : null,
        activity_level: form.activity_level || null,
        dietary_preferences: form.dietary_preferences,
        allergies: form.allergies,
        cook_time_preference_minutes: Number(form.cook_time_preference_minutes) || null,
      };

      const goalsPayload = {
        ...targets,
        dietary_restrictions: form.dietary_preferences,
        allergies: form.allergies,
        budget_limit: Number(form.budget_limit) || null,
        max_cook_time_minutes: Number(form.cook_time_preference_minutes) || null,
      };

      // Save profile first, then goals to avoid first-login write races.
      await upsertProfile(userId, profilePayload);
      await upsertGoals(userId, goalsPayload);

      router.push("/dashboard");
    } catch (err) {
      setError(err.message || "Failed to save onboarding profile");
    } finally {
      setSaving(false);
    }
  }

  if (!authorized) {
    return (
      <div className="min-h-screen flex items-center justify-center text-sm text-slate-500">
        Checking session...
      </div>
    );
  }

  return (
    <div className="layout-content-container flex flex-col max-w-4xl w-full">
      <ProgressStepper step={1} totalSteps={2} labels={["Fill Form", "Complete"]} />

      <form
        onSubmit={handleSubmit}
        className="bg-white dark:bg-slate-900 shadow-sm border border-primary/5 rounded-xl overflow-hidden"
      >
        <div className="p-8 border-b border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-3 mb-6">
            <Icon name="person" className="text-primary" />
            <h3 className="text-2xl font-bold">Tell us about yourself</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <label className="flex flex-col gap-2">
              <span className="text-sm font-semibold">Age</span>
              <input
                type="number"
                min="1"
                value={form.age}
                onChange={(e) => setForm((prev) => ({ ...prev, age: e.target.value }))}
                placeholder="e.g. 28"
                className="rounded-lg border border-slate-200 bg-slate-50 p-3"
              />
            </label>
            <label className="flex flex-col gap-2">
              <span className="text-sm font-semibold">Height (cm)</span>
              <input
                type="number"
                min="1"
                value={form.height_cm}
                onChange={(e) => setForm((prev) => ({ ...prev, height_cm: e.target.value }))}
                placeholder="175"
                className="rounded-lg border border-slate-200 bg-slate-50 p-3"
              />
            </label>
            <label className="flex flex-col gap-2">
              <span className="text-sm font-semibold">Weight (kg)</span>
              <input
                type="number"
                min="1"
                value={form.weight_kg}
                onChange={(e) => setForm((prev) => ({ ...prev, weight_kg: e.target.value }))}
                placeholder="72"
                className="rounded-lg border border-slate-200 bg-slate-50 p-3"
              />
            </label>
            <label className="flex flex-col gap-2">
              <span className="text-sm font-semibold">Activity Level</span>
              <select
                value={form.activity_level}
                onChange={(e) => setForm((prev) => ({ ...prev, activity_level: e.target.value }))}
                className="rounded-lg border border-slate-200 bg-slate-50 p-3"
              >
                <option value="sedentary">Sedentary</option>
                <option value="light">Lightly Active</option>
                <option value="moderate">Moderately Active</option>
                <option value="very_active">Very Active</option>
              </select>
            </label>
          </div>
        </div>

        <div className="p-8 border-b border-slate-100 dark:border-slate-800">
          <h3 className="text-2xl font-bold mb-4">Health Goal</h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {[
              { key: "lose_weight", title: "Lose Weight" },
              { key: "gain_muscle", title: "Gain Muscle" },
              { key: "maintenance", title: "Maintenance" },
            ].map((goal) => (
              <button
                type="button"
                key={goal.key}
                onClick={() => setGoalType(goal.key)}
                className={`rounded-xl border-2 p-4 text-left ${
                  goalType === goal.key
                    ? "border-primary bg-primary/10"
                    : "border-slate-200 hover:border-primary/40"
                }`}
              >
                <p className="font-bold">{goal.title}</p>
              </button>
            ))}
          </div>
        </div>

        <div className="p-8 border-b border-slate-100 dark:border-slate-800">
          <h3 className="text-2xl font-bold mb-4">Diet & Allergies</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <p className="text-sm font-semibold mb-3">Dietary Preferences</p>
              <div className="flex flex-wrap gap-2">
                {DIET_OPTIONS.map((item) => (
                  <button
                    type="button"
                    key={item.value}
                    onClick={() => toggleInList("dietary_preferences", item.value)}
                    className={`px-3 py-1.5 rounded-full border text-sm ${
                      form.dietary_preferences.includes(item.value)
                        ? "bg-primary text-white border-primary"
                        : "border-slate-200 hover:border-primary/50"
                    }`}
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <p className="text-sm font-semibold mb-3">Allergies</p>
              <div className="flex flex-wrap gap-2">
                {ALLERGY_OPTIONS.map((item) => (
                  <button
                    type="button"
                    key={item.value}
                    onClick={() => toggleInList("allergies", item.value)}
                    className={`px-3 py-1.5 rounded-full border text-sm ${
                      form.allergies.includes(item.value)
                        ? "bg-red-500 text-white border-red-500"
                        : "border-slate-200 hover:border-red-300"
                    }`}
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="p-8 border-b border-slate-100 dark:border-slate-800 grid grid-cols-1 md:grid-cols-2 gap-6">
          <label className="flex flex-col gap-2">
            <span className="text-sm font-semibold">Max cooking time (minutes)</span>
            <input
              type="number"
              min="5"
              max="180"
              value={form.cook_time_preference_minutes}
              onChange={(e) =>
                setForm((prev) => ({ ...prev, cook_time_preference_minutes: e.target.value }))
              }
              className="rounded-lg border border-slate-200 bg-slate-50 p-3"
            />
          </label>
          <label className="flex flex-col gap-2">
            <span className="text-sm font-semibold">Weekly grocery budget ($)</span>
            <input
              type="number"
              min="0"
              step="0.5"
              value={form.budget_limit}
              onChange={(e) => setForm((prev) => ({ ...prev, budget_limit: e.target.value }))}
              className="rounded-lg border border-slate-200 bg-slate-50 p-3"
            />
          </label>
        </div>

        <div className="p-8 bg-slate-50 dark:bg-slate-800/50 space-y-4">
          <div className="p-4 rounded-xl border border-primary/20 bg-primary/5">
            <p className="text-sm font-bold text-primary mb-2">Daily target preview</p>
            <p className="text-sm text-slate-700 dark:text-slate-300">
              Calories {targets.calories_target} • Protein {targets.protein_g_target}g • Carbs{" "}
              {targets.carbs_g_target}g • Fat {targets.fat_g_target}g
            </p>
          </div>

          {error && (
            <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={saving || loading}
            className="w-full md:w-auto px-10 py-4 bg-primary text-white rounded-xl font-bold text-lg disabled:opacity-50"
          >
            {saving ? "Saving..." : loading ? "Loading..." : "Create My Nutrition Profile"}
          </button>
        </div>
      </form>
    </div>
  );
}
