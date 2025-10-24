import { API_BASE_URL } from "@/lib/config";
import { toast } from "react-hot-toast";

// globalny fetch z automatyczną obsługą błędów i tokena
export async function authFetch(
  path: string,
  options: RequestInit = {}
): Promise<Response> {
  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("access_token")
      : null;

  const headers = new Headers(options.headers || {});
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });

  if (res.status === 401) {
    if (typeof window !== "undefined") {
      toast.error("Sesja wygasła. Zaloguj się ponownie.");
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";
    }
  } else if (res.status === 403) {
    toast.error("Brak uprawnień do wykonania tej akcji.");
  } else if (res.status >= 500) {
    toast.error("Błąd serwera. Spróbuj ponownie później.");
  }

  return res;
}
