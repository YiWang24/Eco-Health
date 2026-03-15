import Button from "@/components/ui/Button";
import { ROUTES } from "@/lib/constants";

export default function CtaSection() {
  return (
    <section className="px-6 lg:px-20 py-20">
      <div className="max-w-5xl mx-auto rounded-[2rem] bg-slate-900 dark:bg-primary/10 overflow-hidden relative border border-slate-800">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-transparent" />
        <div className="relative px-8 py-16 lg:p-20 flex flex-col items-center text-center gap-8">
          <h2 className="text-white text-4xl lg:text-5xl font-black tracking-tight max-w-2xl">
            Ready to start your nutrition journey?
          </h2>
          <p className="text-slate-400 text-lg lg:text-xl max-w-xl">
            Join thousands of users optimizing their health and kitchen
            efficiency with Agentic Personal Dietitian.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Button
              href={`${ROUTES.auth}?mode=register`}
              variant="primary"
              size="lg"
              className="!bg-primary !text-white hover:!scale-[1.05]"
            >
              Get Started Now
            </Button>
            <Button variant="ghost" size="lg">
              Talk to Sales
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}
