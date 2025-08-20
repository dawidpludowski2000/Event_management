"use client";

import { rejectReservation } from "@/lib/api/reservations";
import { toast } from "react-hot-toast";

interface RejectReservationButtonProps {
  reservationId: number;
  onSuccess: () => void;
}

export default function RejectReservationButton({
  reservationId,
  onSuccess,
}: RejectReservationButtonProps) {
  const handleClick = async () => {
    const response = await rejectReservation(reservationId);

    if (response.ok) {
      toast.success("Rezerwacja odrzucona ❌");
      setTimeout(onSuccess, 300);
    } else {
      const data = await response.json().catch(() => ({}));
      const msg = data?.detail || "Nie udało się odrzucić rezerwacji.";
      toast.error(msg);
    }
  };

  return <button onClick={handleClick}>Odrzuć</button>;
}
