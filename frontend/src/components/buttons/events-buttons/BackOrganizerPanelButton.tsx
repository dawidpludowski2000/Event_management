"use client";
import { useRouter } from "next/navigation";

export default function BackOrganizerPanelButton() {
  const router = useRouter();
  return (
    <button onClick={() => router.push("/organizer-reservation")}>
      ← Panel organizatora
    </button>
  );
}
