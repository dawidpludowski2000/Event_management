import { API_BASE_URL } from "@/lib/config";
import { authFetch } from "@/lib/api/http";

export async function cancelReservation(reservationId: number): Promise<Response> {
  return authFetch(`/api/reservations/${reservationId}/`, {
    method: "DELETE",
  });
}

export async function confirmReservation(reservationId: number): Promise<Response> {
  return authFetch(`/api/reservations/${reservationId}/status/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: "confirmed" }),
  });
}

export async function rejectReservation(reservationId: number): Promise<Response> {
  return authFetch(`/api/reservations/${reservationId}/status/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: "rejected" }),
  });
}

export async function getMyReservations(): Promise<any[]> {
  const res = await authFetch(`/api/my-reservations/`);
  if (!res.ok) throw new Error("Błąd pobierania rezerwacji");
  return await res.json();
}

export async function getOrganizerReservations(): Promise<any[]> {
  const res = await authFetch(`/api/organizer/reservations/`);
  if (!res.ok) throw new Error("Błąd podczas pobierania rezerwacji");
  return await res.json();
}

export async function downloadTicket(reservationId: number): Promise<Blob> {
  const res = await authFetch(`/api/reservations/${reservationId}/ticket/`);
  if (!res.ok) throw new Error("Nie udało się pobrać biletu");
  return await res.blob();
}

// Funkcja do skanowania biletu
export async function checkInReservation(reservationId: number): Promise<{
  detail: string;
  checked_in: boolean;
  reservation_id: number;
}> {
  const res = await authFetch(`/api/reservations/${reservationId}/check-in/`, {
    method: "POST",
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data?.detail || "Błąd podczas check-in");
  return data;
}

//
export async function inspectReservation(reservationId: number): Promise<any> {
  const res = await authFetch(`/api/reservations/${reservationId}/inspect/`);
  if (!res.ok) throw new Error("Nie udało się pobrać danych rezerwacji");
  return res.json();
}
