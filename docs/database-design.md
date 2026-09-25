# Database Design

## Entity Relationship (Logical)

```text
User (teacher)
  │
  ├──< Class
  │
  └──< Student
         │
         └──< Enrollment >── Class
                │
                ├── (implicit) Attendance, Payment scoped by student + class
                │
Student ──< StudentNote
Student ──< Recommendation

Attendance: Student + Class + session_date (unique)
Payment:    Student + Class
```

**Decision: Enrollment instead of `Student.class_id`**

| Requirement | How Enrollment helps |
|-------------|----------------------|
| Student in multiple classes | Many enrollments per student |
| Leave a class | Set `left_at` or `is_active=False` |
| Historical membership | Keep enrollment row; filter active for attendance UI |
| Attendance per class | FK to `Class` + `Student`; validate active enrollment |
| Payment per class | Same validation |

Students are **owned by the teacher** (`Student.owner`), not global across users. Two teachers never share the same `Student` row (acceptable for MVP; future “organization” tenancy could lift this).

---

## Tables

### `accounts_user`

Custom user extending `AbstractUser` or `AbstractBaseUser` + `PermissionsMixin`.

| Column | Type | Notes |
|--------|------|--------|
| id | BigAuto PK | |
| email | EmailField, unique | LOGIN_FIELD |
| password | hashed | |
| first_name, last_name | CharField | optional display |
| is_active | bool | |
| is_staff | bool | admin only |
| date_joined | datetime | |

Indexes: unique on `email`.

---

### `classes_class`

| Column | Type | Notes |
|--------|------|--------|
| id | BigAuto PK | |
| owner_id | FK → User | CASCADE |
| title | CharField(200) | |
| description | TextField, blank | |
| created_at | DateTime | auto |
| updated_at | DateTime | auto |

Index: `(owner_id, title)` for list queries.

---

### `students_student`

| Column | Type | Notes |
|--------|------|--------|
| id | BigAuto PK | |
| owner_id | FK → User | CASCADE |
| first_name | CharField(100) | |
| last_name | CharField(100) | |
| phone | CharField(32), blank | indexed for search |
| email | EmailField, blank | |
| date_of_birth | DateField, null | |
| notes | TextField, blank | **legacy/summary field optional** — prefer `StudentNote` for chronology |
| created_at, updated_at | DateTime | |

Index: `(owner_id, last_name, first_name)`, GIN/trigram optional later for search.

---

### `students_enrollment`

| Column | Type | Notes |
|--------|------|--------|
| id | BigAuto PK | |
| student_id | FK → Student | CASCADE |
| class_id | FK → Class | CASCADE |
| enrolled_at | DateTime | auto on create |
| left_at | DateTime, null | null = active |
| is_active | bool | default True; `left_at` set → False |

**Constraints:**

- `UniqueConstraint(student, class)` — one enrollment row per pair (re-enroll updates same row or new row per policy; MVP: one row, reactivate by clearing `left_at`).

**Validation:** `student.owner_id == class.owner_id`.

---

### `attendance_attendance`

| Column | Type | Notes |
|--------|------|--------|
| id | BigAuto PK | |
| student_id | FK → Student | |
| class_id | FK → Class | |
| session_date | Date | “which class day” |
| recorded_at | DateTime | timezone-aware, auto on create/update |
| status | CharField | choices: `present`, `absent`, `late` |
| note | TextField, blank | |
| created_at | DateTime | |

**Constraints:**

- `UniqueConstraint(student, class, session_date)` — prevents duplicate marks for same day.

**Indexes:** `(class_id, session_date)`, `(student_id, session_date)`, `(student_id, class_id)`.

**Timezone note:** `session_date` is authoritative for “attendance on this day” reporting. `recorded_at` captures when the teacher saved the record (UTC in DB).

---

### `payments_payment`

| Column | Type | Notes |
|--------|------|--------|
| id | BigAuto PK | |
| student_id | FK → Student | |
| class_id | FK → Class | |
| amount | Decimal(12, 2) | never Float |
| payment_date | Date | |
| description | CharField/TextField, blank | |
| created_at | DateTime | |

Indexes: `(student_id)`, `(class_id)`, `(payment_date)`.

---

### `notes_studentnote`

| Column | Type | Notes |
|--------|------|--------|
| id | BigAuto PK | |
| student_id | FK → Student | CASCADE |
| content | TextField | |
| created_at, updated_at | DateTime | |

Chronological list: `order_by('-created_at')`.

---

### `recommendations_recommendation`

| Column | Type | Notes |
|--------|------|--------|
| id | BigAuto PK | |
| student_id | FK → Student | CASCADE |
| content | TextField | |
| completed | bool | default False |
| created_at, updated_at | DateTime | |

Index: `(student_id, completed)`.

---

## ER Diagram (Mermaid)

```mermaid
erDiagram
    User ||--o{ Class : owns
    User ||--o{ Student : owns
    Student ||--o{ Enrollment : has
    Class ||--o{ Enrollment : has
    Student ||--o{ Attendance : has
    Class ||--o{ Attendance : for
    Student ||--o{ Payment : has
    Class ||--o{ Payment : for
    Student ||--o{ StudentNote : has
    Student ||--o{ Recommendation : has
```

---

## Attendance Status Extensibility

MVP: Django `TextChoices` on model + serializer validation.

Future: separate `AttendanceStatus` lookup table or JSON schema — not needed for three statuses.

---

## Cascades and Deletes

| Action | Behavior |
|--------|----------|
| Delete Class | CASCADE enrollments; CASCADE attendance/payments for that class (or RESTRICT with message — **MVP: CASCADE** with UI confirmation) |
| Delete Student | CASCADE notes, recommendations, enrollments, attendance, payments |
| Remove from class | PATCH enrollment `is_active=False`, `left_at=now` |

---

## Statistics (Computed, Not Stored)

**Per student** (query or annotated endpoint):

- Total sessions with attendance rows vs present/late/absent counts
- Attendance % = `(present + late) / total` or `present / total` — **document: count `present` + `late` as “attended” for percentage**
- Total paid: `Sum(payment.amount)`
- Pending recommendations: `count(completed=False)`

**Per class:**

- Active students: count active enrollments
- Average attendance: aggregate across students in class for date range
- Total payments: `Sum` for class_id

---

## Migrations Strategy

- Initial migration per app in dependency order: accounts → classes → students → attendance → payments → notes → recommendations.
- Data migrations only when needed; none for greenfield.

---

## PostgreSQL

- Use PostgreSQL 15+ in Docker.
- `USE_TZ=True`, `TIME_ZONE='UTC'` in Django; display in mobile with `date-fns` / `Intl` in local timezone.
