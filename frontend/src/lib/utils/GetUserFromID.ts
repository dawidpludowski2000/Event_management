export function getUserIdFromToken(token: string): number | null {
  try {
    const payloadBase64 = token.split(".")[1];
    const decodedPayload = JSON.parse(atob(payloadBase64));
    return decodedPayload.user_id || null;
  } catch (error) {
    return null;
  }
}


//  pobiera token z localStorage (tylko po stronie klienta)
export function getAccessTokenFromStorage(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}