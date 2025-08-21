import { useEffect, useState } from "react";

export type EventMetrics = {
  confirmed_count: number;
  pending_count: number;
  checked_in_count: number;
  spots_left: number;
};

function wsBase(): string {
  const env = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
  try {
    const u = new URL(env);
    u.protocol = u.protocol === "https:" ? "wss:" : "ws:";
    u.pathname = "";
    return u.origin;
  } catch {
    if (typeof window !== "undefined") {
      const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
      return `${proto}//${window.location.host}`;
    }
    return "ws://localhost:8000";
  }
}

export function useEventMetricsWS(eventId: number) {
  const [metrics, setMetrics] = useState<EventMetrics | null>(null);

  useEffect(() => {
    if (!eventId) return;
    const ws = new WebSocket(`${wsBase()}/ws/events/${eventId}/`);

    ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        if (data?.type === "metrics") {
          setMetrics({
            confirmed_count: data.confirmed_count ?? 0,
            pending_count: data.pending_count ?? 0,
            checked_in_count: data.checked_in_count ?? 0,
            spots_left: data.spots_left ?? 0,
          });
        }
      } catch {
        /* ignore bad payloads */
      }
    };

    return () => ws.close();
  }, [eventId]);

  return metrics;
}
