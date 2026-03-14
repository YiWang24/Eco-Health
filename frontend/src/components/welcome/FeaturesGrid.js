import Icon from "@/components/ui/Icon";

const features = [
  {
    icon: "camera_outdoor",
    title: "Scan your fridge",
    description:
      "Snap a photo of your ingredients and let our AI vision identify items automatically.",
  },
  {
    icon: "monitoring",
    title: "Track automatically",
    description:
      "No more manual logging. Our agent tracks your nutritional intake as you cook.",
  },
  {
    icon: "skillet",
    title: "Personalized recipes",
    description:
      "Chef-quality recipes tailored to your fitness goals and what's in your pantry.",
  },
  {
    icon: "eco",
    title: "Reduce food waste",
    description:
      "Save money and the planet by using every ingredient before it expires.",
  },
];

export default function FeaturesGrid() {
  return (
    <section
      id="features"
      className="px-6 lg:px-20 py-20 bg-slate-50 dark:bg-slate-900/30"
    >
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col gap-4 mb-16 text-center lg:text-left">
          <h2 className="text-slate-900 dark:text-slate-100 text-3xl lg:text-4xl font-black tracking-tight">
            Smart Features for a Healthier You
          </h2>
          <p className="text-slate-600 dark:text-slate-400 text-lg max-w-2xl">
            Everything you need to manage your nutrition efficiently and
            sustainably.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map(({ icon, title, description }) => (
            <div
              key={title}
              className="group flex flex-col gap-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/50 p-8 hover:border-primary/50 transition-all hover:shadow-xl hover:shadow-primary/5"
            >
              <div className="bg-primary/10 text-primary w-12 h-12 rounded-xl flex items-center justify-center group-hover:bg-primary group-hover:text-white transition-colors">
                <Icon name={icon} className="text-2xl" />
              </div>
              <div className="flex flex-col gap-2">
                <h3 className="text-slate-900 dark:text-slate-100 text-xl font-bold">
                  {title}
                </h3>
                <p className="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">
                  {description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
