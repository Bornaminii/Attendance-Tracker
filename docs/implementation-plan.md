# Implementation Plan

Work **one phase at a time**. After each phase: run tests, fix regressions, update `docs/progress.md`.

---

## Phase 1: Project setup

**Goal:** Runnable backend (Docker + Postgres), empty mobile app shell, env templates, CI-friendly test command.

**Files:** `backend/`, `docker-compose.yml`, `.env.example`, `mobile/` (Expo init), `README.md`, `docs/progress.md`.

**Tasks:**

- Django project `config` with settings split (base/dev/prod).
- Install DRF, simplejwt, cors, django-filter, drf-spectacular, psycopg.
- Docker Compose: postgres + web.
- Expo TypeScript app with NativeWind, React Navigation, Redux Toolkit, TanStack Query.
- Pre-commit or makefile targets: `make test`, `make migrate`.

**Tests:** Smoke test — Django `manage.py check`; mobile Jest runs empty suite.

**Acceptance:** `docker compose up` brings API health; `expo start` launches app.

---

## Phase 2: Database models

**Goal:** All models, migrations, admin registration (optional), queryset scoping helpers.

**Files:** `apps/accounts`, `classes`, `students` (+ Enrollment), `attendance`, `payments`, `notes`, `recommendations`.

**Tasks:**

- Custom User model (email login).
- Models per `docs/database-design.md`.
- Unique constraint on attendance.
- `DecimalField` for payments.

**Tests:** Model factory tests, constraint tests (duplicate attendance).

**Acceptance:** `migrate` succeeds; admin or shell can create graph of data.

---

## Phase 3: Authentication

**Goal:** Register, login, refresh, logout, me; JWT blacklist; mobile login + persistence + refresh.

**Files:** `accounts/views.py`, `accounts/serializers.py`, `urls`, mobile `authSlice`, `api/client.ts`, Login/Register screens, `RootNavigator` auth gate.

**Tests:** Backend auth test module (login, invalid, refresh, unauthorized, logout).

**Acceptance:** Register → login → `me` → reopen app still authenticated → logout blocks `me`.

---

## Phase 4: Class management

**Goal:** Class CRUD API + mobile list/create/edit/delete.

**Files:** `classes/` API, screens `ClassList`, `CreateClass`, `EditClass`.

**Tests:** Class CRUD + user isolation (user B cannot read user A’s class).

**Acceptance:** Teacher creates multiple classes and sees only their own.

---

## Phase 5: Student management & enrollment

**Goal:** Student CRUD, enroll/unenroll in class, class student list.

**Files:** `students/` API, enrollment nested routes, mobile student screens, class detail student list.

**Tests:** Student CRUD, enrollment, isolation, search filter.

**Acceptance:** Add student to class; remove from class without deleting global student (deactivate enrollment).

---

## Phase 6: Attendance

**Goal:** Single + bulk attendance API; Take Attendance screen; history list with filters.

**Files:** `attendance/` views including bulk, `TakeAttendanceScreen`, `AttendanceHistoryScreen`.

**Tests:** Create, update, duplicate prevention, filtering, bulk upsert, enrollment validation.

**Acceptance:** Mark all present, change individuals, save once; view history by date/class.

---

## Phase 7: Payments

**Goal:** Payment CRUD, filters, totals on student profile.

**Files:** `payments/` API, `RecordPaymentScreen`, payment list sections.

**Tests:** Decimal handling, create/update, filters, isolation.

**Acceptance:** Record payment; see total paid and month summary on profile.

---

## Phase 8: Notes

**Goal:** Note CRUD per student, chronological UI.

**Files:** `notes/` API, notes section on `StudentDetail`.

**Tests:** Note CRUD + isolation.

**Acceptance:** Create, edit, delete notes on student profile.

---

## Phase 9: Recommendations

**Goal:** Recommendation CRUD, complete toggle, pending counts.

**Files:** `recommendations/` API, UI on student + dashboard snippet.

**Tests:** CRUD, complete recommendation, filter `completed=false`.

**Acceptance:** Mark complete; pending count updates on dashboard/profile.

---

## Phase 10: Dashboard & statistics

**Goal:** `GET /api/dashboard/`; student/class stats on detail endpoints; dashboard screen.

**Files:** `dashboard` view or service, `DashboardScreen`, stat annotations on serializers.

**Tests:** Dashboard aggregation smoke; student stats math (attendance rate).

**Acceptance:** Dashboard shows today’s summary, recent payments, pending recs; student profile shows rate and totals.

---

## Phase 11: Frontend polish

**Goal:** Loading/empty/error states, toasts, delete confirmations, search UX, consistent UI components.

**Files:** `components/ui/*`, screen updates.

**Tests:** RTL snapshots for critical empty/error states (optional).

**Acceptance:** Meets UI/UX section of requirements; attendance flow feels fast.

---

## Phase 12: Testing & hardening

**Goal:** Full backend test suite; key mobile tests; OpenAPI complete; README runbooks.

**Files:** `backend/tests/` or per-app `tests.py`, mobile `__tests__/`, spectacular schema.

**Tests:** All modules from requirements §22.

**Acceptance:** `pytest` green; documented API; user isolation test suite passes.

---

## Phase 13: Production readiness

**Goal:** Production settings, gunicorn, static/security checklist, `.env.example` complete.

**Files:** `config/settings/production.py`, docker prod profile optional, security headers.

**Acceptance:** Deployable checklist in README; no secrets in repo.

---

## Dependency Graph

```text
Phase 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13
                      └──────────────────┴── parallel possible: 8 & 9 after 5
```

Phases 8–9 can run in parallel after Phase 5; Phase 6–7 should follow enrollment.

---

## Questions Requiring Your Decision

Please confirm or override before implementation starts:

1. **Expo vs bare React Native** — Plan assumes **Expo** for SecureStore and faster setup. Do you require bare RN (e.g. custom native modules)?

2. **Public registration** — Plan includes `POST /api/auth/register/` for acceptance criterion “create an account.” Should registration be **open**, **invite-only** (disabled in prod), or **admin-only** (Django admin creates users)?

3. **Attendance rate formula** — Should **late** count as attended for percentage? **Proposed: yes** (`present` + `late` in numerator). Alternative: only `present`.

4. **Delete class with history** — **Proposed:** hard delete class cascades attendance/payments for that class (with confirmation dialog). Alternative: soft-delete class and retain read-only history.

5. **`Student.notes` text field** — Model includes optional summary field on Student; chronological notes use `StudentNote`. **Proposed:** use `StudentNote` only in UI and leave `Student.notes` for optional quick blurb or omit from UI entirely.

6. **Login identifier** — **Proposed: email only** (no separate username). Acceptable?

If you approve defaults where you don’t answer, implementation will follow the **Proposed** options above.
