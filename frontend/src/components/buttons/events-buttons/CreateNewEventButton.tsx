"use client";

import { useRouter } from "next/navigation";
import { use } from "react";


export default function CreateNewEventButton() {
    const router = useRouter();

    return (
      <button onClick={() => router.push("/organizer-create-new-events")}>
      + Stwórz nowe wydarzenie
    </button>
  );
}
