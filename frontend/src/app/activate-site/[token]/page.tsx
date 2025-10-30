"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect } from "react";
import { useActivateAccount } from "@/lib/hooks/useActivateAccount";
import ActivationResult from "@/components/users/ActivationResult";

export default function ActivatePage() {
  const { token } = useParams<{ token: string }>();
  const router = useRouter();
  const { loading, message, success } = useActivateAccount(token);

  useEffect(() => {
    if (success) {
      const timer = setTimeout(() => router.push("/login"), 3000);
      return () => clearTimeout(timer);
    }
  }, [success, router]);

  return (
    <ActivationResult loading={loading} message={message} success={success} />
  );
}
