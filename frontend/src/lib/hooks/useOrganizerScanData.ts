import { useCallback, useEffect, useState } from "react";
import { getOrganizerMyEvents } from "@/lib/api/events";
import { getOrganizerReservations } from "@/lib/api/reservations";

export function useOrganizerScanData() {
  const [events, setEvents] = useState<any[]>([]);
  const [reservations, setReservations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchAll = useCallback(async () => {
    setLoading(true);
    try {
      const [eventsData, reservationsData] = await Promise.all([
        getOrganizerMyEvents(),
        getOrganizerReservations(),
      ]);
      setEvents(eventsData);
      setReservations(reservationsData);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAll();
  }, [fetchAll]);

  return { events, reservations, loading, fetchAll };
}
