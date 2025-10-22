"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { useMyReservationStatus } from "@/lib/hooks/useMyReservationStatus";
import { registerToEvent } from "@/lib/api/events";
import { toast } from "react-hot-toast";

interface EventRegisterButtonProps {
  eventId: number;
}

export default function EventRegisterButton({ eventId }: EventRegisterButtonProps) {

  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [justRegistered, setJustRegistered] = useState(false); // 👈 lokalny stan
  const { registered, isFull, loading: statusLoading, refetch } =
    useMyReservationStatus(eventId);

  const handleClick = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      toast.error("Musisz być zalogowany.");
      router.push("/login");
      return;
    }

    try {
      setLoading(true);
      const res = await registerToEvent(eventId);

      if (res.status === 201) {
        toast.success("Zapisano na wydarzenie ✅");
        setJustRegistered(true); // 👈 od razu zmień przycisk
        setTimeout(() => refetch(), 400);
        return;
      }

      if (res.status === 400) {
        const data = await res.json().catch(() => ({}));
        const msg =
          data?.detail ??
          (Array.isArray(data?.non_field_errors)
            ? data.non_field_errors[0]
            : undefined) ??
          (data && typeof data === "object"
            ? String(Object.values(data).flat()[0])
            : undefined) ??
          "Nie można zapisać na wydarzenie.";

        if (msg.includes("already registered")) {
          toast.error("Już jesteś zapisany na to wydarzenie.");
        } else {
          toast.error(msg);
        }
        return;
      }

      if (res.status === 404) {
        toast.error("Wydarzenie nie istnieje.");
      } else {
        toast.error("Wystąpił nieznany błąd.");
      }
    } catch (err) {
      console.error(err);
      toast.error("Błąd połączenia z serwerem.");
    } finally {
      setLoading(false);
    }
  };

  if (statusLoading) return null;

  if (registered || justRegistered)
    return (
      <button disabled style={{ opacity: 0.6 }}>
        ✅ Zapisano na wydarzenie
      </button>
    );

  if (isFull)
    return (
      <button disabled style={{ opacity: 0.6 }}>
        ❌ Brak miejsc
      </button>
    );

  return (
    <button onClick={handleClick} disabled={loading}>
      {loading ? "Wysyłam..." : "Zapisz się"}
    </button>
  );
}
