"use client";

import { useRouter } from "next/navigation";
import { logout } from "@/lib/api/auth";

export default function LogoutButton() {
  const router = useRouter();

  const handleLogout = () => {
    logout();                
    router.push("/login");   
  };

  return (
    <button onClick={handleLogout}>
      Wyloguj
    </button>
  );
}
