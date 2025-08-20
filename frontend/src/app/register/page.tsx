"use client";

import { useState } from "react";
import RegisterButton from "@/components/buttons/users-buttons/RegisterButton";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");   // opcjonalne
  const [lastName, setLastName] = useState("");     // opcjonalne

  return (
    <form>
      <h1>Rejestracja</h1>

      <div>
        <label htmlFor="email">Email*</label><br />
        <input
          id="email"
          type="email"
          placeholder="np. jan@wp.pl"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete="email"
        />
      </div>

      <div>
        <label htmlFor="password">Hasło*</label><br />
        <input
          id="password"
          type="password"
          placeholder="Twoje hasło"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          autoComplete="new-password"
        />
      </div>

      <div>
        <label htmlFor="first_name">Imię (opcjonalnie)</label><br />
        <input
          id="first_name"
          type="text"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          autoComplete="given-name"
        />
      </div>

      <div>
        <label htmlFor="last_name">Nazwisko (opcjonalnie)</label><br />
        <input
          id="last_name"
          type="text"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          autoComplete="family-name"
        />
      </div>

      <RegisterButton
        email={email}
        password={password}
        firstName={firstName || undefined}
        lastName={lastName || undefined}
      />
    </form>
  );
}
