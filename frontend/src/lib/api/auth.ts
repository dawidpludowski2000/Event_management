// lib/api/auth.ts
import { API_BASE_URL } from "@/lib/config";

export function logout(): void {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}

export async function loginUser(
  email: string,
  password: string
): Promise<{ access: string; refresh: string }> {
  const res = await fetch(`${API_BASE_URL}/api/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();

  if (!res.ok || data.success === false) {
    throw new Error(data.message || "Nieprawidłowy email lub hasło.");
  }

  return {
    access: data.data.access,
    refresh: data.data.refresh,
  };
}


// NOWA sygnatura: (email, password, opcjonalne imię/nazwisko)
export async function registerUser(
  email: string,
  password: string,
  opts?: { first_name?: string; last_name?: string }
): Promise<void> {
  const payload: Record<string, any> = { email, password };
  if (opts?.first_name) payload.first_name = opts.first_name;
  if (opts?.last_name)  payload.last_name  = opts.last_name;

  const res = await fetch(`${API_BASE_URL}/api/users/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || "Błąd rejestracji.");
  }
}
