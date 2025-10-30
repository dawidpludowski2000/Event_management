"use client";

interface Props {
  loading: boolean;
  message: string;
  success: boolean | null;
}

export default function ActivationResult({ loading, message, success }: Props) {
  return (
    <div
      style={{
        maxWidth: 480,
        margin: "100px auto",
        padding: "2rem",
        textAlign: "center",
        borderRadius: 12,
        border: "1px solid #ddd",
        background: "#fff",
        boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
      }}
    >
      <h1>Aktywacja konta</h1>
      <p style={{ marginTop: "1rem", fontSize: "1.1rem" }}>
        {loading ? "⏳ Aktywuję konto..." : message}
      </p>

      {success && (
        <p style={{ marginTop: "2rem", color: "#0070f3" }}>
          Przekierowuję do logowania...
        </p>
      )}
    </div>
  );
}
