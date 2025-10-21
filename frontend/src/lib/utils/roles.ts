import { authFetch } from "@/lib/api/http";

export async function checkIfOrganizer(): Promise<boolean> {
  try {
    const res = await authFetch(`/api/events/is-organizer/`);
    const json = await res.json().catch(() => ({}));

    if (!res.ok || json.success === false) return false;

    return json.data?.is_organizer === true;
  } catch (err) {
    console.error("checkIfOrganizer error:", err);
    return false;
  }
}
