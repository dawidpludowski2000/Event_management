import { authFetch } from "@/lib/api/http";

export async function checkIfOrganizer(): Promise<boolean> {
  try {
    const res = await authFetch(`/api/events/is-organizer/`, { method: "GET" });
    if (!res.ok) return false;
    const data = await res.json();
    return data.is_organizer === true;
  } catch (err) {
    console.error(err);
    return false;
  }
}
