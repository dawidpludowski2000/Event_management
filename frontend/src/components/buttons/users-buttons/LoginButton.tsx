"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { loginUser } from "@/lib/api/auth";
import { toast } from "react-hot-toast";

interface Props {
  email: string;
  password: string;
}

export default function LoginButton({ email, password }: Props) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!email || !password) {
      toast.error("Podaj e-mail i hasło.");
      return;
    }

    try {
      setLoading(true);
      const data = await loginUser(email, password);
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      toast.success("Zalogowano pomyślnie! 🎉");
      router.push("/events");
    } catch (err: any) {
      toast.error(err.message || "Błąd logowania.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleLogin} disabled={loading}>
      {loading ? "Logowanie..." : "Zaloguj"}
    </button>
  );
}
