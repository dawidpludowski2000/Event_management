import { API_BASE_URL } from "@/lib/config";

// token automatycznie pobierany, inne funkcje nie muszą go przyjmować, automatyzacja 
export async function authFetch(
  path: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  const headers = new Headers(options.headers || {});
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });

  if (res.status === 401) {
    // token nieważny/niepoprawny → wyloguj i przenieś na /login
    if (typeof window !== "undefined") {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";
    }
  }

  return res;
}
