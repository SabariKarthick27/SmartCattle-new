import Link from "next/link";
import { getServerSession } from "next-auth";
import { authOptions } from "./api/auth/[...nextauth]/route";
import { redirect } from "next/navigation";
import {
  IconScan,
  IconStethoscope,
  IconShieldAlert,
  IconActivity,
} from "@/components/icons";
import { SmartCattleLogo } from "@/components/SmartCattleLogo";
import HeroInteractiveWorkbench from "@/components/HeroInteractiveWorkbench";
import HeroTelemetryPill from "@/components/HeroTelemetryPill";

export default async function Home() {
  const session = await getServerSession(authOptions);

  const dashMap: Record<string, string> = {
    farmer: "/farmer",
    vet: "/vet",
    admin: "/admin",
  };
  const userDashUrl = session?.user?.role ? (dashMap[session.user.role] ?? "/login") : null;

  const capabilities = [
    {
      role: "For Dairy Farmers",
      title: "Fast QR Tag Scanning",
      desc: "Scan ear tags with your phone camera in seconds. Easily log daily milk, feed, weight, and track weekly baseline progress without paperwork.",
    },
    {
      role: "For Veterinarians",
      title: "Weekly Health Checkups & Analysis",
      desc: "Perform routine weekly checkups, review 7-day baseline trends, record vitals like temperature, and send health reports to farmers.",
    },
    {
      role: "For Health Officers",
      title: "Disease & Outbreak Alerts",
      desc: "Track animal health across districts, catch disease outbreaks early, and organize vaccination drives to protect herds.",
    },
  ];

  const workflowSteps = [
    {
      step: "01",
      icon: IconScan,
      title: "Scan Cow Ear Tag",
      desc: "Quickly scan the QR tag on the cow's ear using any mobile phone camera, even in low light.",
    },
    {
      step: "02",
      icon: IconActivity,
      title: "Weekly Baseline Calculation",
      desc: "The system calculates the cow's health baseline once a week, comparing 7-day milk, weight, and feed patterns.",
    },
    {
      step: "03",
      icon: IconStethoscope,
      title: "Weekly Vet Checkup",
      desc: "Your field veterinarian conducts weekly health checks, logs vitals like temperature, and shares diagnosis reports.",
    },
    {
      step: "04",
      icon: IconShieldAlert,
      title: "Stop Disease Spread",
      desc: "Regional disease alerts protect nearby farms before contagious infections can spread.",
    },
  ];

  return (
    <main className="min-h-screen bg-[#f6f8f7] text-slate-900 flex flex-col antialiased">
      {/* ── Precision Header ─────────────────────────────── */}
      <header className="sticky top-0 z-50 bg-slate-900 text-slate-300 border-b border-slate-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link href="/" className="group">
            <SmartCattleLogo variant="light" />
          </Link>

          <div className="flex items-center gap-3 sm:gap-4 text-xs font-mono">
            {session ? (
              <>
                <span className="text-slate-400 hidden sm:inline">
                  Signed in as <strong className="text-emerald-400 font-semibold">{session.user.name}</strong>
                </span>
                <Link
                  href={userDashUrl ?? "/login"}
                  id="nav-dashboard-btn"
                  className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-colors shadow-xs"
                >
                  Go to Dashboard →
                </Link>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  id="nav-login-btn"
                  className="text-slate-300 hover:text-white px-3 py-1.5 rounded-lg hover:bg-slate-800 transition-colors font-medium text-xs"
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  id="nav-register-btn"
                  className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-colors shadow-xs"
                >
                  Create Account →
                </Link>
              </>
            )}
          </div>
        </div>
      </header>

      {/* ── Split Specimen Hero ──────────────────────────── */}
      <section className="border-b border-slate-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
            {/* Left: Mission & Tactical Actions */}
            <div className="lg:col-span-6 space-y-6">
              <div className="inline-flex items-center gap-2 px-2.5 py-1 bg-emerald-50 border border-emerald-200 rounded text-emerald-800 text-xs font-mono font-bold">
                <span className="w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span>
                SIMPLE CATTLE HEALTH &amp; FARM MANAGEMENT
              </div>

              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-950 tracking-tight leading-[1.12]">
                Simple cattle health tracking &amp; fast QR ear tag scanning.
              </h1>

              <p className="text-slate-600 text-base sm:text-lg leading-relaxed max-w-xl">
                A simple, friendly tool built for dairy farmers, field vets, and livestock officers. Scan ear tags in seconds, catch sickness early, and keep your cows healthy and productive.
              </p>

              {/* Quick Jump Matrix */}
              <div className="pt-2 flex flex-wrap gap-3">
                {session ? (
                  <Link
                    href={userDashUrl ?? "/login"}
                    className="btn btn-primary btn-lg shadow-sm"
                  >
                    Open {session.user.role.toUpperCase()} Dashboard →
                  </Link>
                ) : (
                  <>
                    <Link
                      href="/login"
                      className="btn btn-primary btn-lg shadow-sm"
                    >
                      Sign In
                    </Link>
                    <Link
                      href="/register"
                      className="btn btn-secondary btn-lg"
                    >
                      Create Account
                    </Link>
                  </>
                )}
              </div>

              {/* Lively Animated Telemetry Pill Accent */}
              <HeroTelemetryPill />
            </div>

            {/* Right: Interactive Workbench Inspector */}
            <div className="lg:col-span-6">
              <HeroInteractiveWorkbench />
            </div>
          </div>
        </div>
      </section>

      {/* ── Role Capabilities Matrix ──────────────────────── */}
      <section className="py-14 border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl mb-10">
            <h2 className="text-2xl font-bold text-slate-950 tracking-tight">
              Designed for Everyone on the Farm
            </h2>
            <p className="text-slate-600 text-sm mt-1">
              Easy, simple features made specifically for farmers, veterinarians, and local officials.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {capabilities.map((c, i) => (
              <div key={i} className="card p-6 flex flex-col justify-start hover:border-slate-400 transition-colors space-y-3">
                <div>
                  <span className="text-xs font-mono font-bold text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 rounded-full uppercase">
                    {c.role}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-900">{c.title}</h3>
                <p className="text-slate-600 text-sm leading-relaxed">{c.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Verifiable Workflow Architecture ──────────────── */}
      <section className="py-14 bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl mb-10">
            <h2 className="text-2xl font-bold text-slate-950 tracking-tight">
              How SmartCattle Works
            </h2>
            <p className="text-slate-600 text-sm mt-1">
              Simple 4-step workflow to keep your cows healthy every day.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {workflowSteps.map((ws, i) => {
              const Icon = ws.icon;
              return (
                <div key={i} className="card p-5 bg-[#f8faf9] border border-slate-200 flex flex-col gap-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono font-bold text-[#123326] bg-emerald-100 px-2 py-0.5 rounded border border-emerald-200">
                      {ws.step}
                    </span>
                    <Icon className="w-5 h-5 text-[#123326]" />
                  </div>
                  <h4 className="text-base font-bold text-slate-900">{ws.title}</h4>
                  <p className="text-slate-600 text-xs leading-relaxed">{ws.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ── Utilitarian Footer ────────────────────────────── */}
      <footer className="bg-slate-900 text-slate-400 py-8 text-xs font-mono border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3 text-slate-300">
            <SmartCattleLogo variant="light" />
            <span className="hidden md:inline text-slate-500 font-sans text-xs">
              — Smart care for healthier cattle and thriving dairy farms.
            </span>
          </div>
          <div className="flex items-center gap-6">
            <Link href="/login" className="hover:text-white transition-colors">Sign In</Link>
            <Link href="/register" className="hover:text-white transition-colors">Create Account</Link>
            <span className="text-slate-600">|</span>
            <span className="text-slate-400">Designed for Dairy Farmers &amp; Veterinarians</span>
          </div>
        </div>
      </footer>
    </main>
  );
}
