"use client";

import { useEffect, useState } from "react";
import { activateAccount } from "@/lib/api/auth";

export function useActivateAccount(token: string | undefined) {
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("Aktywuję konto...");
  const [success, setSuccess] = useState<boolean | null>(null);

  useEffect(() => {
    if (!token) return;

    const activate = async () => {
      try {
        const data = await activateAccount(token);
        if (data.success) {
          setMessage("✅ Konto zostało aktywowane! Możesz się teraz zalogować.");
          setSuccess(true);
        } else {
          setMessage("Nie udało się aktywować konta.");
          setSuccess(false);
        }
      } catch (err: any) {
        setMessage(err.message || "Błąd połączenia z serwerem.");
        setSuccess(false);
      } finally {
        setLoading(false);
      }
    };

    activate();
  }, [token]);

  return { loading, message, success };
}
