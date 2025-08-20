"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { registerUser } from "@/lib/api/auth";

interface Props {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
}

export default function RegisterButton({ email, password, firstName, lastName }: Props) {
  const router = useRouter();
  const [error, setError] = useState("");

  const handleRegister = async () => {
    try {
      await registerUser(email, password, {
        first_name: firstName,
        last_name: lastName
      });
      alert("Rejestracja zakończona sukcesem! Sprawdź e-mail aktywacyjny.");
      router.push("/login");
    } catch (err: any) {
      setError(err.message || "Błąd podczas rejestracji.");
    }
  };

  return (
    <>
      <button type="button" onClick={handleRegister}>
        Zarejestruj
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </>
  );
}
