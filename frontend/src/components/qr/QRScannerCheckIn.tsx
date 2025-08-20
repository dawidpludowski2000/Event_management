"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { checkInReservation } from "@/lib/api/reservations";

// Dynamiczny import skanera (SSR off). Typy „any”, bo biblioteka bywa kapryśna w TS.
const QrReader: any = dynamic(
  () => import("react-qr-reader").then((m: any) => m.QrReader ?? m.default),
  { ssr: false, loading: () => <p>Ładowanie skanera…</p> }
);

type Props = {
  /** Wywoływane po udanym check-in (lub po symulacji). Użyj np. do refetch listy/metryk. */
  onSuccess: () => void;
  /**
   * Jeśli false, komponent NIE robi check-in od razu.
   * Zamiast tego wywoła onScannedReservationId(id) – rodzic decyduje, co dalej (np. pokazuje panel i przycisk "Potwierdź").
   * Domyślnie: true (auto check-in).
   */
  autoCheckIn?: boolean;
  /** Otrzymuje reservationId odczytane z QR w trybie manualnym (autoCheckIn=false). */
  onScannedReservationId?: (reservationId: number) => void;
};

export default function QRScannerCheckIn({
  onSuccess,
  autoCheckIn = true,
  onScannedReservationId,
}: Props) {
  const [open, setOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastText, setLastText] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);     // blokada wielokrotnych wywołań
  const [manual, setManual] = useState("");    // symulacja skanu bez kamery

  // Wspólna logika przetwarzania tekstu z QR
  const processText = async (text: string) => {
    if (busy) return;

    setLastText(text);
    const match = text.match(/Reservation:(\d+)/i);
    if (!match) {
      setError("Nieprawidłowy kod QR");
      return;
    }

    const id = Number(match[1]);

    // Tryb MANUALNY – nie robimy check-in, tylko przekazujemy ID do rodzica
    if (!autoCheckIn && onScannedReservationId) {
      setError(null);
      onScannedReservationId(id);
      // Opcjonalnie czyścimy „ostatni tekst” po chwili, by nie zasłaniał UI
      setTimeout(() => setLastText(null), 1200);
      return;
    }

    // Tryb AUTO – od razu wywołujemy check-in na backendzie
    try {
      setBusy(true);
      const resp = await checkInReservation(id);
      // TODO: można zamienić na toast
      alert(resp.detail || "Check-in wykonany.");
      setError(null);
      onSuccess();
    } catch (e) {
      setError("Błąd przy check-in");
      console.error(e);
    } finally {
      // krótki debounce, bo skaner potrafi wywołać kilka razy z tym samym wynikiem
      setTimeout(() => setBusy(false), 800);
      setTimeout(() => setLastText(null), 1200);
    }
  };

  // Callback z kamery (biblioteka różnie zwraca wynik – obsługujemy kilka kształtów)
  const handleResult = async (result: any, err: any) => {
    if (err) return; // normalne na „pustych” klatkach
    const text = result?.getText ? result.getText() : result?.text || result;
    if (!text || typeof text !== "string") return;
    await processText(text);
  };

  return (
    <div>
      <button onClick={() => setOpen(v => !v)}>
        {open ? "✖ Zamknij skaner" : "📷 Skanuj bilet"}
      </button>

      {open && (
        <div style={{
          width: 360,
          maxWidth: "100%",
          marginTop: 12,
          border: "2px dashed #999",
          borderRadius: 8,
          padding: 10
        }}>
          <p style={{ margin: 0, fontSize: 12, opacity: 0.8 }}>
            {error ? "❌ " + error : "🎥 Kamera aktywna — pokaż kod QR"}
          </p>

          <QrReader
            constraints={{ facingMode: "environment" }}
            onResult={handleResult}
            videoStyle={{ width: "100%" }}
          />

          {lastText && (
            <p style={{ fontSize: 12, marginTop: 8 }}>
              ✅ Odczytano: <code>{lastText}</code>
            </p>
          )}

          {/* Symulacja skanu bez kamery (np. desktop bez HTTPS) */}
          <div style={{ marginTop: 10 }}>
            <input
              value={manual}
              onChange={e => setManual(e.target.value)}
              placeholder='Wklej tekst QR, np. "Reservation:123"'
              style={{ width: "100%" }}
            />
            <button
              onClick={() => processText(manual)}
              style={{ marginTop: 6 }}
              disabled={!manual.trim()}
            >
              ▶ Symuluj skan (bez kamery)
            </button>
          </div>

          <p style={{ marginTop: 8, fontSize: 11, opacity: 0.7 }}>
            Uwaga: dostęp do kamery działa na HTTPS lub na http://localhost.
          </p>
        </div>
      )}
    </div>
  );
}
