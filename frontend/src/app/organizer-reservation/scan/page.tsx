"use client";

import { useEffect, useMemo, useState, useCallback } from "react";
import BackOrganizerPanelButton from "@/components/buttons/events-buttons/BackOrganizerPanelButton";
import QRScannerCheckIn from "@/components/qr/QRScannerCheckIn";
import { getOrganizerMyEvents } from "@/lib/api/events";
import { getOrganizerReservations, checkInReservation } from "@/lib/api/reservations";
import { inspectReservation } from "@/lib/api/reservations";
import { checkIfOrganizer } from "@/lib/utils/roles";
import { useRouter } from "next/navigation";

type Resv = {
  reservation_id: number;
  event_id: number;
  user_email: string;
  status: "pending" | "confirmed" | "rejected";
  checked_in: boolean;
  created_at: string;
  event_title: string;
  event_start_time: string;
};

export default function ScanPage() {
  const router = useRouter();
  const [events, setEvents] = useState<any[]>([]);
  const [resvs, setResvs] = useState<Resv[]>([]);
  const [loading, setLoading] = useState(true);

  // panel po prawej (ostatnio zeskanowana rezerwacja)
  const [inspectingId, setInspectingId] = useState<number | null>(null);
  const [inspecting, setInspecting] = useState<any | null>(null);  // dane z inspect endpointu
  const [inspectErr, setInspectErr] = useState<string | null>(null);
  const [busyConfirm, setBusyConfirm] = useState(false);

  const fetchAll = useCallback(async () => {
    const [E, R] = await Promise.all([getOrganizerMyEvents(), getOrganizerReservations()]);
    setEvents(E);
    setResvs(R);
    setLoading(false);
  }, []);

  useEffect(() => {
    (async () => {
      if (!(await checkIfOrganizer())) { router.push("/login"); return; }
      fetchAll();
    })();
  }, [fetchAll, router]);

  // liczenie „pozostało do check-inu” = confirmed − checked_in
  const remainingByEvent = useMemo(() => {
    const map: Record<number, { confirmed: number; checkedIn: number; remaining: number }> = {};
    for (const e of events) map[e.id] = { confirmed: 0, checkedIn: 0, remaining: 0 };
    for (const r of resvs) {
      if (!(r.event_id in map)) continue;
      if (r.status === "confirmed") map[r.event_id].confirmed += 1;
      if (r.checked_in) map[r.event_id].checkedIn += 1;
    }
    for (const id of Object.keys(map)) {
      const m = map[+id];
      m.remaining = Math.max(0, m.confirmed - m.checkedIn);
    }
    return map;
  }, [events, resvs]);

  // po zeskanowaniu dostajemy reservationId → pokaż panel z danymi
  const handleScanned = async (reservationId: number) => {
    setInspectingId(reservationId);
    setInspecting(null);
    setInspectErr(null);
    try {
      const data = await inspectReservation(reservationId);
      setInspecting(data);
    } catch (e: any) {
      setInspectErr(e?.message || "Nie udało się pobrać danych rezerwacji.");
    }
  };

  const confirmCheckIn = async () => {
    if (!inspectingId) return;
    try {
      setBusyConfirm(true);
      await checkInReservation(inspectingId);
      setInspectErr(null);
      // odśwież listy/liczniki
      await fetchAll();
      // wyczyść panel
      setInspectingId(null);
      setInspecting(null);
      alert("Check-in wykonany.");
    } catch (e: any) {
      setInspectErr(e?.message || "Nie udało się wykonać check-in.");
    } finally {
      setBusyConfirm(false);
    }
  };

  if (loading) return <p>⏳ Ładowanie…</p>;
  if (!events.length) return <p>Nie masz jeszcze wydarzeń.</p>;

  return (
    <div style={{ maxWidth: 1100, margin: "0 auto", padding: 12 }}>
      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <BackOrganizerPanelButton />
        <h1 style={{ margin: 0 }}>Skaner biletów</h1>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginTop: 12 }}>
        {/* LEWA: lista eventów z licznikami */}
        <div>
          <h3>Twoje wydarzenia</h3>
          <ul>
            {events.map((e: any) => {
              const m = remainingByEvent[e.id] || { remaining: 0 };
              return (
                <li key={e.id} style={{ marginBottom: 8 }}>
                  <strong>{e.title}</strong> — {e.start_time} — {e.location}
                  <div>(Pozostało do check-inu: <b>{m.remaining}</b>)</div>
                </li>
              );
            })}
          </ul>
        </div>

        {/* PRAWA: skaner + panel sprawdzanej rezerwacji */}
        <div>
          <QRScannerCheckIn
            onSuccess={fetchAll}              // gdyby autoCheckIn=true
            autoCheckIn={false}               // ← tryb manualny (najpierw podgląd)
            onScannedReservationId={handleScanned}
          />

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
                  <button onClick={confirmCheckIn} disabled={busyConfirm || inspecting.checked_in}>
                    Potwierdź
                  </button>
                  <button onClick={() => { setInspectingId(null); setInspecting(null); setInspectErr(null); }}>
                    Anuluj
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <p style={{ marginTop: 12, fontSize: 12, opacity: 0.7 }}>
        Uwaga: skaner wymaga HTTPS (lub http://localhost). Na telefonie użyj wersji z HTTPS.
      </p>
    </div>
  );
}
