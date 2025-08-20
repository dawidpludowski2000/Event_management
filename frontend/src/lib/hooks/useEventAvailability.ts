import { getSeatsAvailability } from "@/lib/api/events";
import { useEffect, useState } from "react";

export function useEventAvailability(eventId: number) {
  const [spotsLeft, setSpotsLeft] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    getSeatsAvailability(eventId)
      .then((data) => {
        if (!mounted) return;
        setSpotsLeft(data.spots_left);
        setLoading(false);
      })
      .catch(() => {
        if (!mounted) return;
        setSpotsLeft(null);
        setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, [eventId]);

  return { spotsLeft, loading };
}
