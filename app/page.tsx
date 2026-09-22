import Link from "next/link";
import { getServerSession } from "next-auth";
import { authOptions } from "./api/auth/[...nextauth]/route";
import { redirect } from "next/navigation";
import { IconCattle, IconScan, IconAudit, IconStethoscope, IconCow } from "@/components/icons";

export default async function Home() {
  const session = await getServerSession(authOptions);

  if (session) {
    const dashMap: Record<string, string> = {
      farmer: "/farmer",
      vet: "/vet",
      admin: "/admin",
    };
    redirect(dashMap[session.user.role] ?? "/login");
  }

  const steps = [
    {
      num: "1",
      icon: IconScan,
      title: "Scan the QR Tag",
      desc: "Point your phone at the cattle tag — its full profile opens instantly.",
    },
    {
      num: "2",
      icon: IconAudit,
      title: "Log Health Data",
      desc: "Record weight, feed, and symptoms in seconds. History is saved automatically.",
    },
    {
      num: "3",
      icon: IconStethoscope,
      title: "Vet Gets Notified",
      desc: "If something looks off, the system flags it and alerts an assigned vet.",
    },
  ];

  return (
    <main className="min-h-screen bg-slate-50 flex flex-col">
      {/* ── Hero ─────────────────────────────────────────── */}
      <div className="gradient-hero text-white relative overflow-hidden">
        {/* Decorative blobs */}
        <div className="absolute -top-32 -left-32 w-80 h-80 bg-white/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-20 -right-20 w-72 h-72 bg-emerald-300/10 rounded-full blur-3xl pointer-events-none" />

        {/* Nav */}
        <nav className="relative z-10 flex items-center justify-between px-6 md:px-10 py-5">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-sm border border-white/30 shadow-sm">
              <IconCow className="w-5 h-5 text-white" />
            </div>
            <span className="text-white font-bold text-xl tracking-tight">SmartCattle</span>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/login" className="text-white/80 hover:text-white text-sm font-medium transition-colors px-4 py-2">
              Sign in
            </Link>
            <Link href="/register" className="bg-white text-brand-950 rounded-xl px-4 py-2 text-sm font-semibold hover:bg-brand-50 transition-all shadow-md active:scale-[0.98]">
              Register
            </Link>
          </div>
        </nav>

        {/* Hero content */}
        <div className="relative z-10 flex flex-col items-center text-center px-6 pt-12 pb-24 max-w-2xl mx-auto">
          <div className="w-20 h-20 bg-white/20 rounded-2xl flex items-center justify-center border border-white/30 backdrop-blur-sm mb-6 animate-fade-in-up shadow-lg">
            <IconCow className="w-10 h-10 text-white" />
          </div>

          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 leading-tight tracking-tight animate-fade-in-up">
            Keep Your Herd
            <span className="block text-emerald-300 mt-1">Healthy & Safe</span>
          </h1>

          <p className="text-white/75 text-base max-w-md mb-10 leading-relaxed animate-fade-in-up">
            Scan a QR tag · Log health notes · Get vet alerts.
            <br />Works on any phone, no extra hardware.
          </p>

          <div className="flex flex-col sm:flex-row items-center gap-3 w-full sm:w-auto animate-fade-in-up">
            <Link
              href="/register"
              id="hero-register-btn"
              className="btn-primary btn-lg bg-white text-brand-950 hover:bg-emerald-50 w-full sm:w-auto shadow-xl font-bold"
            >
              Register →
            </Link>
            <Link
              href="/login"
              id="hero-login-btn"
              className="btn-secondary btn-lg bg-white/15 text-white border-white/30 hover:bg-white/25 backdrop-blur-sm w-full sm:w-auto"
            >
              Sign in
            </Link>
          </div>
        </div>
      </div>

      {/* ── How it works ─────────────────────────────────── */}
      <div className="flex-1 bg-white border-t border-slate-100 px-6 md:px-12 py-16">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-slate-900 text-center mb-2">How SmartCattle Works</h2>
          <p className="text-slate-400 text-sm text-center mb-10">Three simple steps — no training needed</p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {steps.map((s, i) => {
              const Icon = s.icon;
              return (
                <div
                  key={i}
                  className="flex flex-col items-center text-center gap-4 bg-slate-50 rounded-2xl border border-slate-200 p-7 hover:shadow-md hover:-translate-y-1 transition-all duration-300 animate-fade-in-up"
                  style={{ animationDelay: `${i * 0.12}s` }}
                >
                  <div className="w-14 h-14 bg-brand-50 border border-brand-200/80 rounded-2xl flex items-center justify-center">
                    <Icon className="w-7 h-7 text-brand-700" />
                  </div>
                  <div>
                    <span className="inline-block text-xs font-bold text-brand-700 bg-brand-50 border border-brand-200 rounded-full px-3 py-1 mb-2">
                      Step {s.num}
                    </span>
                    <h3 className="text-slate-900 font-bold text-lg mb-2">{s.title}</h3>
                    <p className="text-slate-500 text-sm leading-relaxed">{s.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </main>
  );
}
