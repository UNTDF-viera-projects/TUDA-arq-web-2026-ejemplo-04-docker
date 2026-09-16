# Ejemplo 06 - Docker compose desarrollo back y front

## Setup

1. clonar repo
2. Copiar el `.env.example` a `.env` y cambiarle los valores. Ejemplo `cp .env.example .env`
2. `docker compose up`
3. `docker compose run --rm api python manage.py migrate`
4. `docker compose run --rm app pnpm install`