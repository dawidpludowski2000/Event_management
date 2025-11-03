// MOJE REZERWACJE

"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import BackEventListButton from "@/components/buttons/events-buttons/BackEventListButton";
import CancelReservationButton from "@/components/buttons/reservations-buttons/CancelReservationButton";
import DownloadTicketButton from "@/components/qr/DownloadTicketButton";
import { getMyReservations } from "@/lib/api/reservations";
import styles from "./MyReservations.module.css";

export default function MyReservationsPage() {
  const [reservations, setReservations] = useState<any[]>([]);
  const router = useRouter();

  const fetchReservations = useCallback(async () => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      router.push("/login");
      return;
    }

    try {
      const data = await getMyReservations();
      setReservations(data);
    } catch (err) {
      console.error(err);
    }
  }, [router]);

  useEffect(() => {
    fetchReservations();
  }, [fetchReservations]);

  return (
    <div>
      <BackEventListButton />
      <h1>Moje rezerwacje</h1>

      <ul>
        {reservations.map((res) => (
          <li
            key={res.event_title + res.event_start_time}
            style={{ marginBottom: "20px" }} // odstęp między rezerwacjami
          >
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <strong>{res.event_title}</strong> – {res.event_start_time} - {res.location} –
              <span
                className={
                  res.status === "confirmed"
                    ? styles.statusConfirmed
                    : res.status === "cancelled"
                    ? styles.statusCancelled
                    : styles.statusPending
                }
              >
                {res.status}
              </span>

              {res.status === "confirmed" && (
                <DownloadTicketButton reservationId={res.reservation_id} />
              )}
            </div>

            <div style={{ marginTop: "8px" }}>
              <CancelReservationButton
                reservationId={res.reservation_id}
                onSuccess={fetchReservations}
              />
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
