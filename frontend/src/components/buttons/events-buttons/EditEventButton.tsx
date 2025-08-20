"use client";

import { useRouter } from "next/navigation";

interface EditEventButtonProps {
  eventId: number;
}

export default function EditEventButton({ eventId }: EditEventButtonProps) {
  const router = useRouter();
  const go = () => router.push(`/organizer-edit-my-events?eventId=${eventId}`);

  return <button onClick={go}>Edytuj wydarzenie</button>;
}
