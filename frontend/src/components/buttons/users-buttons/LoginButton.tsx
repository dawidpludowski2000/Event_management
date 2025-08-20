"use client";

import { useRouter } from "next/navigation";
import { loginUser } from "@/lib/api/auth";

interface Props {
  email: string;
  password: string;
}

export default function LoginButton({ email, password }: Props) {
  const router = useRouter();

  const handleLogin = async () => {
    try {
      const data = await loginUser(email, password);
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      alert("Zalogowano pomyślnie!");
      router.push("/events");
    } catch (err: any) {
      alert(err.message);
    }
  };

  return <button onClick={handleLogin}>Zaloguj</button>;
}
