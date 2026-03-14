import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import HeroSection from "@/components/welcome/HeroSection";
import FeaturesGrid from "@/components/welcome/FeaturesGrid";
import CtaSection from "@/components/welcome/CtaSection";

export default function HomePage() {
  return (
    <div className="relative flex min-h-screen flex-col overflow-x-hidden">
      <div className="layout-container flex h-full grow flex-col">
        <Header variant="welcome" />
        <main className="flex-1">
          <HeroSection />
          <FeaturesGrid />
          <CtaSection />
        </main>
        <Footer />
      </div>
    </div>
  );
}
