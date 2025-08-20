"use client";

import { checkInReservation } from "@/lib/api/reservations";
import { toast } from "react-hot-toast";

interface Props {
  reservationId: number;
  onSuccess: () => void;
}

export default function CheckInButton({ reservationId, onSuccess }: Props) {
  const handleCheckIn = async () => {
    try {
      // ta funkcja zwraca JSON { detail, checked_in, reservation_id } albo rzuca błąd
      const data = await checkInReservation(reservationId);
      toast.success(data.detail || "Check-in wykonany ✅");
      setTimeout(onSuccess, 300);
    } catch (e: any) {
      toast.error(e?.message || "Nie udało się wykonać check-in.");
    }
  };

  return <button onClick={handleCheckIn}>✅ Check-in</button>;
}
