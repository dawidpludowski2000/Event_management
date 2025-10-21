import { API_BASE_URL } from "@/lib/config";

// globalny fetch z automatycznym tokenem i obsługą błędów wrappera
export async function authFetch(
  path: string,
  options: RequestInit = {}
): Promise<Response> {
  const token =
    typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  const headers = new Headers(options.headers || {});
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });

  // 🔒 automatyczne wylogowanie przy 401
  if (res.status === 401 && typeof window !== "undefined") {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.href = "/login";
  }

  // 🔍 sprawdzamy standardowy format odpowiedzi backendu
  try {
    const json = await res.clone().json().catch(() => ({}));
    if (json.success === false) {
      console.warn("API error:", json.message);
    }
  } catch {
    // np. przy blob (bilety PDF)
  }

  return res;
}
