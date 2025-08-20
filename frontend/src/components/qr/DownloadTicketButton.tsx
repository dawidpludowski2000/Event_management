"use client";

import { downloadTicket } from "@/lib/api/reservations";

interface Props { reservationId: number; }

export default function DownloadTicketButton({ reservationId }: Props) {
  const handleDownload = async () => {
    try {
      const blob = await downloadTicket(reservationId);
      const url = URL.createObjectURL(blob);
      window.open(url, "_blank");
    } catch (err) {
      console.error(err);
      alert("Błąd podczas pobierania biletu.");
    }
  };

  return <button onClick={handleDownload}>🎟 Pobierz bilet</button>;
}
