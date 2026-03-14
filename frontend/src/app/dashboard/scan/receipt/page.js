import Link from "next/link";
import Icon from "@/components/ui/Icon";

export const metadata = {
  title: "Receipt Scan - Agentic Dietitian",
};

const RECEIPT_IMAGE =
  "https://lh3.googleusercontent.com/aida-public/AB6AXuBDL_KmWUsS-JI3LfgXWk58eciGRxIpL3PktHtGdQAtb-XsIXJMshzUVlHnUt4K-jCHXZqK0THmsMXnFb9CRm4XmyZinA-qAzbtDK47QxaKVH5ht3zUDPCadQUNXVxrWKQtLEPuKmOiyx-8n7uvQ7yETwhgU2ANpkfwaxy6KAmukJguBsvmLXpRRC-2HBzDHFiTFp1oKkhWqBIfYXgF0hNx4KjPGFpL0IOqqeoKOziz7kPK9kYyrjxuf8S9TPITDnd8aU6tMBmwnnuo";

const detectedItems = [
  "Organic Spinach",
  "Large Eggs",
  "Chicken Breast",
];

export default function ReceiptScanPage() {
  return (
    <div className="flex flex-1 flex-col overflow-hidden p-6 gap-6">
      <div className="flex flex-1 gap-6 min-h-0">
        <div className="flex-1 flex flex-col gap-4">
          <div className="relative flex-1 overflow-hidden rounded-xl bg-slate-900 border-4 border-primary/20 shadow-2xl">
            <div
              className="absolute inset-0 bg-cover bg-center opacity-80"
              style={{ backgroundImage: `url('${RECEIPT_IMAGE}')` }}
            />
            <div className="absolute top-0 left-0 w-full h-1 bg-primary/60 shadow-[0_0_15px_rgba(76,174,79,0.8)] z-10" />
            {detectedItems.map((item, i) => (
              <div
                key={item}
                className="absolute flex items-center gap-2 bg-primary/90 text-white px-3 py-1 rounded-full text-xs font-bold shadow-lg border border-white/20"
                style={{
                  top: `${20 + i * 22}%`,
                  left: `${15 + (i % 2) * 25}%`,
                }}
              >
                <Icon name="check_circle" className="text-sm" />
                {item}
              </div>
            ))}
            <div className="absolute top-4 left-4 w-8 h-8 border-t-2 border-l-2 border-primary" />
            <div className="absolute top-4 right-4 w-8 h-8 border-t-2 border-r-2 border-primary" />
            <div className="absolute bottom-4 left-4 w-8 h-8 border-b-2 border-l-2 border-primary" />
            <div className="absolute bottom-4 right-4 w-8 h-8 border-b-2 border-r-2 border-primary" />
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-64 h-64 border border-white/20 rounded-xl flex items-center justify-center">
                <Icon name="filter_center_focus" className="text-white/40 text-6xl" />
              </div>
            </div>
          </div>
          <button
            type="button"
            className="w-full bg-primary hover:bg-primary/90 text-white py-4 rounded-xl font-bold text-lg flex items-center justify-center gap-2 transition-all shadow-lg active:scale-[0.98]"
          >
            <Icon name="camera_alt" />
            Capture Receipt
          </button>
        </div>
        <div className="w-72 flex-shrink-0 flex flex-col gap-4">
          <h3 className="text-sm font-bold text-primary flex items-center gap-2">
            <Icon name="barcode_scanner" className="animate-pulse" />
            Detected Items
          </h3>
          <ul className="space-y-2 overflow-y-auto">
            {detectedItems.map((item) => (
              <li
                key={item}
                className="flex items-center gap-2 p-2 rounded-lg bg-white dark:bg-slate-800 border border-primary/10"
              >
                <Icon name="check_circle" className="text-primary text-sm" />
                <span className="text-sm font-medium">{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
