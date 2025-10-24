"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import { updateOrganizerEvent } from "@/lib/api/events";
import { toast } from "react-hot-toast";

export default function OrganizerEditMyEventsPage() {
  const router = useRouter();
  const sp = useSearchParams();
  const eventId = Number(sp.get("eventId"));
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!Number.isFinite(eventId)) {
      toast.error("Brak poprawnego eventId w adresie.");
      return;
    }

    const f = new FormData(e.currentTarget);
    const start = String(f.get("start_time") || "");
    const end = String(f.get("end_time") || "");
    const description = String(f.get("description") || "");

    if (!start && !end && !description) {
      toast.error("Wpisz chociaż jedną zmianę (data/godzina lub opis).");
      return;
    }

    if (start && end && new Date(end) <= new Date(start)) {
      toast.error("Koniec musi być po początku.");
      return;
    }

    const payload: any = {};
    if (start) payload.start_time = new Date(start).toISOString();
    if (end) payload.end_time = new Date(end).toISOString();
    if (description) payload.description = description;

    try {
      setLoading(true);
      await updateOrganizerEvent(eventId, payload);
      toast.success("Zapisano zmiany!");
      router.push("/organizer-reservation");
    } catch (err: any) {
      toast.error(err?.message || "Błąd edycji wydarzenia.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={onSubmit} style={{ maxWidth: 640, margin: "0 auto", padding: 12 }}>
      <h1>Edytuj wydarzenie</h1>
      <p style={{ opacity: 0.8, fontSize: 13, marginTop: -6 }}>
        Zmień tylko to, co potrzebujesz. Puste pola nie będą wysłane.
      </p>

      <label>Początek</label><br />
      <input name="start_time" type="datetime-local" /><br />

      <label>Koniec</label><br />
      <input name="end_time" type="datetime-local" /><br />

      <label>Opis</label><br />
      <textarea name="description" rows={3} /><br />

      <button type="submit" disabled={loading}>
        {loading ? "Zapisywanie..." : "Zapisz zmiany"}
      </button>
      <button
        type="button"
        onClick={() => router.push("/organizer-reservation")}
        style={{ marginLeft: 8 }}
      >
        Anuluj
      </button>
    </form>
  );
}
