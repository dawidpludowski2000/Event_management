"use client";

import { useState, useEffect } from "react";
import { getOrganizerReservations } from "@/lib/api/reservations";
import { getOrganizerMyEvents } from "@/lib/api/events";
import BackEventListButton from "@/components/buttons/events-buttons/BackEventListButton";
import ConfirmReservationButton from "@/components/buttons/reservations-buttons/ConfirmReservationButton";
import RejectReservationButton from "@/components/buttons/reservations-buttons/RejectReservationButton";
import CheckInButton from "@/components/qr/CheckInButton";
import CreateNewEventButton from "@/components/buttons/events-buttons/CreateNewEventButton";
import EditEventButton from "@/components/buttons/events-buttons/EditEventButton";
import PublishEventButton from "@/components/buttons/events-buttons/PublishEventButton";
import CancelEventButton from "@/components/buttons/events-buttons/CancelEventButton";
import ScanTicketsButton from "@/components/buttons/events-buttons/ScanTicketsButton";
import styles from "./OrganizerCreateNewEvents.module.css";

export default function OrganizerReservationsPage() {
  const [reservations, setReservations] = useState<any[]>([]);
  const [myEvents, setMyEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [reservationsData, eventsData] = await Promise.all([
        getOrganizerReservations(),
        getOrganizerMyEvents(),
      ]);
      setReservations(reservationsData);
      setMyEvents(eventsData);
    } catch (err) {
      console.error("Błąd:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <p>⏳ Ładowanie…</p>;

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: "1rem" }}>
      <div className={styles.buttons}>
        <BackEventListButton />
        <CreateNewEventButton />
        <ScanTicketsButton />
      </div>

      <h1>Rezerwacje na moje wydarzenia</h1>

      <ul style={{ listStyle: "none", padding: 0 }}>
        {reservations.map((r) => (
          <li
            key={r.reservation_id}
            style={{
              borderBottom: "1px solid #ddd",
              padding: "0.5rem 0",
              marginBottom: "0.75rem",
            }}
          >
            <div>
              <strong>{r.event_title}</strong> ({r.event_start_time})
              <br />
              <span style={{ fontSize: 14 }}>
                {r.user_email} —{" "}
                <b>
                  {r.status === "pending"
                    ? "Oczekuje"
                    : r.status === "confirmed"
                    ? "Potwierdzona"
                    : "Odrzucona"}
                </b>{" "}
                {r.checked_in && "(obecny)"}
              </span>
            </div>

            <div style={{ marginTop: 4 }}>
              {r.status === "pending" && (
                <>
                  <ConfirmReservationButton
                    reservationId={r.reservation_id}
                    onSuccess={fetchData}
                  />
                  <RejectReservationButton
                    reservationId={r.reservation_id}
                    onSuccess={fetchData}
                  />
                </>
              )}

              {r.status === "confirmed" && !r.checked_in && (
                <CheckInButton
                  reservationId={r.reservation_id}
                  onSuccess={fetchData}
                />
              )}
            </div>
          </li>
        ))}
      </ul>

      <h2 style={{ marginTop: "2rem" }}>Moje wydarzenia</h2>
      {myEvents.length === 0 ? (
        <p>Brak utworzonych wydarzeń.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {myEvents.map((event) => (
            <li
              key={event.id}
              style={{
                borderBottom: "1px solid #ddd",
                padding: "0.5rem 0",
                marginBottom: "0.75rem",
              }}
            >
              <strong>{event.title}</strong> — {event.start_time} ({event.location}){" "}
              <span
                style={{
                  padding: "2px 8px",
                  borderRadius: 6,
                  backgroundColor:
                    event.status === "published"
                      ? "#d1fae5"
                      : event.status === "draft"
                      ? "#fef9c3"
                      : "#fee2e2",
                  color:
                    event.status === "published"
                      ? "#065f46"
                      : event.status === "draft"
                      ? "#92400e"
                      : "#991b1b",
                  fontWeight: 600,
                  fontSize: 13,
                }}
              >
                {event.status === "published"
                  ? "Opublikowane"
                  : event.status === "draft"
                  ? "Szkic"
                  : "Anulowane"}
              </span>
              <div style={{ marginTop: 6 }}>
                <EditEventButton eventId={event.id} />{" "}
                {event.status === "draft" && (
                  <PublishEventButton eventId={event.id} onSuccess={fetchData} />
                )}
                {event.status === "published" && (
                  <CancelEventButton eventId={event.id} onSuccess={fetchData} />
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
