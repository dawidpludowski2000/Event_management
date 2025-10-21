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
  const json = await res.json().catch(() => ({}));

  if (!res.ok || json.success === false) {
    throw new Error(json.message || "Błąd pobierania rezerwacji");
  }

  return json.data?.results || json.data || [];
}

export async function getOrganizerReservations(): Promise<any[]> {
  const res = await authFetch(`/api/organizer/reservations/`);
  const json = await res.json().catch(() => ({}));

  if (!res.ok || json.success === false) {
    throw new Error(json.message || "Błąd podczas pobierania rezerwacji");
  }

  return json.data?.results || json.data || [];
}

export async function downloadTicket(reservationId: number): Promise<Blob> {
  const res = await authFetch(`/api/reservations/${reservationId}/ticket/`);
  if (!res.ok) throw new Error("Nie udało się pobrać biletu");
  return await res.blob();
}

export async function checkInReservation(reservationId: number): Promise<{
  detail: string;
  checked_in: boolean;
  reservation_id: number;
}> {
  const res = await authFetch(`/api/reservations/${reservationId}/check-in/`, {
    method: "POST",
  });

  const json = await res.json().catch(() => ({}));
  if (!res.ok || json.success === false) {
    throw new Error(json.message || "Błąd podczas check-in");
  }

  // Backend w data.detail / data.checked_in / data.reservation_id
  return json.data || {};
}
