# API Design

Base URL: `/api/`  
Authentication: `Authorization: Bearer <access_token>` unless noted.

OpenAPI: `/api/schema/` (drf-spectacular), UI at `/api/docs/`.

## Pagination

List endpoints use **page number pagination**:

```json
{
  "count": 100,
  "next": "http://.../api/students/?page=2",
  "previous": null,
  "results": []
}
```

Default page size: 20 (configurable via `?page_size=` capped at 100).

## Filtering

Query parameters on list endpoints (django-filter):

| Resource | Filters |
|----------|---------|
| classes | `search` (title) |
| students | `search` (name, phone, email), `class_id` (enrolled active) |
| attendance | `student_id`, `class_id`, `date` / `session_date`, `status` |
| payments | `student_id`, `class_id`, `payment_date`, `payment_date_after`, `payment_date_before` |
| notes | `student_id` |
| recommendations | `student_id`, `completed` |

## Auth

| Method | Path | Auth | Body | Response |
|--------|------|------|------|----------|
| POST | `/api/auth/register/` | No | email, password, first_name?, last_name? | user summary + tokens **or** 201 + login separately |
| POST | `/api/auth/login/` | No | email, password | `{ access, refresh }` |
| POST | `/api/auth/token/refresh/` | No | refresh | `{ access }` |
| POST | `/api/auth/logout/` | Yes | refresh | 204 — blacklists refresh |
| GET | `/api/auth/me/` | Yes | — | `{ id, email, first_name, last_name }` |

**Register response (proposed):** return tokens like login to avoid extra round-trip:

```json
{
  "user": { "id": 1, "email": "a@b.com", "first_name": "", "last_name": "" },
  "access": "...",
  "refresh": "..."
}
```

Never return password hash or `is_superuser` to clients.

### Errors

| Status | When |
|--------|------|
| 400 | Validation |
| 401 | Missing/invalid token |
| 403 | Object not owned by user |
| 404 | Not found (or 404 for cross-tenant hide) |
| 409 | Duplicate attendance (unique constraint) |

---

## Classes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/classes/` | List teacher's classes |
| POST | `/api/classes/` | Create |
| GET | `/api/classes/{id}/` | Detail + optional stats query `?include=stats` |
| PATCH | `/api/classes/{id}/` | Update |
| DELETE | `/api/classes/{id}/` | Delete |

**Create body:**

```json
{ "title": "Piano Monday", "description": "" }
```

**List item (example):**

```json
{
  "id": 1,
  "title": "Piano Monday",
  "description": "",
  "student_count": 12,
  "created_at": "...",
  "updated_at": "..."
}
```

`student_count` and `latest_session_date` can be annotations on list serializer.

---

## Students

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/students/` | List owned students |
| POST | `/api/students/` | Create student |
| GET | `/api/students/{id}/` | Profile + summary stats |
| PATCH | `/api/students/{id}/` | Update |
| DELETE | `/api/students/{id}/` | Delete |

**Create with optional class enrollment:**

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1...",
  "email": "",
  "date_of_birth": null,
  "class_ids": [1]
}
```

**Profile summary (`GET /api/students/{id}/`):**

```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "...": "...",
  "stats": {
    "attendance_rate": 0.92,
    "total_paid": "150.00",
    "last_attendance_date": "2026-09-23",
    "pending_recommendations": 2
  },
  "enrollments": [{ "class_id": 1, "class_title": "Piano", "is_active": true }]
}
```

---

## Enrollments

Nested under class or student for clarity:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/classes/{class_id}/enrollments/` | Active students in class |
| POST | `/api/classes/{class_id}/enrollments/` | Add student `{ "student_id": 5 }` |
| DELETE | `/api/classes/{class_id}/enrollments/{student_id}/` | Remove (deactivate) |

Alternative: `POST /api/enrollments/` with `class_id` + `student_id` — implementation may pick one style; **nested under class** matches “add student to class” UX.

---

## Attendance

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/attendance/` | Filtered list |
| POST | `/api/attendance/` | Single record |
| POST | `/api/attendance/bulk/` | **Bulk upsert for one class + date** |
| GET | `/api/attendance/{id}/` | Detail |
| PATCH | `/api/attendance/{id}/` | Update status/note |
| DELETE | `/api/attendance/{id}/` | Delete |

**Single create:**

```json
{
  "student": 1,
  "class": 1,
  "session_date": "2026-09-25",
  "status": "present",
  "note": ""
}
```

**Bulk (Take Attendance screen):**

```json
{
  "class_id": 1,
  "session_date": "2026-09-25",
  "records": [
    { "student_id": 1, "status": "present" },
    { "student_id": 2, "status": "absent" }
  ],
  "mark_all_present_first": false
}
```

Server: upsert by `(student, class, session_date)`; set `recorded_at` on each write.

Optional shortcut:

```json
{
  "class_id": 1,
  "session_date": "2026-09-25",
  "mark_all_present": true
}
```

Creates/updates all **actively enrolled** students to `present`.

---

## Payments

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/payments/` | List + filters |
| POST | `/api/payments/` | Create |
| GET | `/api/payments/{id}/` | Detail |
| PATCH | `/api/payments/{id}/` | Update |
| DELETE | `/api/payments/{id}/` | Delete |

**Create:**

```json
{
  "student": 1,
  "class": 1,
  "amount": "50.00",
  "payment_date": "2026-09-25",
  "description": "September tuition"
}
```

**Aggregates endpoint (optional):**

`GET /api/payments/summary/?student_id=&class_id=` → total, month_total, last_payment.

Can be folded into student/class detail instead to reduce surface area.

---

## Notes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/notes/` | `?student_id=` |
| POST | `/api/notes/` | Create |
| GET | `/api/notes/{id}/` | Detail |
| PATCH | `/api/notes/{id}/` | Update |
| DELETE | `/api/notes/{id}/` | Delete |

```json
{ "student": 1, "content": "Parent requested evening sessions." }
```

---

## Recommendations

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/recommendations/` | `?student_id=&completed=false` |
| POST | `/api/recommendations/` | Create |
| PATCH | `/api/recommendations/{id}/` | Update content or `completed` |
| DELETE | `/api/recommendations/{id}/` | Delete |

```json
{ "student": 1, "content": "Practice 30 minutes daily", "completed": false }
```

---

## Dashboard

`GET /api/dashboard/` — single aggregated payload for home screen:

```json
{
  "today_classes": [...],
  "today_attendance_summary": { "present": 5, "absent": 1, "late": 0 },
  "recent_payments": [...],
  "pending_recommendations_count": 3,
  "students_count": 25
}
```

Keeps mobile to one round-trip; implemented via selective queries or a thin service.

---

## Permissions Matrix

All resources: **authenticated + queryset scoped to `request.user`**.

Object-level: retrieve/update/delete only if related `owner` or enrollment chain matches.

Bulk attendance: reject if any `student_id` not enrolled in `class_id` or wrong owner.

---

## Versioning

No `/v1/` prefix for MVP; add when breaking changes occur.

---

## CORS

Development: allow Expo dev server origins.  
Production: explicit `CORS_ALLOWED_ORIGINS` from environment.
