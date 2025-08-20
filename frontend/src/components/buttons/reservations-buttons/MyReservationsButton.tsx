"use client";

import { useRouter } from "next/navigation";

export default function MyReservationsButton() {
  const router = useRouter();

  const handleClick = () => {
    router.push("/my-reservations");
  };

  return (
    <button onClick={handleClick}>
      Moje rezerwacje
    </button>
  );
}
