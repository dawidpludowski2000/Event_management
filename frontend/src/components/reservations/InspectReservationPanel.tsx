"use client";

interface InspectReservationPanelProps {
  inspectingId: number | null;
  inspecting: any | null;
  inspectErr: string | null;
  busyConfirm: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

export default function InspectReservationPanel({
  inspectingId,
  inspecting,
  inspectErr,
  busyConfirm,
  onConfirm,
  onCancel,
}: InspectReservationPanelProps) {
  return (
    <div style={{ marginTop: 16, border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
      <h3>Sprawdzana rezerwacja</h3>

      {!inspectingId && <p>Brak — zeskanuj bilet, aby wyświetlić dane.</p>}
      {inspectErr && <p style={{ color: "red" }}>{inspectErr}</p>}

      {inspecting && (
        <div style={{ lineHeight: 1.6 }}>
          <div><b>Rezerwacja:</b> #{inspecting.reservation_id}</div>
          <div><b>Osoba:</b> {inspecting.user_first_name || "-"} {inspecting.user_last_name || "-"} ({inspecting.user_email})</div>
          <div><b>Wydarzenie:</b> {inspecting.event_title}</div>
          <div><b>Status:</b> {inspecting.status} {inspecting.checked_in && " (już check-in)"}</div>

          <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
            <button onClick={onConfirm} disabled={busyConfirm || inspecting.checked_in}>
              Potwierdź
            </button>
            <button onClick={onCancel}>
              Anuluj
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
