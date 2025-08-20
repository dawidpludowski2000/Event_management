"use client";

import { useState, useEffect } from "react";
import { getOrganizerReservations } from "@/lib/api/reservations";
import { getOrganizerMyEvents } from "@/lib/api/events";

import BackEventListButton from "@/components/buttons/events-buttons/BackEventListButton";
import ConfirmReservationButton from "@/components/buttons/reservations-buttons/ConfirmReservationButton";
import RejectReservationButton from "@/components/buttons/reservations-buttons/RejectReservationButton";
import CheckInButton from "@/components/qr/CheckInButton";
import QRScannerCheckIn from "@/components/qr/QRScannerCheckIn";
import CreateNewEventButton from "@/components/buttons/events-buttons/CreateNewEventButton";
import EditEventButton from "@/components/buttons/events-buttons/EditEventButton";
import PublishEventButton from "@/components/buttons/events-buttons/PublishEventButton";
import CancelEventButton from "@/components/buttons/events-buttons/CancelEventButton";
import ScanTicketsButton from "@/components/buttons/events-buttons/ScanTicketsButton";



import styles from "./OrganizerCreateNewEvents.module.css";

export default function OrganizerReservationsPage() {
  const [reservations, setReservations] = useState<any[]>([]);
  const [myEvents, setMyEvents] = useState<any[]>([]);
  const [loadingMyEvents, setLoadingMyEvents] = useState(true);

  const fetchReservations = async () => {
    try {
      const data = await getOrganizerReservations();
      setReservations(data);
    } catch (err) {
      console.error("Błąd:", err);
    }
  };

  const fetchMyEvents = async () => {
    try {
      const data = await getOrganizerMyEvents();
      setMyEvents(data);
    } catch (err) {
      console.error("Błąd:", err);
    } finally {
      setLoadingMyEvents(false);
    }
  };

  useEffect(() => {
    fetchReservations();
    fetchMyEvents();
  }, []);

  return (
    <div>
      <div className={styles.buttons}>
        <BackEventListButton />
        <CreateNewEventButton />
        <ScanTicketsButton />
      </div>

      <h1>Rezerwacje na moje wydarzenia</h1>

      <ul>
        {reservations.map((r) => (
          <li key={r.reservation_id} style={{ marginBottom: "0.75rem" }}>
            <strong>{r.event_title}</strong> ({r.event_start_time})<br />
            {r.user_email} – {r.status} {r.checked_in && " (obecny)"}

            {r.status === "pending" && (
              <>
                <ConfirmReservationButton
                  reservationId={r.reservation_id}
                  onSuccess={fetchReservations}
                />
                <RejectReservationButton
                  reservationId={r.reservation_id}
                  onSuccess={fetchReservations}
                />
              </>
            )}

            {r.status === "confirmed" && !r.checked_in && (
              <CheckInButton
                reservationId={r.reservation_id}
                onSuccess={fetchReservations}
              />
            )}
          </li>
        ))}
      </ul>

      <h2 style={{ marginTop: "2rem" }}>Moje wydarzenia</h2>
      {loadingMyEvents ? (
        <p>⏳ Ładowanie…</p>
      ) : myEvents.length === 0 ? (
        <p>Brak utworzonych wydarzeń.</p>
      ) : (
        <ul>
          {myEvents.map((event) => (
            <li key={event.id} style={{ marginBottom: "0.75rem" }}>
              <strong>{event.title}</strong> ({event.start_time}) – {event.location}{" "}
              <span
                className={`${styles.status} ${event.status === "published"
                    ? styles.statusPublished
                    : event.status === "draft"
                      ? styles.statusDraft
                      : styles.statusCancelled
                  }`}
              >
                {event.status}
              </span>


              <EditEventButton eventId={event.id} />

              {event.status === "draft" && (
                <PublishEventButton eventId={event.id} onSuccess={fetchMyEvents} />
              )}

              {event.status === "published" && (
                <CancelEventButton eventId={event.id} onSuccess={fetchMyEvents} />
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
