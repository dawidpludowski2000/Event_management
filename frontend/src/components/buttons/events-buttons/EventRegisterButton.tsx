"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { useMyReservationStatus } from "@/lib/hooks/useMyReservationStatus";
import { registerToEvent } from "@/lib/api/events";
import { toast } from "react-hot-toast"; // ← DODANE

interface EventRegisterButtonProps {
  eventId: number;
}

export default function EventRegisterButton({ eventId }: EventRegisterButtonProps) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const {
    registered,
    isFull,
    loading: statusLoading,
    refetch,
  } = useMyReservationStatus(eventId);

  const handleClick = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      toast.error("Musisz być zalogowany."); // ← zamiana
      router.push("/login");
      return;
    }

    try {
      setLoading(true);
      const res = await registerToEvent(eventId);

      if (res.status === 201) {
        toast.success("Zapisano! Czekaj na potwierdzenie."); // ← zamiana
        refetch();
      } else if (res.status === 400) {
        const data = await res.json().catch(() => ({}));
        const msg =
          data?.detail ??
          (Array.isArray(data?.non_field_errors) ? data.non_field_errors[0] : undefined) ??
          (data && typeof data === "object" ? String(Object.values(data).flat()[0]) : undefined) ??
          "Nie można zapisać na wydarzenie.";
        toast.error(msg); // ← zamiana
      } else if (res.status === 404) {
        toast.error("Wydarzenie nie istnieje."); // ← zamiana
      } else {
        toast.error("Wystąpił nieznany błąd."); // ← zamiana
      }
    } catch (err) {
      console.error(err);
      toast.error("Błąd połączenia z serwerem."); // ← zamiana
    } finally {
      setLoading(false);
    }
  };

  if (statusLoading || registered || isFull) return null;

  return (
    <button onClick={handleClick} disabled={loading}>
      {loading ? "Wysyłam..." : "Zapisz się"}
    </button>
  );
}
