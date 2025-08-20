"use client";

import { useRouter } from "next/navigation";

export default function RegisterButton() {
  const router = useRouter();

  return (
    <button onClick={() => router.push("/register")}>
      Zarejestruj się
    </button>
  );
}
