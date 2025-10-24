"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createNewEvent } from "@/lib/api/events";
import BackEventListButton from "@/components/buttons/events-buttons/BackEventListButton";
import { toast } from "react-hot-toast";

export default function CreateEventPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    title: "",
    description: "",
    location: "",
    start_time: "",
    end_time: "",
    seats_limit: 50,
  });

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!form.title || !form.location || !form.start_time || !form.end_time) {
      toast.error("Uzupełnij wymagane pola.");
      return;
    }
    if (new Date(form.end_time) <= new Date(form.start_time)) {
      toast.error("Koniec musi być po początku.");
      return;
    }

    try {
      setLoading(true);
      const res = await createNewEvent({
        title: form.title,
        description: form.description || "",
        location: form.location,
        start_time: new Date(form.start_time).toISOString(),
        end_time: new Date(form.end_time).toISOString(),
        seats_limit: Number(form.seats_limit),
      });

      if (res.ok) {
        toast.success("Wydarzenie utworzone pomyślnie 🎉");
        setTimeout(() => router.push("/organizer-reservation"), 1000);
      } else {
        const data = await res.json().catch(() => ({}));
        toast.error(data.detail || "Błąd tworzenia wydarzenia.");
      }
    } catch (err) {
      console.error(err);
      toast.error("Błąd połączenia z serwerem.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 720, margin: "0 auto" }}>
      <BackEventListButton />
      <h1>Utwórz nowe wydarzenie</h1>

      <form onSubmit={onSubmit} style={{ border: "1px solid #ddd", padding: 16 }}>
        <label>Tytuł*</label><br />
        <input
          value={form.title}
          onChange={e => setForm({ ...form, title: e.target.value })}
          required
        /><br />

        <label>Opis</label><br />
        <textarea
          value={form.description}
          onChange={e => setForm({ ...form, description: e.target.value })}
        /><br />

        <label>Lokalizacja*</label><br />
        <input
          value={form.location}
          onChange={e => setForm({ ...form, location: e.target.value })}
          required
        /><br />

        <label>Początek</label><br />
        <input
          type="datetime-local"
          value={form.start_time}
          onChange={e => setForm({ ...form, start_time: e.target.value })}
          required
        /><br />

        <label>Koniec</label><br />
        <input
          type="datetime-local"
          value={form.end_time}
          onChange={e => setForm({ ...form, end_time: e.target.value })}
        /><br />

        <label>Maks. miejsc</label><br />
        <input
          type="number"
          min={1}
          value={form.seats_limit}
          onChange={e => setForm({ ...form, seats_limit: Number(e.target.value) })}
        /><br /><br />

        <button type="submit" disabled={loading}>
          {loading ? "Tworzenie..." : "Zapisz"}
        </button>
      </form>
    </div>
  );
}
