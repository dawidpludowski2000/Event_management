// jedno źródło prawdy na adres backendu (dev/prod)
const FALLBACK = "http://localhost:8000";
export const API_BASE_URL =
  (process.env.NEXT_PUBLIC_API_BASE_URL && process.env.NEXT_PUBLIC_API_BASE_URL.trim()) || FALLBACK;

