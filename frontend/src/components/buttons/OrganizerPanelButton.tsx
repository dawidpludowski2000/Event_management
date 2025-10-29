"use client";
import { useRouter } from "next/navigation";

export default function OrganizerPanelButton() {
  const router = useRouter();

  return (
    <button
      onClick={() => router.push("/organizer-reservation")}
      style={{
        backgroundColor: "#0070f3",
        color: "white",
        padding: "8px 16px",
        border: "none",
        borderRadius: "6px",
        cursor: "pointer",
        fontWeight: 500,
        marginRight: "10px",
        whiteSpace: "nowrap",
        height: "33px", 
      }}
    >
      Zarządzaj wydarzeniami / Stwórz nowy event
    </button>
  );
}
