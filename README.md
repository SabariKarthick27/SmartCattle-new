# SmartCattle — QR-Based Cattle Management & Precision Health Monitoring System

> **StartupFair Hackathon: Solo Participant 50 (Final Year Mini Project — IT / AIDS Dept)**  
> **Repository:** [sona-final-year-mini-it-aids-d-theofflsabari-371](https://github.com/StartupFair/sona-final-year-mini-it-aids-d-theofflsabari-371)

SmartCattle is an intelligent precision livestock operations platform designed to bridge smallholder dairy farmers and veterinary professionals across Tamil Nadu. Using non-invasive digital ear tags with secure QR technology, the system enables instant livestock identification, streamlined daily health data logging, multivariate disease risk prediction (CHDI), and automated veterinary triage.

---

## 🌟 Key Highlights

- **Instant QR Livestock Identification:** Scan ear tags using any standard mobile camera or the in-app scanner to retrieve digital cattle profiles in under 1 second.
- **Integrated Daily Health Logging Workflow:** Directly log Body Weight (kg), Feed Intake (kg), Milk Yield (L), and Body Temperature (°C) immediately upon scanning the QR tag.
- **Three-Stage CHDI Analytical Engine:**
  - **Stage 1 — Rolling Baseline:** 14-day moving average and sample variance with Bessel's correction to compute personalized vital departures ($z$-scores).
  - **Stage 2 — Regularized Mahalanobis Distance:** Tikhonov-regularized multivariate covariance matrix ($\Sigma_{reg} = \Sigma + \lambda I$) producing a composite 0–100 health score with analytical confidence gating.
  - **Stage 3 — LOCO Feature Attribution:** Leave-One-Covariate-Out permutation to identify primary physiological anomaly drivers with plain-language explanations.
- **Automated Clinical Triage & Alerts:** Animals flagged in the *Watch* (50–74) or *At-Risk* (<50) triage bands automatically spawn prioritized cases for veterinary doctors.
- **Role-Based Access Control:** Dedicated, responsive portals for **Farmers**, **Veterinarians**, and **Livestock Administrators**.

---

## 🏗️ Architecture & Tech Stack

- **Frontend & Fullstack Framework:** Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS v4
- **Database & ORM:** PostgreSQL (Neon Serverless) with Prisma ORM
- **Authentication:** NextAuth.js (SessionGuard, Role-based protection)
- **Machine Learning Microservice:** Python 3.13, FastAPI, NumPy, SciPy (Spatial Distance), Scikit-learn
- **Data Visualization & Telemetry:** Recharts, HTML5-QRCode, NodeMailer, QRCode

---

## 🚀 Getting Started

### 1. Prerequisites
- Node.js 20+ (Node.js 24 recommended)
- Python 3.10+
- PostgreSQL database (or Neon connection string)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/StartupFair/sona-final-year-mini-it-aids-d-theofflsabari-371.git
cd sona-final-year-mini-it-aids-d-theofflsabari-371

# Install Node dependencies
npm install

# Set up Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install fastapi uvicorn numpy scipy scikit-learn pydantic
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
DATABASE_URL="postgresql://user:password@host/dbname?sslmode=require"
DIRECT_URL="postgresql://user:password@host/dbname?sslmode=require"
NEXTAUTH_SECRET="your-secure-random-secret"
NEXTAUTH_URL="http://localhost:3000"
```

### 4. Database Setup
```bash
# Push Prisma schema to your database
npm run db:push

# (Optional) Seed default users, settings, and cattle profiles
npm run db:seed
```

### 5. Running the Application
```bash
# Run both Next.js frontend and Python ML service concurrently:
npm run dev

# Or run services individually:
npm run dev:next      # Starts Next.js on http://localhost:3000
npm run dev:python    # Starts FastAPI ML Microservice on http://localhost:8000
```

### 6. Mathematical Verification
Verify mathematical parity of the IEEE paper formulas (Equations 1 to 9):
```bash
npm run verify:math
```

---

## 📱 User Roles & Default Portals

1. **Farmer Portal (`/farmer`):** Cattle herd management, instant QR scanning, daily health check-in, vaccination schedules, and vet assistance requests.
2. **Veterinary Portal (`/vet`):** Clinical triage queue, case diagnosis, automated alert reviews, and district-level weekly epidemiological analysis.
3. **Administrator Dashboard (`/admin`):** User approvals, CHDI mathematical threshold calibration, ML retraining metrics, and immutable system audit logs.

---

## 📄 License & Attribution
Developed for the **StartupFair Hackathon 2026** by Solo Participant 50 (Final Year Mini Project — IT / AIDS Department).
