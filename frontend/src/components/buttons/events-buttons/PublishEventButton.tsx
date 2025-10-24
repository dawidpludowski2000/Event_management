"use client";
import { publishEvent } from "@/lib/api/events";
import { toast } from "react-hot-toast";

export default function PublishEventButton({
  eventId,
  onSuccess,
}: {
  eventId: number;
  onSuccess: () => void;
}) {
  const onClick = async () => {
    const res = await publishEvent(eventId);
    const data = await res.json().catch(() => ({}));
    if (res.ok) {
      toast.success(data.detail || "Wydarzenie zostało opublikowane ✅");
      onSuccess();
    } else {
      toast.error(data.detail || "Nie udało się opublikować wydarzenia ❌");
    }
  };

  return <button onClick={onClick}>Opublikuj</button>;
}
