"use client";
import { useEventMetricsWS } from "@/lib/hooks/useEventMetricsWS";

export default function LiveEventMetrics({ eventId }: { eventId: number }) {
  const m = useEventMetricsWS(eventId);
  if (!m) {
    return <div style={{ fontSize: 12, opacity: 0.7 }}>LIVE: czekam na dane…</div>;
  }
  return (
    <div style={{ fontSize: 12 }}>
      LIVE — potw.: <b>{m.confirmed_count}</b>, oczek.: <b>{m.pending_count}</b>, check-in:{" "}
      <b>{m.checked_in_count}</b>, wolne: <b>{m.spots_left}</b>
    </div>
  );
}
