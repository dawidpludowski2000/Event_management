EventFlow

Production-ready event management system with JWT authentication, role-based access (User / Organizer / Admin), QR tickets, and real-time metrics powered by Django REST and Next.js.
The project was designed to demonstrate full-stack architecture with clear separation of backend and frontend, Docker-based setup, and real-world DevOps practices.

Overview

Authentication and registration with email activation link (SMTP)

JWT login, logout, and token refresh

Roles: User, Organizer, Admin

Event creation, publishing, cancellation

Reservations with waiting list and organizer approval

QR tickets (PDF) and real-time check-in confirmation

Organizer and Admin dashboards

Live event metrics via WebSocket (Django Channels + Redis)

Full Docker Compose setup for backend, frontend, Redis, and PostgreSQL

Sentry integration (optional)

100% test coverage (pytest)

Clean architecture and SRP in both backend and frontend layers

Stack

Backend: Django REST Framework + Django Channels

Frontend: Next.js (React 19 + TypeScript + Tailwind CSS)

Database: PostgreSQL

Caching / Realtime: Redis

DevOps: Docker Compose (dev + prod), GitHub Actions CI/CD

Mail: Gmail SMTP (for account activation)

Key Features

User registration with activation email

JWT login and refresh tokens

Organizer event management (create, publish, cancel)

Reservation workflow (pending / confirmed / rejected)

PDF QR ticket generation

Organizer check-in with QR scanner

Live event metrics (confirmed, pending, checked-in, spots-left)

Role-based access control

Admin role management panel

Clean folder structure and separation of logic (SRP)

Run the project (Docker Compose)

Clone the repository

Copy .env.dev → .env

Run containers:
docker compose up --build

Backend: http://localhost:8000

Frontend: http://localhost:3000

Swagger API docs: http://localhost:8000/api/schema/swagger-ui/

Redis and PostgreSQL run automatically through Docker

Typical user flow

User registers and receives activation email

After activation, logs in via JWT

Organizer creates and publishes an event

Users register for the event

Organizer confirms or rejects reservations

Users download QR tickets (PDF)

Organizer scans ticket and confirms check-in

Metrics update live through WebSocket

Production setup

DEBUG=False

Set proper ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS

Configure real SMTP for activation emails

Use HTTPS (required for QR scanning on mobile)

Redis and Postgres in dedicated containers

Deploy backend (e.g. Railway / Render / Fly.io)

Deploy frontend (Vercel) connected through NEXT_PUBLIC_API_BASE_URL

Enable Sentry DSN if desired



----------------------------------------------------------------------------------------------




EventFlow (Polska wersja)

Production-ready system do zarządzania wydarzeniami z autoryzacją JWT, rolami (User / Organizer / Admin), QR-biletami i metrykami w czasie rzeczywistym (Django REST + Next.js).
Projekt zaprojektowany z myślą o pokazaniu profesjonalnej architektury full-stack, z podziałem backend / frontend, Dockerem i praktykami DevOps.

Opis

Rejestracja i logowanie z linkiem aktywacyjnym przez e-mail (SMTP)

Autoryzacja JWT (login, logout, refresh token)

Role: User, Organizer, Admin

Tworzenie, publikacja i anulowanie wydarzeń

Rezerwacje z kolejką oczekujących i zatwierdzaniem przez organizatora

QR-bilety (PDF) i check-in w czasie rzeczywistym

Panel organizatora i administratora

Metryki na żywo przez WebSocket (Django Channels + Redis)

Pełna konfiguracja Docker Compose (backend, frontend, Redis, PostgreSQL)

Integracja z Sentry (opcjonalna)

Testy automatyczne (pytest)

Czysta architektura i SRP (Single Responsibility Principle)

Stos technologiczny

Backend: Django REST Framework + Django Channels

Frontend: Next.js (React 19 + TypeScript + Tailwind CSS)

Baza danych: PostgreSQL

Caching / Realtime: Redis

DevOps: Docker Compose (dev + prod), GitHub Actions CI/CD

E-mail: Gmail SMTP (aktywacja konta)

Główne funkcjonalności

Rejestracja z aktywacją konta przez e-mail

Logowanie i autoryzacja JWT

Tworzenie i publikacja wydarzeń przez organizatora

Rezerwacje i zatwierdzanie zgłoszeń

Generowanie QR-biletów w formacie PDF

Skanowanie QR i potwierdzanie obecności uczestników

Metryki wydarzenia aktualizowane w czasie rzeczywistym

Zarządzanie rolami użytkowników

Oddzielone warstwy logiki i widoku (czysty kod, SRP)

Uruchomienie (Docker Compose)

Sklonuj repozytorium

Skopiuj plik .env.dev do .env

Uruchom kontenery poleceniem:
docker compose up --build

Backend: http://localhost:8000

Frontend: http://localhost:3000

Swagger: http://localhost:8000/api/schema/swagger-ui/

Redis i PostgreSQL uruchamiane automatycznie przez Docker

Typowy przepływ użytkownika

Użytkownik rejestruje się i aktywuje konto przez e-mail

Loguje się tokenem JWT

Organizator tworzy i publikuje wydarzenie

Użytkownicy rezerwują miejsca

Organizator zatwierdza lub odrzuca zgłoszenia

Użytkownicy pobierają QR-bilety (PDF)

Organizator skanuje kod QR i potwierdza check-in

Metryki wydarzenia aktualizują się na żywo (WebSocket)

Konfiguracja produkcyjna

DEBUG=False

Ustaw ALLOWED_HOSTS i CSRF_TRUSTED_ORIGINS

Skonfiguruj prawdziwe SMTP dla e-maili aktywacyjnych

Używaj HTTPS (konieczne dla QR na telefonach)

Redis i PostgreSQL w osobnych kontenerach

Backend: Railway / Render / Fly.io

Frontend: Vercel

Połączone przez NEXT_PUBLIC_API_BASE_URL

Sentry DSN opcjonalnie do monitoringu