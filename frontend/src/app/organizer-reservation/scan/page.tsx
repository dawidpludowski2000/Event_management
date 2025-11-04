"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import BackOrganizerPanelButton from "@/components/buttons/events-buttons/BackOrganizerPanelButton";
import QRScannerCheckIn from "@/components/qr/QRScannerCheckIn";
import { checkIfOrganizer } from "@/lib/utils/roles";
import { checkInReservation, inspectReservation } from "@/lib/api/reservations";
import { useOrganizerScanData } from "@/lib/hooks/useOrganizerScanData";
import EventListForScanner from "@/components/event-info/EventListForScanner";
import InspectReservationPanel from "@/components/reservations/InspectReservationPanel";

export default function Page() {
  const router = useRouter();
  const { events, loading, fetchAll } = useOrganizerScanData();

  const [inspectingId, setInspectingId] = useState<number | null>(null);
  const [inspecting, setInspecting] = useState<any | null>(null);
  const [inspectErr, setInspectErr] = useState<string | null>(null);
  const [busyConfirm, setBusyConfirm] = useState(false);

  // sprawdzenie roli organizatora
  useEffect(() => {
    (async () => {
      if (!(await checkIfOrganizer())) {
        router.push("/login");
      }
    })();
  }, [router]);

  // po zeskanowaniu
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
      await fetchAll();
      setInspectingId(null);
      setInspecting(null);
      alert("Check-in wykonany ✅");
    } catch (e: any) {
      setInspectErr(e?.message || "Nie udało się wykonać check-in.");
    } finally {
      setBusyConfirm(false);
    }
  };

  return (
    <div style={{ maxWidth: 1100, margin: "0 auto", padding: 12 }}>
      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <BackOrganizerPanelButton />
        <h1 style={{ margin: 0 }}>Skaner biletów</h1>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 16,
          marginTop: 12,
        }}
      >
        {/* LEWA: lista eventów */}
        <EventListForScanner events={events} loading={loading} />

        {/* PRAWA: skaner + panel sprawdzanej rezerwacji */}
        <div>
          <QRScannerCheckIn
            onSuccess={fetchAll}
            autoCheckIn={false}
            onScannedReservationId={handleScanned}
          />

          <InspectReservationPanel
            inspectingId={inspectingId}
            inspecting={inspecting}
            inspectErr={inspectErr}
            busyConfirm={busyConfirm}
            onConfirm={confirmCheckIn}
            onCancel={() => {
              setInspectingId(null);
              setInspecting(null);
              setInspectErr(null);
            }}
          />
        </div>
      </div>

      <p style={{ marginTop: 12, fontSize: 12, opacity: 0.7 }}>
        Uwaga: skaner wymaga HTTPS (lub http://localhost). Na telefonie użyj
        wersji z HTTPS.
      </p>
    </div>
  );
}
