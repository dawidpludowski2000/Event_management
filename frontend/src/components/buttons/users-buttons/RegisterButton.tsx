"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { registerUser } from "@/lib/api/auth";
import { toast } from "react-hot-toast";

interface Props {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
}

export default function RegisterButton({ email, password, firstName, lastName }: Props) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    if (!email || !password) {
      toast.error("Podaj e-mail i hasło.");
      return;
    }

    try {
      setLoading(true);
      await registerUser(email, password, {
        first_name: firstName,
        last_name: lastName,
      });
      toast.success("Rejestracja zakończona sukcesem! Sprawdź e-mail aktywacyjny 📧");
      router.push("/login");
    } catch (err: any) {
      toast.error(err.message || "Błąd podczas rejestracji.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button type="button" onClick={handleRegister} disabled={loading}>
      {loading ? "Rejestracja..." : "Zarejestruj"}
    </button>
  );
}
