import { redirect } from "next/navigation";

export default function FridgeScanRedirectPage() {
  redirect("/dashboard/scan?tab=fridge");
}
