"use client";

import { Suspense } from "react";
import EditEventPageContent from "@/components/event-info/EditEventPageContent";

export default function Page() {
  return (
    <Suspense fallback={<p>Ładowanie strony edycji wydarzenia...</p>}>
      <EditEventPageContent />
    </Suspense>
  );
}
