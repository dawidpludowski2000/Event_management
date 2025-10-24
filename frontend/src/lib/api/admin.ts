import { authFetch } from "@/lib/api/http";

export async function getAllUsers(): Promise<any[]> {
  const res = await authFetch(`/api/users/admin/users/`);
  if (!res.ok) throw new Error("Błąd pobierania użytkowników.");
  const data = await res.json();
  return data.data || data.results || data;
}

export async function setOrganizerRole(
  userId: number,
  isOrganizer: boolean
): Promise<Response> {
  return authFetch(`/api/users/admin/users/${userId}/set-organizer/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ is_organizer: isOrganizer }),
  });
}
