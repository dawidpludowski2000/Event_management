"use client";

import { useState } from "react";
import { toast } from "react-hot-toast";
import { setOrganizerRole } from "@/lib/api/admin";

type Props = {
  userId: number;
  isOrganizer: boolean;
  onDone: () => void; // np. refetch listy
};

export default function SetOrganizerRoleButton({ userId, isOrganizer, onDone }: Props) {
  const [busy, setBusy] = useState(false);

  const nextVal = !isOrganizer;
  const label = nextVal ? "Nadaj rolę organizatora" : "Usuń rolę organizatora";

  const bg = nextVal ? "#0ea5e9" /* niebieski */ : "#ef4444" /* delikatny czerwony */;
  const hover = nextVal ? "#0284c7" : "#dc2626";

  const onClick = async () => {
    if (busy) return;
    try {
      setBusy(true);
      await setOrganizerRole(userId, nextVal);

      toast.success(nextVal ? "Nadano rolę organizatora." : "Usunięto rolę organizatora.");
      onDone();
    } catch (e: any) {
      toast.error(e?.message || "Nie udało się zapisać zmiany roli.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <button
      onClick={onClick}
      disabled={busy}
      style={{
        backgroundColor: bg,
        color: "white",
        padding: "6px 10px",
        border: "none",
        borderRadius: 6,
        cursor: busy ? "not-allowed" : "pointer",
        fontWeight: 500,
      }}
      onMouseOver={(e) => (e.currentTarget.style.backgroundColor = hover)}
      onMouseOut={(e) => (e.currentTarget.style.backgroundColor = bg)}
    >
      {busy ? "Zapisywanie…" : label}
    </button>
  );
}
