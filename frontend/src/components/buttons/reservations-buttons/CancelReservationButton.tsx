"use client";
import { useState } from "react";
import { cancelReservation } from "@/lib/api/reservations";
import { toast } from "react-hot-toast";

interface CancelReservationButtonProps {
  reservationId: number;
  onSuccess: () => void;
}

export default function CancelReservationButton({
  reservationId,
  onSuccess,
}: CancelReservationButtonProps) {
  const [loading, setLoading] = useState(false);

  const handleCancel = async () => {
    if (loading) return;
    setLoading(true);

    try {
      const res = await cancelReservation(reservationId);
      const data = await res.json().catch(() => ({}));
      if (res.ok) {
        toast.success("Rezerwacja została anulowana ❌");
        onSuccess();
      } else {
        toast.error(data.detail || "Nie udało się anulować rezerwacji ❌");
      }
    } catch {
      toast.error("Błąd połączenia z serwerem.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleCancel} disabled={loading}>
      {loading ? "Anuluję..." : "Anuluj rezerwację"}
    </button>
  );
}
