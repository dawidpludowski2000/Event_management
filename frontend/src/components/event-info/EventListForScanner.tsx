"use client";

import LiveEventMetrics from "@/components/event-info/LiveEventMetrics";

interface EventListForScannerProps {
  events: any[];
  loading: boolean;
}

export default function EventListForScanner({ events, loading }: EventListForScannerProps) {
  if (loading) return <p>⏳ Ładowanie wydarzeń…</p>;

  if (!events || events.length === 0)
    return <p>Nie masz jeszcze żadnych wydarzeń do skanowania.</p>;

  return (
    <div>
      <h3>Twoje wydarzenia</h3>
      <ul>
        {events.map((e) => (
          <li key={e.id} style={{ marginBottom: 8 }}>
            <strong>{e.title}</strong> — {e.start_time} — {e.location}
            <div style={{ marginTop: 4 }}>
              <LiveEventMetrics eventId={e.id} />
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
