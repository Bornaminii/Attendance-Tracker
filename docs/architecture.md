# Architecture Overview

## Purpose

Production-quality full-stack mobile application for teachers/tutors to manage classes, students, attendance, payments, notes, and recommendations. The backend is a Django REST API with PostgreSQL; the client is React Native (TypeScript) optimized for fast in-class attendance entry.

## High-Level System

```text
┌─────────────────────┐         HTTPS / JSON          ┌──────────────────────────┐
│  React Native App   │ ◄──────────────────────────► │  Django + DRF API        │
│  (Expo recommended) │   JWT (access + refresh)     │  PostgreSQL              │
│                     │                               │  Simple JWT + blacklist  │
│  Redux: auth, UI    │                               │  Per-user data isolation │
│  React Query: API   │                               │  OpenAPI (drf-spectacular)│
└─────────────────────┘                               └──────────────────────────┘
         │
         ▼
  Secure token storage (expo-secure-store)
```

## Architectural Principles

1. **Backend is the source of truth** — Authorization and business rules live in Django; the mobile app never enforces security alone.
2. **Thin API, focused domain** — REST resources map to teacher workflows; filtering and pagination on list endpoints.
3. **MVP-first, documented extension points** — Enrollment model and attendance-by-date support multi-class students and reporting without a `ClassSession` entity in v1.
4. **Separation of server state vs client state** — React Query owns fetched entities; Redux owns session and ephemeral UI state only.
5. **Testability** — Backend tests per domain app; mobile tests for auth flow, API client, and critical screens where practical.

## Repository Layout

```text
Attendance-Tracker/
├── backend/
│   ├── manage.py
│   ├── config/                 # settings (base, dev, prod), urls, wsgi
│   ├── apps/
│   │   ├── accounts/           # User, auth views
│   │   ├── classes/            # Class
│   │   ├── students/           # Student, Enrollment
│   │   ├── attendance/
│   │   ├── payments/
│   │   ├── notes/
│   │   └── recommendations/
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── dev.txt
│   │   └── prod.txt
│   └── pytest.ini / conftest
├── mobile/
│   ├── src/
│   │   ├── api/                # axios/fetch client, interceptors, endpoints
│   │   ├── components/
│   │   ├── features/           # optional feature modules
│   │   ├── navigation/
│   │   ├── screens/
│   │   ├── store/              # Redux Toolkit
│   │   ├── hooks/
│   │   └── utils/
│   ├── app.json / package.json
│   └── ...
├── docker/
│   └── django, postgres compose services
├── docker-compose.yml
├── .env.example
├── docs/
└── README.md
```

**Rationale:** Domain-split Django apps keep migrations and tests isolated. `students` owns `Student` and `Enrollment` because enrollment is the hinge between classes and students.

## Backend Architecture

### Layers

| Layer | Responsibility |
|-------|----------------|
| **Models** | Schema, constraints (unique attendance per day), `Decimal` for money |
| **Managers / queryset helpers** | `for_teacher(user)` scoping on all tenant data |
| **Serializers** | Validation, nested reads, write-only fields |
| **Views / ViewSets** | HTTP, permissions, filters |
| **Permissions** | `IsAuthenticated` + object-level checks via owner/enrollment chain |
| **Services (light)** | Bulk attendance (`mark_all_present`), stats aggregation — only where views would become heavy |

### Multi-Tenancy (User Isolation)

Every query for `Class`, `Student`, and dependent records filters through **ownership**:

- `Class.owner_id == request.user.id`
- `Student.owner_id == request.user.id`
- `Attendance`, `Payment`, `StudentNote`, `Recommendation` — accessible only if the related student (and class where applicable) belongs to the current user.

Enrollments are validated on create: both class and student must belong to the same teacher.

### Authentication Strategy

- **django-rest-framework-simplejwt** for access/refresh tokens.
- **Token blacklist** (`rest_framework_simplejwt.token_blacklist`) for logout (invalidate refresh token).
- Custom user model (`accounts.User`) with email as login identifier (username optional or same as email).
- **Registration:** `POST /api/auth/register/` for MVP (required by acceptance criteria “create an account”); can be disabled via settings in production if desired.

### Configuration

- `django-environ` or `dj-database-url` for `DATABASE_URL`, `SECRET_KEY`, JWT lifetimes, CORS.
- Settings split: `config/settings/base.py`, `development.py`, `production.py`.
- `DEBUG=False` in production; `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` from env.

### API Documentation

- **drf-spectacular** for OpenAPI 3 schema and Swagger UI at `/api/schema/` and `/api/docs/`.

### Error Format

Consistent JSON errors for validation and API exceptions:

```json
{
  "detail": "Human-readable message",
  "errors": {
    "field_name": ["message"]
  }
}
```

DRF’s default validation shape is acceptable; a small exception handler can normalize `detail` for non-field errors.

## Mobile Architecture

### Recommended Stack Details

- **Expo (SDK current stable)** with dev client — simplifies SecureStore, navigation, and team onboarding; React Native workflow remains standard (`npx expo start`).
- **NativeWind v4** for Tailwind-style styling.
- **Axios** (or fetch wrapper) with interceptors for auth headers and refresh-on-401.

### Networking

1. Access token attached to requests.
2. On 401, attempt refresh once; on failure, clear auth and navigate to Login.
3. Base URL from `EXPO_PUBLIC_API_URL`.

## Docker (Development)

- `docker-compose.yml`: `db` (PostgreSQL 16), `web` (Django runserver or gunicorn for prod profile).
- Mobile runs on host machine pointing at `http://localhost:8000` (or machine IP for physical devices).
- Volume mount for backend code; migrations on container start optional via entrypoint script.

## Key Tradeoffs

| Decision | Choice (MVP) | Alternative | Why |
|----------|--------------|-------------|-----|
| Student ↔ Class | **Enrollment** M2M | FK `class` on Student | Multi-class, leave/join history |
| Attendance grain | **One row per student/class/calendar date** | ClassSession + attendance | Faster MVP; unique constraint on `(student, class, session_date)` |
| Date/time | **`session_date` (Date)** + **`recorded_at` (DateTime TZ-aware)** | Single datetime only | Easy daily reports; audit when marked |
| User signup | **Public register endpoint** | Admin-only users | Matches acceptance criteria |
| Monorepo | **backend + mobile** in one repo | Separate repos | Simpler for solo/small team MVP |

## Future Scalability (Documented, Not MVP)

- **ClassSession** entity for recurring schedules and session-level attendance rollups.
- Payment status, method, refunds.
- Soft-delete on students/classes.
- Push notifications for recommendations.
- Offline-first attendance queue (sync when online).

## Security Summary

- Password hashing: Django default (PBKDF2).
- JWT short-lived access, longer refresh; refresh blacklisted on logout.
- No secrets in repo; `.env.example` only placeholders.
- CORS restricted to known origins in production.
- CSRF: not required for JWT API from mobile; session auth not used for API.
- Rate limiting: optional `django-ratelimit` or DRF throttling on auth endpoints in a later phase.

## Ambiguities Resolved (Without User Input)

1. **Student reuse across classes** — Yes, via Enrollment; student record is per-teacher, not per-class.
2. **Duplicate attendance** — Prevented by DB unique constraint on `(student, class, session_date)`.
3. **Timezone** — Store UTC in `recorded_at`; `session_date` is the teacher-selected “class day” (default: device/local date at save time, sent explicitly from client as `YYYY-MM-DD`).
4. **Account creation** — Register endpoint included; login uses email + password.
5. **Delete student** — Removing from class = deactivate/delete Enrollment; deleting Student cascades or blocks based on FK policy (recommend: soft-remove enrollment with `left_at`, hard delete student only from global student list with confirmation).

## Questions for Product Owner

See end of `docs/implementation-plan.md` and summary in README — only items that materially change schema or UX.
