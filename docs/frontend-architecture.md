# Frontend Architecture (React Native)

## Stack

| Concern | Choice |
|---------|--------|
| Framework | React Native via **Expo** (TypeScript template) |
| Navigation | **React Navigation 6** — native stack + bottom tabs |
| Server state | **TanStack Query v5** |
| Client state | **Redux Toolkit** — auth session + UI only |
| Styling | **NativeWind** (Tailwind CSS) |
| Forms | React Hook Form + zod (light validation) |
| HTTP | Axios + interceptors |
| Secure storage | `expo-secure-store` for refresh (and optionally access) token |
| Dates | `date-fns` for formatting; send `session_date` as ISO date string |

## Redux vs React Query

### Redux Toolkit owns

| State | Reason |
|-------|--------|
| `auth.status` (`idle` \| `loading` \| `authenticated` \| `unauthenticated`) | App-wide gate for navigation |
| `auth.user` | Cached from `/api/auth/me/` after login |
| `auth.tokens` | Access in memory; refresh in SecureStore |
| UI preferences | e.g. last selected class id, theme (optional) |
| Transient UI | e.g. attendance draft before save (optional; can be local component state) |

### React Query owns

| Data | Query keys (examples) |
|------|------------------------|
| Classes | `['classes']`, `['classes', id]` |
| Students | `['students', { search, classId }]`, `['students', id]` |
| Enrollments | `['classes', classId, 'enrollments']` |
| Attendance | `['attendance', { classId, date }]`, mutations invalidate |
| Payments | `['payments', filters]`, `['payments', 'summary', studentId]` |
| Notes | `['notes', { studentId }]` |
| Recommendations | `['recommendations', { studentId, completed }]` |
| Dashboard | `['dashboard']` |

**Rule:** Do not copy lists of classes/students into Redux. After login, React Query fetches fresh data; on logout, `queryClient.clear()`.

### Auth + Query integration

1. Login mutation → store tokens → `dispatch(setAuthenticated)` → prefetch `me` + `dashboard`.
2. Axios request interceptor reads access token from Redux (or memory ref).
3. Response interceptor: 401 → refresh → retry once → else logout + clear queries.
4. App launch: read refresh from SecureStore → refresh access → `me` → set authenticated or login.

## Project Structure (`mobile/src/`)

```text
api/
  client.ts           # axios instance, interceptors
  auth.ts
  classes.ts
  students.ts
  attendance.ts
  ...
components/
  ui/                 # Button, Card, Input, EmptyState, ErrorState, Loading
  forms/
navigation/
  RootNavigator.tsx
  AuthNavigator.tsx
  MainNavigator.tsx
  types.ts
screens/
  auth/
    LoginScreen.tsx
    RegisterScreen.tsx
  dashboard/
    DashboardScreen.tsx
  classes/
    ClassListScreen.tsx
    ClassDetailScreen.tsx
    CreateClassScreen.tsx
    EditClassScreen.tsx
  attendance/
    TakeAttendanceScreen.tsx
    AttendanceHistoryScreen.tsx
  students/
    StudentListScreen.tsx
    StudentDetailScreen.tsx
    CreateStudentScreen.tsx
    EditStudentScreen.tsx
  payments/
    PaymentListScreen.tsx
    RecordPaymentScreen.tsx
  notes/
    NotesScreen.tsx
  recommendations/
    RecommendationsScreen.tsx
store/
  index.ts
  authSlice.ts
hooks/
  useAuth.ts
  useRefreshOnFocus.ts
utils/
  dates.ts
  currency.ts
```

## Navigation Structure

```text
RootNavigator
├── AuthStack (unauthenticated)
│   ├── Login
│   └── Register
└── MainTabs (authenticated)
    ├── DashboardTab → DashboardStack
    │   └── Dashboard
    ├── ClassesTab → ClassesStack
    │   ├── ClassList
    │   ├── ClassDetail
    │   ├── CreateClass / EditClass
    │   ├── TakeAttendance
    │   └── AttendanceHistory
    ├── StudentsTab → StudentsStack
    │   ├── StudentList (search)
    │   ├── StudentDetail (profile, tabs: overview, attendance, payments, notes, recs)
    │   └── CreateStudent / EditStudent
    └── MoreTab (optional) → Payments, Settings, Logout
```

**Fast path:** ClassDetail prominent **Take Attendance** button → `TakeAttendanceScreen` with class id + today’s date.

Student flows from ClassDetail: tap student → `StudentDetail` with `classId` context for payments/attendance filters.

Type-safe params via `@react-navigation/native` + `RootStackParamList`.

## Screen UX Patterns

| Pattern | Usage |
|---------|--------|
| Pull-to-refresh | Lists and dashboard |
| Optimistic updates | Recommendation `completed` toggle (with rollback) |
| Confirmation modal | Delete class/student/note |
| Toast / snackbar | Success after mutations |
| Skeleton loaders | Dashboard and lists |
| Empty states | No classes, no students, no attendance for date |

## Take Attendance UX

1. Load enrollments for class via React Query.
2. Load existing attendance for `session_date` (default today).
3. Local state: map `studentId → status` (default `present` if “Mark all present”).
4. Single **Save** → `POST /api/attendance/bulk/`.
5. Large tap targets: Present / Absent / Late segmented control per row.

Minimize taps: optional **Mark all present** at top, then change exceptions.

## Student Profile

Tabs or sections:

- Info + stats header (attendance %, total paid, pending recs)
- Attendance history (filter by class)
- Payments + totals
- Notes (chronological)
- Recommendations (pending first)

## Forms and Validation

- Client: required fields, email format, amount > 0, max lengths.
- Server errors mapped to form fields from DRF `errors` object.

## Testing (Mobile)

| Area | Tool |
|------|------|
| Unit | Jest — auth slice, api client refresh logic, utils |
| Component | React Native Testing Library — Login, TakeAttendance row |
| E2E (optional later) | Detox or Maestro |

Priority: auth persistence helper, bulk attendance submit payload, login error states.

## Environment

```text
EXPO_PUBLIC_API_URL=http://127.0.0.1:8000/api
```

Android emulator: `10.0.2.2` instead of localhost — document in README.

## Accessibility

- Minimum touch target 44pt
- `accessibilityLabel` on attendance status buttons
- Sufficient color contrast for status chips (present=green, absent=red, late=amber)

## Performance

- FlatList for student/attendance lists
- `staleTime` 30–60s for class/student lists; shorter for attendance on active screen
- Invalidate narrowly on mutations (e.g. only `['attendance', { classId, date }]`)
