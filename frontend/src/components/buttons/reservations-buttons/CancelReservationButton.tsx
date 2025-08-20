"use client";

import { useState } from "react";
import { cancelReservation } from "@/lib/api/reservations";

interface CancelReservationButtonProps {
  reservationId: number;
  onSuccess: () => void;
}

export default function CancelReservationButton({
  reservationId,
  onSuccess,
}: CancelReservationButtonProps) {
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleCancel = async () => {
    const res = await cancelReservation(reservationId);

    if (res.ok) {
      setSuccess("Rezerwacja została anulowana.");
      setError("");
      onSuccess();
    } else {
      const data = await res.json().catch(() => ({}));
      setError(data.detail || "Nie udało się anulować rezerwacji.");
      setSuccess("");
    }
  };

  return (
    <>
      <button onClick={handleCancel}>Anuluj rezerwację</button>
      {success && <p style={{ color: "green" }}>{success}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </>
  );
}
