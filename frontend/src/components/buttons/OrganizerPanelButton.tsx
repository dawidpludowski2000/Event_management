"use client";
import { useRouter } from "next/navigation";

export default function OrganizerPanelButton() {
  const router = useRouter();

  return (
    <button onClick={() => router.push("/organizer-reservation")}>
      Zarządzaj swoimi wydarzeniami / Stwórz nowy event
    </button>
  );
}
