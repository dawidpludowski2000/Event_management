import { useEffect, useState, useCallback } from "react";
import { authFetch } from "@/lib/api/http";

export function useMyReservationStatus(eventId: number) {

  const [registered, setRegistered] = useState<boolean | null>(null);
  const [isFull, setIsFull] = useState(false);
  const [freeSlots, setFreeSlots] = useState<number | null>(null);
  const [maxParticipants, setMaxParticipants] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = useCallback(async () => {
    try {
      const res = await authFetch(`/api/events/${eventId}/my-reservation/`);

      if (res.ok) {
        const json = await res.json();

        const data = json?.data ?? json; 

        setRegistered(["pending", "confirmed"].includes(data.status));
        setIsFull(data.full);
        setFreeSlots(data.free_slots);
        setMaxParticipants(data.max_participants);



        setError(null);
      } else {
        setRegistered(false);
        setIsFull(false);
        setFreeSlots(null);
        setMaxParticipants(null);
        setError("Błąd pobierania statusu.");
      }
    } catch (err) {
      console.error(err);
      setError("Błąd połączenia z API.");
    } finally {
      setLoading(false);
    }
  }, [eventId]);

  useEffect(() => {
    fetchStatus();
  }, [fetchStatus]);

  return {
    registered,
    isFull,
    freeSlots,
    maxParticipants,
    loading,
    error,
    refetch: fetchStatus,
  };
}
