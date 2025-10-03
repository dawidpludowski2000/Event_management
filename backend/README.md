# EventFlow

Projekt do zarządzania wydarzeniami: rejestracja użytkowników, tworzenie wydarzeń przez organizatorów, kolejka oczekujących, QR-bilety i metryki w czasie rzeczywistym.

## Funkcjonalności (skrót)
- Rejestracja/logowanie (JWT)
- Tworzenie wydarzeń przez organizatorów (draft → publish → cancel)
- Rezerwacje: kolejka oczekujących, potwierdzanie/odrzucanie
- QR-bilety (pobieranie PNG) i check-in przez organizatora
- Live metryki dla eventu (WebSocket / Channels)
- Wysyłka maili z ICS dla potwierdzonych rezerwacji

## Uruchomienie (dev)
1. Przejdź do katalogu `backend`.
2. Stwórz i aktywuj virtualenv:
   1. `python -m venv .venv`
   2. PowerShell: `.venv\Scripts\Activate.ps1`
   3. CMD: `.venv\Scripts\activate.bat`
3. Zainstaluj zależności:
   - `pip install -r backend/requirements.txt`
4. Uruchom serwer:
   - `python backend/manage.py runserver`

Uwaga: jeśli używasz Dockera/CI — zaktualizuj `Dockerfile` / `docker-compose` i upewnij się, że `requirements.txt` jest zaktualizowany (uruchom w aktywnym venv: `pip freeze > backend/requirements.txt`).

## API (lokalnie)
- Interaktywna dokumentacja (Swagger): `http://localhost:8000/api/docs/`
- OpenAPI schema: `http://localhost:8000/api/schema/`
- ReDoc: `http://localhost:8000/api/redoc/`

## Konfiguracja środowiska
- Wszystkie wrażliwe ustawienia (SECRET_KEY, EMAIL_*, REDIS_URL itp.) trzymaj w `.env`.
- W `config/settings.py` w produkcji ustaw:
  ```py
  DEBUG = False
  ALLOWED_HOSTS = ["twoja-domena.pl"]


Produkcyjnie używaj:

    Postgres jako DB,

    Redis dla Channels,

    serwer ASGI (Daphne/Uvicorn) za reverse-proxy (nginx).


Dodatkowe uwagi / bezpieczeństwo

    Nie zostawiaj CORS_ALLOW_ALL_ORIGINS = True w produkcji.

    Upewnij się, że SECRET_KEY nie jest w repo.

    Dodaj monitoring/logowanie (Sentry) i backup bazy w produkcji.
