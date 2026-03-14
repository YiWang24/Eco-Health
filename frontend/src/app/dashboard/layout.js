import Header from "@/components/layout/Header";
import BottomNav from "@/components/layout/BottomNav";

export default function DashboardLayout({ children }) {
  return (
    <div className="relative flex min-h-screen w-full flex-col overflow-x-hidden">
      <Header variant="dashboard" />
      <main className="mx-auto flex w-full flex-1 flex-col p-6 pb-24">
        {children}
      </main>
      <BottomNav />
    </div>
  );
}
