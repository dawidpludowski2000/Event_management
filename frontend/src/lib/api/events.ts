import { API_BASE_URL } from "@/lib/config";
import { authFetch } from "@/lib/api/http";

export async function getAllEvents(): Promise<any[]> {
  const res = await authFetch(`/api/events/`);
  const json = await res.json().catch(() => ({}));

  if (!res.ok || json.success === false) {
    throw new Error(json.message || "Błąd pobierania wydarzeń");
  }

  return json.data?.results || json.data || [];
}


export async function registerToEvent(eventId: number): Promise<Response> {
  return authFetch(`/api/events/${eventId}/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
}

export async function getSeatsAvailability(eventId: number): Promise<any> {
  const res = await authFetch(`/api/events/${eventId}/availability/`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  const json = await res.json().catch(() => ({}));

  if (!res.ok || json.success === false) {
    throw new Error(json.message || "Błąd pobierania dostępnych miejsc");
  }

  return json.data || {};
}

export async function createNewEvent(payload: {
  title: string;
  description?: string;
  location: string;
  start_time: string;
  end_time: string;
  seats_limit: number;
}): Promise<Response> {
  return authFetch(`/api/events/organizer/events/create/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function getOrganizerMyEvents(): Promise<any[]> {
  const res = await authFetch(`/api/events/organizer/my-events-list/`);
  const json = await res.json().catch(() => ({}));

  if (!res.ok || json.success === false) {
    throw new Error(json.message || "Błąd pobierania listy moich wydarzeń");
  }

  return json.data?.results || json.data || [];
}

export async function updateOrganizerEvent(eventId: number, payload: any): Promise<any> {
  const res = await authFetch(`/api/events/organizer/${eventId}/edit/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const json = await res.json().catch(() => ({}));

  if (!res.ok || json.success === false) {
    throw new Error(json.message || "Błąd edycji wydarzenia");
  }

  return json.data || {};
}

export async function publishEvent(eventId: number): Promise<Response> {
  return authFetch(`/api/events/organizer/${eventId}/publish/`, { method: "POST" });
}

export async function cancelEvent(eventId: number): Promise<Response> {
  return authFetch(`/api/events/organizer/${eventId}/cancel/`, { method: "POST" });
}
