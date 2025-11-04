EventFlow – Backend

System zarządzania wydarzeniami z rejestracją użytkowników, rolami (User / Organizer / Admin), kolejką rezerwacji, QR-biletami i metrykami na żywo.
Aplikacja oparta na Django REST Framework i Channels, w pełni zintegrowana z Dockerem i Redisem.

Główne funkcjonalności

• Rejestracja z aktywacją konta przez e-mail (SMTP)
• Logowanie i autoryzacja JWT (access / refresh)
• Role użytkowników: User, Organizer, Admin
• Tworzenie i publikacja wydarzeń (draft → published → cancelled)
• Rezerwacje z kolejką oczekujących (pending / confirmed / rejected)
• QR-bilety i check-in przez organizatora (z generacją PDF)
• Live metryki (confirmed, pending, checked-in, spots-left) – WebSocket / Django Channels / Redis
• Panel organizatora (zarządzanie wydarzeniami i rezerwacjami)
• Panel administratora (nadawanie ról)
• Logowanie błędów i Sentry (DSN opcjonalny)
• Healthcheck i spójna architektura API (Clean Architecture + SRP)

Struktura projektu

backend/
│ config/
│ ├ asgi.py → ASGI + WebSocket routing
│ ├ settings.py
│ ├ core/api_response.py → standard success()/error() API responses
│ └ urls.py
│
├ users/ → rejestracja, logowanie, aktywacja, role
├ events/ → tworzenie, publikacja, websocket metrics
├ reservations/ → rezerwacje, check-in, QR ticket
├ requirements.txt
└ Dockerfile

Każdy moduł ma oddzielone warstwy: serializers, views, services, permissions (zgodnie z zasadą SRP).

Uruchomienie lokalne (Docker Compose)

Wymagania: Docker i Docker Compose

Skopiuj plik .env.dev i zmień jego nazwę na .env

Uruchom kontenery poleceniem:

docker compose up --build

Backend będzie dostępny pod adresem: http://localhost:8000

Redis uruchamia się automatycznie (kanał warstwa Channels)

Po pierwszym starcie wykonaj migracje:

docker compose exec backend python manage.py migrate

(Opcjonalnie) utwórz konto administratora:

docker compose exec backend python manage.py createsuperuser

Środowisko i konfiguracja (.env)

DJANGO_SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=http://localhost:3000

CSRF_TRUSTED_ORIGINS=http://localhost:3000

DATABASE_URL=postgresql://eventflow:eventflow@db:5432/eventflow
REDIS_URL=redis://redis:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
DEFAULT_FROM_EMAIL="Events App noreply@example.com
"
FRONTEND_ACTIVATION_URL=http://localhost:8000

SENTRY_DSN=

Kluczowe endpointy API

Użytkownicy
POST /api/users/register/ – rejestracja + wysyłka maila aktywacyjnego
GET /api/users/activate/<token>/ – aktywacja konta
POST /api/login/ – JWT login
POST /api/token/refresh/ – odświeżenie tokena

Wydarzenia
GET /api/events/ – lista publicznych wydarzeń
POST /api/events/organizer/events/create/ – tworzenie eventu
PATCH /api/events/organizer/<id>/edit/ – edycja eventu
POST /api/events/organizer/<id>/publish/ – publikacja

Rezerwacje
POST /api/events/<event_id>/register/ – zarezerwuj miejsce
GET /api/my-reservations/ – moje rezerwacje
GET /api/organizer/reservations/<id>/inspect/ – podgląd rezerwacji (QR / ID)
POST /api/reservations/<id>/check-in/ – potwierdzenie wejścia
GET /api/reservations/<id>/ticket/ – pobranie QR-biletu (PDF)

WebSocket
/ws/events/<event_id>/ – live metryki wydarzenia

Przykładowe dane wysyłane przez Channels:
{
"type": "metrics",
"event_id": 2,
"confirmed_count": 12,
"pending_count": 3,
"checked_in_count": 7,
"spots_left": 38
}

Dokumentacja API

Swagger UI: http://localhost:8000/api/schema/swagger-ui/

ReDoc: http://localhost:8000/api/schema/redoc/

Produkcja i bezpieczeństwo

• Uruchamiaj z DEBUG=False
• Ustaw ALLOWED_HOSTS i CSRF_TRUSTED_ORIGINS
• Nie commituj pliku .env
• Nie używaj CORS_ALLOW_ALL_ORIGINS = True
• Hasła i klucze trzymaj poza repozytorium
• Backend działa jako ASGI app (Daphne lub Uvicorn) za reverse-proxy (np. nginx)
• Redis wymagany do obsługi Channels / WebSocketów
• Można włączyć Sentry (SENTRY_DSN) do logowania błędów

Testy

Uruchom testy jednostkowe:

docker compose exec backend pytest -q


  Typowy przepływ

1. Użytkownik rejestruje się → otrzymuje link aktywacyjny e-mailem

2. Po aktywacji może się zalogować (JWT)

3. Organizer tworzy wydarzenie → publikuje

4. Użytkownicy rezerwują miejsca

5. Organizer potwierdza / odrzuca zgłoszenia

6. W dniu wydarzenia skanuje QR kod z biletu i potwierdza check-in

7. WebSocket aktualizuje metryki w czasie rzeczywistym