"use client";

import { useRouter } from "next/navigation";


export default function CreateNewEventButton() {
    const router = useRouter();

    return (
      <button onClick={() => router.push("/organizer-create-new-events")}>
      + Stwórz nowe wydarzenie
    </button>
  );
}
