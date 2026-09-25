# Attendance Tracker

Mobile app and API for a teacher to manage classes, students, attendance, payments, notes, and recommendations.

## Stack

- Backend: Django, Django REST Framework, PostgreSQL, Simple JWT
- Mobile: Expo (React Native, TypeScript), NativeWind, React Navigation, Redux Toolkit, TanStack Query
- Local infrastructure: Docker Compose

## Setup

```bash
cp .env.example .env
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements/dev.txt
cd mobile && npm install
```

## Run the API

```bash
docker compose up --build
```

Health check: [http://localhost:8000/api/health/](http://localhost:8000/api/health/)

OpenAPI UI: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

Postgres is published on host port **5433** (container port 5432) so it does not collide with another local Postgres. Apply migrations on the host when `DATABASE_URL` points at that port:

```bash
make migrate
```

## Run the mobile app

```bash
cd mobile
npx expo start
```

Point `EXPO_PUBLIC_API_URL` at the API. On a physical device, use the computer's LAN address instead of `localhost`.

## Tests

```bash
make test
```

Backend tests use SQLite and do not need Docker. `make check` runs Django's system check against development settings.
