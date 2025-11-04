EventFlow – Frontend

Frontend aplikacji EventFlow, zbudowany w Next.js (TypeScript + React + Tailwind).
System zapewnia pełny przepływ użytkownika: rejestracja, logowanie JWT, tworzenie wydarzeń, rezerwacje, panel organizatora i administratora oraz obsługę QR-check-in z metrykami w czasie rzeczywistym.

Główne funkcjonalności

• Rejestracja użytkowników z linkiem aktywacyjnym (Gmail SMTP z backendu)
• Logowanie i wylogowanie przez JWT (access / refresh token)
• Widok publiczny wydarzeń (lista i szczegóły)
• Panel użytkownika: lista własnych rezerwacji
• Panel organizatora: zarządzanie wydarzeniami, potwierdzanie rezerwacji, check-in
• Skaner QR kodów z podglądem i akcją "check-in"
• Live metryki wydarzenia (WebSocket – Channels/Redis)
• Panel administratora (nadawanie ról)
• Toasty potwierdzeń akcji (react-hot-toast)
• Routing z ochroną stron prywatnych
• Czysta struktura kodu według zasady SRP (Single Responsibility Principle)

Struktura projektu

frontend/
│ app/ → strony (Next.js App Router)
│ ├ login/ → logowanie
│ ├ register/ → rejestracja
│ ├ events/ → lista i szczegóły wydarzeń
│ ├ my-reservations/ → rezerwacje użytkownika
│ ├ organizer-reservation/ → panel organizatora
│ ├ admin-panel/ → panel administratora
│ └ layout.tsx → wspólny layout aplikacji
│
├ components/ → komponenty UI (formularze, przyciski, listy, QRScanner)
├ lib/
│ ├ api/ → funkcje do komunikacji z backendem
│ ├ hooks/ → logika i hooki (useEventMetricsWS, useOrganizerScanData)
│ └ utils/ → funkcje pomocnicze (token handling, role, fetch wrapper)
│
├ public/ → grafiki, favicon, itp.
├ Dockerfile
└ package.json

Uruchomienie lokalne (Docker Compose)

Wymagania: Docker i Docker Compose

Skopiuj plik ".env.dev" i zmień jego nazwę na ".env"

Uruchom kontenery poleceniem:
docker compose up --build

Frontend uruchomi się automatycznie na http://localhost:3000

Komunikacja z backendem odbywa się przez zmienną środowiskową NEXT_PUBLIC_API_BASE_URL (np. http://backend:8000
)

Środowisko (.env)

NEXT_PUBLIC_API_BASE_URL=http://backend:8000

NEXT_PUBLIC_WS_BASE_URL=ws://backend:8000
NEXT_PUBLIC_BACKEND_HEALTHCHECK=http://backend:8000/healthcheck/

Główne zależności

• Next.js 15 (App Router)
• React 19
• TypeScript
• Tailwind CSS
• react-hot-toast (powiadomienia)
• react-qr-reader (skanowanie QR kodów)
• lucide-react (ikony)
• Axios (fetch wrapper w lib/api)

Routing i widoki

Publiczne:

/login – logowanie JWT

/register – rejestracja

/events – lista dostępnych wydarzeń

Użytkownik:

/my-reservations – lista własnych rezerwacji

Organizer:

/organizer-reservation – podgląd rezerwacji + akcje

/organizer-reservation/scan – skaner QR + check-in

/organizer-edit-my-events – edycja wydarzenia

Administrator:

/admin-panel – nadawanie ról i zarządzanie użytkownikami

Dodatkowe:

Autoryzacja i role

Autoryzacja działa w oparciu o JWT tokeny zapisane w localStorage.
Każda strona chroniona wykorzystuje helper "checkIfOrganizer" lub "checkIfAdmin" (z pliku lib/utils/roles.ts).
Tokeny są automatycznie przekazywane w nagłówkach przez "authFetch()" (lib/utils/fetchWrapper.ts).

WebSocket i metryki

Komunikacja z backendem ("/ws/events/<event_id>/") realizowana przez hook:
useEventMetricsWS.ts

Dane aktualizują się w czasie rzeczywistym przy każdej zmianie rezerwacji lub check-in.
Hook useOrganizerScanData.ts synchronizuje dane skanera i listy wydarzeń.

Uruchomienie bez Dockera (tryb dev)

Zainstaluj zależności:
npm install

Utwórz plik ".env.local" i ustaw adres backendu:
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

Uruchom dev serwer:
npm run dev

Build produkcyjny (CI/CD)

Lint i testy typów:
npm run lint
npm run type-check

Build:
npm run build

Start serwera (Node.js):
npm start

Projekt wspiera pipeline CI (GitHub Actions) z krokami:
• instalacja zależności
• lint / typecheck / build
• ewentualny deploy na Vercel

Testowanie (E2E / Manualne)

Typowy przepływ testowy (manualny):

Rejestracja nowego użytkownika

Aktywacja konta przez link e-mail

Logowanie JWT

Organizator tworzy i publikuje wydarzenie

Użytkownik dokonuje rezerwacji

Organizator potwierdza / odrzuca zgłoszenie

Skanowanie QR kodu i check-in

Metryki aktualizują się w czasie rzeczywistym

Produkcja / Deploy

• Backend uruchomiony w Dockerze (Railway / Render / Fly.io)
• Frontend wdrożony na Vercel (automatyczny build z GitHub Actions)
• Warto ustawić zmienne środowiskowe w Vercel:
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url

NEXT_PUBLIC_WS_BASE_URL=wss://your-backend-url