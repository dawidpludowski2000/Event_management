"use client";

import { useRouter } from "next/navigation";

export default function BackEventListButton() {
  const router = useRouter();

  return (
    <button onClick={() => router.push("/events")}>
      Lista wydarzeń
    </button>
  );
}
