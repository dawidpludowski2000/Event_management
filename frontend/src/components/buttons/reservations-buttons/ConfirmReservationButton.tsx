"use client";

import { confirmReservation } from "@/lib/api/reservations";
import toast, { Toast } from "react-hot-toast";

interface ConfirmReservationButtonProps {
  reservationId: number;
  onSuccess: () => void;
}

export default function ConfirmReservationButton({
  reservationId,
  onSuccess,
}: ConfirmReservationButtonProps) {
  const handleClick = async () => {
    const response = await confirmReservation(reservationId);
    if (response.ok) {
      toast.success("Rezerwacja potwierdzona ✅");
      setTimeout(onSuccess, 300);
    } else {
      const data = await response.json().catch(() => ({}));
      const msg = data?.detail || "Nie udało się potwierdzić rezerwacji.";
      toast.error(msg);
    }
  };

  return <button onClick={handleClick}>Potwierdź</button>;
}
