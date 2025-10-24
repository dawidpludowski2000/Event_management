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

export async function checkIfAdmin(): Promise<boolean> {
  try {
    const res = await authFetch(`/api/users/me/`);
    const json = await res.json().catch(() => ({}));

    if (!res.ok || json.success === false) return false;

    return json.data?.is_staff === true;
  } catch (err) {
    console.error("checkIfAdmin error:", err);
    return false;
  }
}
