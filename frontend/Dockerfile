# frontend/Dockerfile  (DEV)
# Debian (glibc) → stabilniej dla natywnych bindów niż Alpine (musl)
FROM node:20-bookworm-slim

WORKDIR /app

# lekkie build deps (gdyby coś chciało się kompilować)
RUN apt-get update && apt-get install -y \
    python3 make g++ \
 && rm -rf /var/lib/apt/lists/*

# Flagi wyłączające natywne bindy Next/Tailwind (oxide/lightningcss)
ENV NEXT_TELEMETRY_DISABLED=1 \
    NEXT_DISABLE_LIGHTNINGCSS=1 \
    TAILWIND_DISABLE_OXIDE=1

# dla cache warstw — realny install zrobimy po starcie kontenera do volumenu
COPY package.json package-lock.json* ./

EXPOSE 3000

# dev serwer — właściwy install robimy w 'command' z docker-compose
CMD ["npm", "run", "dev", "--", "-p", "3000", "-H", "0.0.0.0"]
