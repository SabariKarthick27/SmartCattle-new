# SmartCattle — Master Build Prompt (Final, for Antigravity)

You are an expert full-stack engineer. Build **SmartCattle**, a QR-based cattle health management system for smallholder dairy farmers in India, as a **final-year academic project targeting an IEEE conference paper**. Code quality, clear data models, and instrumented metrics matter as much as functionality, since results will be reported academically.

## Tech Stack (final — use exactly this, single language throughout)
- **Next.js 14** (App Router) — frontend + backend in one project
- **TypeScript** — across the entire codebase, including the ML layer (no Python, no separate microservice)
- **Tailwind CSS** — styling
- **Neon** — serverless Postgres database
- **Prisma** — ORM, used for all database schema and queries against Neon
- **NextAuth.js** — authentication and role-based session management (Neon has no built-in auth, so this is required)
- **`qrcode`** (npm) — QR code generation per animal
- **`html5-qrcode`** — camera-based QR scanning in-browser
- **TensorFlow.js** — Stage 1 baseline forecasting (LSTM), with a simple moving-average fallback
- **Custom TypeScript function** — Mahalanobis distance / z-score based anomaly detection for Stage 2 (CHDI score) — no Isolation Forest library exists in JS, so implement this directly; document it in code comments as "distance-based anomaly detection," not as Isolation Forest
- **`ml-random-forest`** (npm) — Stage 3 vet-feedback classifier
- **Custom permutation-importance function** — explainability layer (SHAP substitute); rank each signal's contribution to the deviation score
- **Recharts** — CHDI trend charts and admin analytics graphs
- **Vercel** — deployment target

## Core Concept & Novelty (maintain this framing in code comments and any generated docs)
Most existing cattle-health-monitoring research assumes IoT wearables/sensors on every animal. SmartCattle is deliberately **sensor-optional**: it works from QR-tag scans and manually logged data (weight, feed, activity, symptoms), making it viable for smallholder farmers who cannot afford sensor hardware. Every logged data point must carry a `source: "manual" | "qr_scan" | "sensor"` field so a later sparse-vs-rich data accuracy comparison is possible — this is the primary evaluation experiment for the paper, so keep signal sources modular, not hardcoded to one input type.

## Roles & Auth
Three roles: **Farmer**, **Veterinarian**, **Admin**. One login page, role-based routing via NextAuth session + middleware.
```prisma
model User {
  id           String   @id @default(cuid())
  name         String
  phone        String
  email        String   @unique
  passwordHash String
  role         Role     // farmer | vet | admin
  farmId       String?
  assignedRegion String?
  isVerified   Boolean  @default(false)
  createdAt    DateTime @default(now())
}
enum Role { farmer vet admin }
```
Admin must approve new farmer/vet signups (`isVerified` gate) before dashboard access. Middleware restricts `/farmer/*`, `/vet/*`, `/admin/*` by role; redirect to the correct dashboard post-login.

## CHDI Health Scoring Engine

### Input Signals (per animal, time-series, each tagged with source)
Weight, feed intake/interval, activity level, vital signs (if available), QR-scan frequency/timing/GPS.

### Prisma Schema (core models)
```prisma
model Cattle {
  id          String   @id @default(cuid())
  farmerId    String
  tagId       String   @unique
  qrToken     String   @unique
  breed       String
  dob         DateTime
  weightLogs  WeightLog[]
  feedLogs    FeedLog[]
  activityLogs ActivityLog[]
  scanLogs    ScanLog[]
  chdiHistory CHDIEntry[]
}
model WeightLog   { id String @id @default(cuid()) cattleId String value Float timestamp DateTime source String }
model FeedLog     { id String @id @default(cuid()) cattleId String quantity Float feedType String timestamp DateTime source String }
model ActivityLog { id String @id @default(cuid()) cattleId String value Float timestamp DateTime source String }
model ScanLog     { id String @id @default(cuid()) cattleId String timestamp DateTime gps String? }
model CHDIEntry   { id String @id @default(cuid()) cattleId String score Float status String confidence Float topFactors Json timestamp DateTime }
model VetCase     { id String @id @default(cuid()) cattleId String farmerId String vetId String? status String urgency String chdiSnapshot Json symptoms String? diagnosis String? treatment String? medication String? followUpDate DateTime? createdAt DateTime @default(now()) resolvedAt DateTime? }
model VetFeedback { id String @id @default(cuid()) cattleId String vetId String caseId String predictedStatus String confirmedOutcome String timestamp DateTime @default(now()) }
model RegionAlert { id String @id @default(cuid()) region String triggeredAt DateTime affectedFarmIds Json severity String status String }
model AuditLog    { id String @id @default(cuid()) actorId String actorRole String action String targetId String? timestamp DateTime @default(now()) metadata Json? }
```

### Stage 1 — Baseline Forecasting (`/lib/chdi/baseline.ts`)
Per-animal (fallback: per-breed-cluster if <2–3 weeks of history) prediction of expected weight/feed/activity trajectory. Implement `computeBaseline(cattleId): { expected, variance }` — start with a moving-average implementation, structure it so a TensorFlow.js LSTM can be swapped in behind the same function signature.

### Stage 2 — Anomaly Detection / CHDI Score (`/lib/chdi/anomaly.ts`)
`computeCHDI(deviationVector): { score, confidence, status }` using Mahalanobis distance against the animal's own historical distribution. Normalize output to 0–100. Do not hardcode fixed per-signal weights — let the distance calculation account for signal covariance instead.

### Stage 3 — Vet-Feedback Classifier (`/lib/chdi/feedback-classifier.ts`)
Once `VetFeedback` accumulates enough labeled rows, train an `ml-random-forest` model on `(feature vector → confirmedOutcome)`. Build this as a callable retraining job (`retrainClassifier()`), stubbed initially, wired to real training once data exists. Track and expose precision/recall/F1.

### Explainability (`/lib/chdi/explain.ts`)
`explainScore(deviationVector): topFactors[]` via permutation importance — rank which signal contributed most to the deviation. Two display levels: plain-language single top factor (farmer view), full ranked breakdown (vet view).

### Confidence / Abstention
If an animal has <2–3 weeks of history, or the anomaly score's confidence interval is too wide, set `status: "abstain"` instead of forcing healthy/unhealthy. Track abstention rate and accuracy-when-not-abstaining as system-wide metrics exposed on the admin dashboard.

### Status Bands
`healthy (green) | watch (yellow) | at-risk (red) | abstain (grey)` — thresholds stored in an admin-configurable settings table, not hardcoded constants.

### Pipeline
New data logged → `computeBaseline()` → deviation calculated → `computeCHDI()` → if confidence low, status = abstain (no alert) → if watch/at-risk, auto-create `VetCase` with CHDI snapshot + `explainScore()` output attached → vet confirms/overrides → logged to `VetFeedback` → periodic `retrainClassifier()` job (cron or manual trigger) → admin dashboard surfaces performance metrics.

## Farmer Dashboard (`/app/farmer`)
- **Overview:** herd summary cards (total/healthy/at-risk/abstain/upcoming visits), CHDI sparklines (Recharts), alert banner.
- **My Cattle:** list/grid — photo, tag ID, QR thumbnail, breed, age, CHDI badge; filter/search; "Scan QR" → camera scanner → cattle profile.
- **Cattle Profile:** CHDI history chart (30/90/365-day toggle), plain-language top-factor panel, vaccination/deworming schedule with due/overdue flags, feed log entry form, "Request Vet Visit" (attaches current CHDI snapshot), manual symptom notes (text + optional photo).
- **QR Management:** generate/reprint QR (encodes animal ID + signed token, not raw data).
- **Notifications:** CHDI status change, vaccination due, vet visit confirmed, regional outbreak alert.
- **Records:** downloadable PDF health record per animal.
- API routes: `GET /api/farmer/cattle`, `GET /api/cattle/[id]`, `POST /api/cattle/[id]/feed-log`, `POST /api/cattle/[id]/vet-request`, `POST /api/cattle/[id]/scan`.

## Veterinarian Dashboard (`/app/vet`)
- **Case Queue (landing page):** auto-populated from at-risk/watch flags + manual requests, sorted by urgency; columns for farmer, location, tag ID, CHDI + trend, request time, distance; filters by region/status/urgency.
- **Patient Detail:** full CHDI history + diagnosis timeline overlay, full permutation-importance breakdown, diagnosis form (symptoms, diagnosis, treatment, medication+dosage, follow-up date), "Confirm/Override CHDI flag" writing to `VetFeedback`.
- **My Assigned Farms:** list/map, herd-level average CHDI per farm.
- **Visit Log:** past visits, outcomes, follow-up compliance.
- **Offline Mode:** cache assigned cases in IndexedDB/localStorage; queue diagnosis entries and sync on reconnect.
- API routes: `GET /api/vet/queue`, `GET /api/vet/cases/[id]`, `POST /api/vet/cases/[id]/diagnose`, `POST /api/vet/cases/[id]/feedback`, `GET /api/vet/farms`.

## Admin Dashboard (`/app/admin`)
- **User Management:** approve/reject farmer & vet signups, deactivate/reassign accounts and vet regions.
- **Herd Analytics:** regional CHDI heatmap, charts (total cattle, active vets, cases resolved/month, avg response time), outbreak early-warning panel.
- **Model Management:** view Stage 1/2/3 performance (abstention rate, confirm/override ratio, precision/recall once Stage 3 is live), adjust global status thresholds, trigger manual retraining, view model version history.
- **Audit Log:** all scans/logins/diagnoses/admin actions, timestamped, searchable, exportable.
- **Data Export:** CSV/PDF export of herd data, case history, CHDI logs, model performance reports.
- API routes: `GET/POST /api/admin/users`, `GET /api/admin/analytics`, `GET /api/admin/model-stats`, `PATCH /api/admin/chdi-config`, `POST /api/admin/retrain`, `GET /api/admin/audit-log`, `GET /api/admin/export`.

## Cross-Role: Regional Outbreak Alerts
If ≥N animals across ≥M farms in one region show a CHDI drop within a short time window, auto-generate a `RegionAlert` via an aggregation query over recent `CHDIEntry` rows — no separate model needed. Visible to Admin (full detail + map), Vets in region (priority case queue entry), Farmers in region (notification banner).

## Build Order
1. `npx create-next-app@latest` (TypeScript + Tailwind + App Router)
2. Set up Prisma + Neon connection string; define full schema above; run migration
3. NextAuth.js setup with role field + middleware for `/farmer`, `/vet`, `/admin` route protection
4. Basic CRUD: add cattle, log weight/feed/activity (tag every entry with `source`)
5. QR generation on cattle creation + scanner page resolving token → profile
6. `/lib/chdi/baseline.ts` — Stage 1 (moving average first)
7. `/lib/chdi/anomaly.ts` — Stage 2 CHDI score + confidence/abstention, with metrics logging
8. `/lib/chdi/explain.ts` — permutation importance, two display levels
9. Farmer dashboard: overview, cattle list, profile, QR, notifications, records
10. Auto-case creation on watch/at-risk → Vet dashboard: case queue, diagnosis form, feedback logging
11. Admin dashboard: user approval, analytics, model management, audit log, export
12. `/lib/chdi/feedback-classifier.ts` — Stage 3, wired once `VetFeedback` data exists
13. Regional outbreak aggregation logic + alert surfacing across all three dashboards
14. Sparse-vs-rich data comparison harness (accept simulated sensor-style input alongside manual/QR data; log Stage 2 accuracy under each condition) — build as a standalone runnable script/report generator, this is the key experiment for the paper
15. Deploy to Vercel, connect Neon, set environment variables

## Non-negotiables
- Never hardcode CHDI weights — the anomaly detection must account for signal covariance/distribution, not fixed manual weights.
- Never force a healthy/unhealthy label without sufficient per-animal history — abstain instead.
- Every logged data point must carry its `source` field.
- Keep Stage 1/2/3 functions swappable behind stable interfaces (e.g., `computeBaseline`, `computeCHDI`, `explainScore`) so implementations can be upgraded (moving-average → LSTM, Mahalanobis → other method) without touching calling code.
- Use Prisma for all database access — no raw SQL unless Prisma cannot express the query.
- All ML logic stays in TypeScript — no Python, no external microservice.
