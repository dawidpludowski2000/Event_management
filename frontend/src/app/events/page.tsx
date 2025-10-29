// STRONA Z LISTĄ WYDARZEŃ


"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import LogoutButton from "@/components/buttons/users-buttons/LogoutButton";
import EventRegisterButton from "@/components/buttons/events-buttons/EventRegisterButton";
import MyReservationsButton from "@/components/buttons/reservations-buttons/MyReservationsButton";
import OrganizerPanelButton from "@/components/buttons/OrganizerPanelButton";

import EventAvailability from "@/components/event-info/EventAvailability";

import { checkIfOrganizer, checkIfAdmin } from "@/lib/utils/roles";
import { getAllEvents } from "@/lib/api/events";
import AdminPanelButton from "@/components/buttons/admin-buttons/AdminPanelButton";



export default function EventsPage() {
  const router = useRouter();
  const [events, setEvents] = useState<any[]>([]);
  const [isOrganizer, setIsOrganizer] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);


  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      router.push("/login");
      return;
    }

    checkIfOrganizer().then(setIsOrganizer);

    checkIfAdmin().then(setIsAdmin);

    getAllEvents()
      .then(setEvents)
      .catch((err) => {
        console.error(err);
      });
  }, [router]);



  return (
  <div style={{ position: "relative" }}>
    {/* Wyloguj w prawym górnym rogu */}
    <div style={{ position: "absolute", top: 0, right: 600 }}>
      <LogoutButton />
    </div>

      
    {/* Przyciski Panelu organizatora i admina obok siebie */}
    <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
      {isOrganizer && <OrganizerPanelButton />}
      {isAdmin && <AdminPanelButton />}
      </div>
      
    {/* Moje rezerwacje po lewej */}
    <MyReservationsButton />

    <h1>Lista wydarzeń</h1>

    

    <ul>
      {events.map((event) => (
        <li
          key={event.id}
          style={{
            marginBottom: "3rem",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
            <strong>{event.title}</strong> – {event.start_time} - {event.location}
            <EventRegisterButton eventId={event.id} />
          </div>

          <EventAvailability
            eventId={event.id}
            seatsLimit={event.seats_limit}
          />
        </li>
      ))}
    </ul>
    </div>
  );
}


