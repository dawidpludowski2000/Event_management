"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { checkIfAdmin } from "@/lib/utils/roles";

export default function AdminPanelButton() {
  const router = useRouter();
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) return;

    checkIfAdmin().then((res) => {
      setIsAdmin(res);
    });
  }, []);

  if (!isAdmin) return null;

  return (
    <button
      onClick={() => router.push("/admin-panel")}
      style={{
        backgroundColor: "#0070f3",
        color: "white",
        padding: "8px 16px",
        border: "none",
        borderRadius: "6px",
        cursor: "pointer",
        fontWeight: 500,
        marginBottom: "16px",
      }}
    >
      🛠 Panel administratora
    </button>
  );
}
