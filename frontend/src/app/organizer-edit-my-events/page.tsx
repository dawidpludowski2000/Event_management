"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { updateOrganizerEvent } from "@/lib/api/events";

export default function OrganizerEditMyEventsPage() {
  const router = useRouter();
  const sp = useSearchParams();
  const eventId = Number(sp.get("eventId"));

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!Number.isFinite(eventId)) {
      alert("Brak poprawnego eventId w adresie.");
      return;
    }

    const f = new FormData(e.currentTarget);
    const start = String(f.get("start_time") || "");
    const end = String(f.get("end_time") || "");
    const description = String(f.get("description") || "");

    if (!start && !end && !description) {
      alert("Wpisz chociaż jedną zmianę (data/godzina lub opis).");
      return;
    }
    if (start && end && new Date(end) <= new Date(start)) {
      alert("Koniec musi być po początku.");
      return;
    }

    const payload: any = {};
    if (start) payload.start_time = new Date(start).toISOString();
    if (end)   payload.end_time   = new Date(end).toISOString();
    if (description) payload.description = description;

    try {
      await updateOrganizerEvent(eventId, payload);
      router.push("/organizer-reservation");
    } catch (err: any) {
      alert(err?.message || "Błąd edycji wydarzenia.");
      console.error(err);
    }
  };

  return (
    <form onSubmit={onSubmit} style={{ maxWidth: 640, margin: "0 auto", padding: 12 }}>
      <h1>Edytuj wydarzenie</h1>
      <p style={{ opacity: 0.8, fontSize: 13, marginTop: -6 }}>
        Zmień tylko to, co potrzebujesz. Puste pola nie będą wysłane.
      </p>

      <label>Początek (data i godzina)</label><br />
      <input name="start_time" type="datetime-local" /><br />

      <label>Koniec (data i godzina)</label><br />
      <input name="end_time" type="datetime-local" /><br />

      <label>Opis (opcjonalnie)</label><br />
      <textarea name="description" rows={3} /><br />

      <button type="submit">Zapisz zmiany</button>
      <button type="button" onClick={() => router.push("/organizer-reservation")} style={{ marginLeft: 8 }}>
        Anuluj
      </button>
    </form>
  );
}
