import { redirect } from "next/navigation";

export default function ReceiptScanRedirectPage() {
  redirect("/dashboard/scan?tab=receipt");
}
