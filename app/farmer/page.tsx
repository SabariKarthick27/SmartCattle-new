import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { getCHDIBadgeConfig, timeAgo } from "@/lib/utils";
import Link from "next/link";
import {
  IconCattle,
  IconSyringe,
  IconActivity,
  IconShieldAlert,
  IconScan,
  IconCow,
} from "@/components/icons";

export default async function FarmerOverview() {
  const session = await getServerSession(authOptions);

  const [cattle, recentCHDI, openCases, regionAlerts, upcomingVaccinations] = await Promise.all([
    prisma.cattle.findMany({
      where: { farmerId: session!.user.id, isActive: true },
      include: {
        chdiHistory: { orderBy: { timestamp: "desc" }, take: 7 },
        vaccinations: { where: { status: "upcoming" }, orderBy: { dueAt: "asc" }, take: 1 },
      },
    }),
    prisma.cHDIEntry.findMany({
      where: { cattle: { farmerId: session!.user.id } },
      orderBy: { timestamp: "desc" },
      take: 5,
      include: { cattle: { select: { name: true, tagId: true } } },
    }),
    prisma.vetCase.count({
      where: { farmerId: session!.user.id, status: { in: ["open", "in_progress"] } },
    }),
    prisma.regionAlert.findMany({
      where: { status: "active" },
      orderBy: { triggeredAt: "desc" },
      take: 3,
    }),
    prisma.vaccinationRecord.findMany({
      where: {
        cattle: { farmerId: session!.user.id },
        status: { in: ["upcoming", "overdue"] },
        dueAt: { lte: new Date(Date.now() + 30 * 86400000) },
      },
      orderBy: { dueAt: "asc" },
      take: 5,
      include: { cattle: { select: { name: true, tagId: true } } },
    }),
  ]);

  // Status Metrics Breakdown
  const total = cattle.length;
  const healthy = cattle.filter((c: any) => c.chdiHistory[0]?.status === "healthy").length;
  const atRisk = cattle.filter((c: any) => c.chdiHistory[0]?.status === "at-risk").length;
  const watch = cattle.filter((c: any) => c.chdiHistory[0]?.status === "watch").length;
  const abstain = cattle.filter((c: any) => !c.chdiHistory[0] || c.chdiHistory[0].status === "abstain").length;

  const stats = [
    { label: "Total Cattle", value: total, badge: "TOTAL", color: "text-slate-900", border: "border-slate-300" },
    { label: "Healthy", value: healthy, badge: "GOOD", color: "text-emerald-700", border: "border-emerald-300" },
    { label: "Needs Attention", value: watch, badge: "WATCH", color: "text-amber-700", border: "border-amber-300" },
    { label: "Sick / At Risk", value: atRisk, badge: "URGENT", color: "text-red-700", border: "border-red-300" },
    { label: "Vet Cases", value: openCases, badge: "DOCTOR", color: "text-blue-700", border: "border-blue-300" },
    { label: "New (Calibrating)", value: abstain, badge: "NEW", color: "text-slate-600", border: "border-slate-300" },
  ];

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6">
      {/* ── Operational Header & Quick Action Strip ────────── */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
              My Farm Dashboard
            </h1>
            <span className="text-[11px] font-mono font-bold px-2 py-0.5 bg-emerald-100 text-emerald-900 rounded border border-emerald-300">
              ACTIVE
            </span>
          </div>
          <p className="text-xs text-slate-500 font-mono mt-0.5">
            Farmer: {session!.user.name ?? "Farmer"} · All cattle records up to date
          </p>
        </div>

        {/* Tactical Actions */}
        <div className="flex items-center gap-2.5">
          <Link
            href="/farmer/scan"
            id="quick-scan-btn"
            className="btn btn-primary btn-sm font-mono text-xs font-bold"
          >
            <IconScan className="w-4 h-4 text-emerald-300" />
            <span>SCAN EAR TAG</span>
          </Link>
          <Link
            href="/farmer/cattle/new"
            id="add-cattle-btn"
            className="btn btn-secondary btn-sm text-xs font-semibold"
          >
            + Add New Cow
          </Link>
        </div>
      </div>

      {/* ── Regional Surveillance Callout ─────────────────── */}
      {regionAlerts.length > 0 && (
        <div className="rounded-lg border border-red-300 bg-red-50/90 p-4 shadow-xs">
          <div className="flex items-start gap-3">
            <IconShieldAlert className="w-5 h-5 text-red-700 mt-0.5 shrink-0" />
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-red-900">
                  District Health Alert
                </span>
                <span className="badge-critical text-[10px] py-0">IMPORTANT</span>
              </div>
              <div className="mt-1 space-y-1">
                {regionAlerts.map((a: any) => (
                  <p key={a.id} className="text-xs text-red-800 font-medium">
                    District: <span className="font-bold underline">{a.region}</span> · Severity: <span className="font-bold">{a.severity.toUpperCase()}</span> · Posted {timeAgo(a.triggeredAt)}
                  </p>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── Status Metrics Strip ──────────────────────────── */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {stats.map((s) => (
          <div key={s.label} className={`card p-3.5 bg-white border ${s.border} flex flex-col justify-between`}>
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-mono font-bold text-slate-500">{s.badge}</span>
              <span className="w-1.5 h-1.5 rounded-full bg-slate-300"></span>
            </div>
            <div className="mt-2">
              <div className={`text-2xl font-extrabold tracking-tight font-display tnum ${s.color}`}>
                {s.value}
              </div>
              <div className="text-[11px] font-semibold text-slate-600 truncate mt-0.5">{s.label}</div>
            </div>
          </div>
        ))}
      </div>

      {/* ── Main Operational Grid ─────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Cattle Roster */}
        <div className="lg:col-span-8 space-y-4">
          <div className="card border border-slate-200 bg-white overflow-hidden shadow-xs">
            <div className="p-3.5 bg-[#f8faf9] border-b border-slate-200 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <IconCattle className="w-4 h-4 text-[#123326]" />
                <h2 className="font-bold text-sm text-slate-900 uppercase font-mono tracking-wider">
                  Cattle Health Summary
                </h2>
              </div>
              <Link
                href="/farmer/cattle"
                className="text-xs font-mono font-semibold text-emerald-900 hover:text-emerald-700 underline"
              >
                View All ({total}) →
              </Link>
            </div>

            <div className="divide-y divide-slate-100">
              {cattle.slice(0, 7).map((c: any) => {
                const latest = c.chdiHistory[0];
                const badge = getCHDIBadgeConfig(latest?.status ?? "abstain");
                return (
                  <Link
                    key={c.id}
                    href={`/farmer/cattle/${c.id}`}
                    id={`cattle-row-${c.id}`}
                    className="flex items-center justify-between p-3.5 hover:bg-slate-50 transition-colors group"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <div className="w-9 h-9 bg-slate-100 border border-slate-200 rounded-lg flex items-center justify-center font-mono font-bold text-xs text-slate-700 group-hover:border-[#123326]">
                        {c.tagId.slice(-4)}
                      </div>
                      <div className="min-w-0">
                        <div className="flex items-center gap-2">
                          <p className="font-bold text-sm text-slate-900 truncate">{c.name ?? c.tagId}</p>
                          <span className="text-[11px] font-mono text-slate-500">{c.tagId}</span>
                        </div>
                        <p className="text-xs text-slate-500 truncate">
                          {c.breed} · {c.gender} · Born {new Date(c.dob).getFullYear()}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-3 shrink-0">
                      {latest && (
                        <div className="text-right hidden sm:block">
                          <div className="text-xs font-mono font-bold text-slate-700 tnum">
                            Score: {latest.score != null ? `${Math.round(latest.score)}/100` : "—"}
                          </div>
                          <div className="text-[10px] text-slate-400 font-mono">
                            {timeAgo(latest.timestamp)}
                          </div>
                        </div>
                      )}
                      <span className={`badge-${latest?.status ?? "abstain"}`}>
                        {badge.label}
                      </span>
                    </div>
                  </Link>
                );
              })}

              {cattle.length === 0 && (
                <div className="p-10 text-center text-slate-400 space-y-3">
                  <IconCow className="w-10 h-10 text-slate-300 mx-auto" />
                  <p className="font-bold text-sm text-slate-700">No cattle registered yet</p>
                  <p className="text-xs text-slate-500 max-w-sm mx-auto">
                    Add your first cow or buffalo with an ear tag to track daily health and milk records.
                  </p>
                  <div>
                    <Link href="/farmer/cattle/new" className="btn btn-primary btn-sm">
                      + Add First Cow
                    </Link>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Vaccinations & Telemetry Feed */}
        <div className="lg:col-span-4 space-y-5">
          {/* Upcoming Vaccinations */}
          <div className="card border border-slate-200 bg-white overflow-hidden shadow-xs">
            <div className="p-3.5 bg-[#f8faf9] border-b border-slate-200 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <IconSyringe className="w-4 h-4 text-[#123326]" />
                <h2 className="font-bold text-xs text-slate-900 uppercase font-mono tracking-wider">
                  Upcoming Vaccines
                </h2>
              </div>
              <span className="text-[10px] font-mono text-slate-500">NEXT 30 DAYS</span>
            </div>

            <div className="divide-y divide-slate-100">
              {upcomingVaccinations.slice(0, 4).map((v: any) => (
                <div key={v.id} className="p-3 flex items-center gap-2.5">
                  <div className={`w-2 h-2 rounded-full ${v.status === "overdue" ? "bg-red-600" : "bg-amber-500"}`}></div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-bold text-slate-900 truncate">{v.vaccineType}</p>
                    <p className="text-[11px] font-mono text-slate-500">{v.cattle.name ?? v.cattle.tagId}</p>
                  </div>
                  <span className="text-[11px] font-mono font-semibold text-slate-700 px-1.5 py-0.5 bg-slate-100 rounded border border-slate-200">
                    {new Date(v.dueAt).toLocaleDateString("en-IN", { day: "numeric", month: "short" })}
                  </span>
                </div>
              ))}

              {upcomingVaccinations.length === 0 && (
                <p className="p-4 text-xs font-mono text-slate-400 text-center">
                  All vaccines are currently up to date
                </p>
              )}
            </div>
          </div>

          {/* Recent CHDI Inference Stream */}
          <div className="card border border-slate-200 bg-white overflow-hidden shadow-xs">
            <div className="p-3.5 bg-[#f8faf9] border-b border-slate-200 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <IconActivity className="w-4 h-4 text-[#123326]" />
                <h2 className="font-bold text-xs text-slate-900 uppercase font-mono tracking-wider">
                  Recent Health Checks
                </h2>
              </div>
              <span className="text-[10px] font-mono text-emerald-800 font-bold">LATEST</span>
            </div>

            <div className="divide-y divide-slate-100">
              {recentCHDI.map((e: any) => {
                const badge = getCHDIBadgeConfig(e.status);
                return (
                  <div key={e.id} className="p-3 flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2 min-w-0">
                      <span className={`w-2 h-2 rounded-full ${badge.dot}`}></span>
                      <div className="min-w-0">
                        <p className="text-xs font-semibold text-slate-800 truncate">
                          {e.cattle.name ?? e.cattle.tagId}
                        </p>
                        <p className="text-[10px] font-mono text-slate-400">{timeAgo(e.timestamp)}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className={`badge-${e.status} text-[10px]`}>
                        {e.score != null ? `${Math.round(e.score)} pts` : "—"}
                      </span>
                    </div>
                  </div>
                );
              })}

              {recentCHDI.length === 0 && (
                <p className="p-4 text-xs font-mono text-slate-400 text-center">
                  No health checks logged recently
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
