import { redirect } from "next/navigation";

export default function MealScanRedirectPage() {
  redirect("/dashboard/scan?tab=meal");
}
