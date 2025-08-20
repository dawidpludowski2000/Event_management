"use client";

import { useEventAvailability } from "@/lib/hooks/useEventAvailability";

interface Props {
  eventId: number;
  seatsLimit: number;
}

export default function EventAvailability({ eventId, seatsLimit }: Props) {
  const { spotsLeft, loading } = useEventAvailability(eventId);

  if (loading) return <p>⏳ Ładowanie miejsc...</p>;
  if (spotsLeft === null) return <p>Nie można pobrać dostępnych miejsc</p>;

  return (
    <p>
      Pozostało <strong>{spotsLeft}</strong> / {seatsLimit} miejsc
    </p>
  );
}
