import { API_BASE_URL } from "@/lib/config";
import { authFetch } from "@/lib/api/http";


export async function getAllEvents(): Promise<any[]> {
  const res = await authFetch(`/api/events/`);
  if (!res.ok) throw new Error("Błąd pobierania wydarzeń");
  const data = await res.json();
  return data.results;
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
  if (!res.ok) throw new Error("Błąd pobierania dostępnych miejsc");
  return await res.json();
}


export async function createNewEvent(payload: {
  title: string;
  description?: string;
  location: string;
  start_time: string; // ISO string
  end_time: string;   // ISO string
  seats_limit: number;

}): Promise<Response> {
  return authFetch(`/api/events/organizer/events/create/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}



export async function getOrganizerMyEvents(): Promise<any[]> {
  const res = await authFetch(`/api/events/organizer/my-events-list/`);
  if (!res.ok) throw new Error("Błąd pobierania listy moich wydarzeń");
  const data = await res.json();
  return data.results ?? data;
}


export async function updateOrganizerEvent(eventId: number, payload: any): Promise<any> {
  const res = await authFetch(`/api/events/organizer/${eventId}/edit/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Błąd edycji wydarzenia");
  }

  return res.json();
}



export async function publishEvent(eventId: number): Promise<Response> {
  return authFetch(`/api/events/organizer/${eventId}/publish/`, {
    method: "POST",
  });
}


export async function cancelEvent(eventId: number): Promise<Response> {
  return authFetch(`/api/events/organizer/${eventId}/cancel/`, {
    method: "POST",
  });
}
