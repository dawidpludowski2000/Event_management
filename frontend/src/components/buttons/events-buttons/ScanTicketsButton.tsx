"use client";
import { useRouter } from "next/navigation";

export default function ScanTicketsButton() {
  const router = useRouter();
  return (
    <button onClick={() => router.push("/organizer-reservation/scan")}>
      📷 Skanuj bilety
    </button>
  );
}
