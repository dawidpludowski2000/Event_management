"use client";
import { cancelEvent } from "@/lib/api/events";
import { toast } from "react-hot-toast";

export default function CancelEventButton({
  eventId,
  onSuccess,
}: {
  eventId: number;
  onSuccess: () => void;
}) {
  const onClick = async () => {
    if (!confirm("Na pewno anulować wydarzenie? Uczestnicy stracą rezerwacje.")) return;

    const res = await cancelEvent(eventId);
    const data = await res.json().catch(() => ({}));
    if (res.ok) {
      toast.success(data.detail || "Wydarzenie anulowane");
      onSuccess();
    } else {
      toast.error(data.detail || "Nie udało się anulować");
    }
  };

  return <button onClick={onClick}>Anuluj</button>;
}
