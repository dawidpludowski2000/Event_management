"use client";

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
  const handleCancel = async () => {
    try {
      const res = await cancelReservation(reservationId);

      if (res.ok) {
        toast.success("Rezerwacja została anulowana.");
        onSuccess();
      } else {
        const data = await res.json().catch(() => ({}));
        toast.error(data.detail || "Nie udało się anulować rezerwacji.");
      }
    } catch (e: any) {
      toast.error(e?.message || "Błąd połączenia z serwerem.");
    }
  };

  return <button onClick={handleCancel}>Anuluj rezerwację</button>;
}
