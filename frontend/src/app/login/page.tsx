"use client";

import { useState } from "react";
import LoginButton from "@/components/buttons/users-buttons/LoginButton";
import RegisterButton from "@/components/buttons/users-buttons/GoToRegisterButton";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  
  
  return (
    <div style={{ maxWidth: "400px", margin: "0 auto", padding: "2rem" }}>
      <h1>Logowanie</h1>

      <label>Email:</label>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <br />

      <label>Hasło:</label>
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <br />

      <LoginButton email={email} password={password} />
      <RegisterButton />
    </div>
  );
}
