import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { getCHDIBadgeConfig, timeAgo } from "@/lib/utils";
import Link from "next/link";
import { IconCattle, IconSyringe, IconActivity, IconShieldAlert } from "@/components/icons";

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

  // Stats
  const total = cattle.length;
  const healthy = cattle.filter((c: any) => c.chdiHistory[0]?.status === "healthy").length;
  const atRisk = cattle.filter((c: any) => c.chdiHistory[0]?.status === "at-risk").length;
  const watch = cattle.filter((c: any) => c.chdiHistory[0]?.status === "watch").length;
  const abstain = cattle.filter((c: any) => !c.chdiHistory[0] || c.chdiHistory[0].status === "abstain").length;

  const stats = [
    { label: "Total Animals", value: total, color: "text-slate-900", bg: "bg-slate-50" },
    { label: "Healthy", value: healthy, color: "text-emerald-700", bg: "bg-emerald-50" },
    { label: "Watch", value: watch, color: "text-amber-700", bg: "bg-amber-50" },
    { label: "At Risk", value: atRisk, color: "text-red-700", bg: "bg-red-50" },
    { label: "Open Cases", value: openCases, color: "text-blue-700", bg: "bg-blue-50" },
    { label: "No Data Yet", value: abstain, color: "text-slate-500", bg: "bg-slate-50" },
  ];

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">
            Good {getGreeting()}, {session!.user.name?.split(" ")[0]}!
          </h1>
          <p className="text-slate-500 mt-1">Here&apos;s your herd health overview</p>
        </div>
        <Link href="/farmer/cattle/new" id="add-cattle-btn" className="btn-primary">
          + Add Cattle
        </Link>
      </div>

      {/* Regional Alert Banner */}
      {regionAlerts.length > 0 && (
        <div className="animate-pulse-ring rounded-2xl border-2 border-red-200 bg-red-50 p-5">
          <div className="flex items-start gap-3">
            <IconShieldAlert className="w-5 h-5 text-red-600 mt-0.5 shrink-0" />
            <div>
              <p className="font-semibold text-red-800">Regional Health Alert</p>
              {regionAlerts.map((a: any) => (
                <p key={a.id} className="text-red-700 text-sm mt-0.5">
                  <strong>{a.severity.toUpperCase()}</strong> alert in <strong>{a.region}</strong> — {timeAgo(a.triggeredAt)}
                </p>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Stats grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {stats.map((s) => (
          <div key={s.label} className={`card p-4 ${s.bg}`}>
            <div className={`text-2xl font-bold ${s.color}`}>{s.value}</div>
            <div className="text-xs text-slate-500 mt-1 font-medium">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Main grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cattle list (recent) */}
        <div className="lg:col-span-2 card">
          <div className="p-5 border-b border-slate-100 flex items-center justify-between">
            <h2 className="font-semibold text-slate-900 flex items-center gap-2">
              <IconCattle className="w-4 h-4 text-brand-700" />
              Your Herd
            </h2>
            <Link href="/farmer/cattle" className="text-sm text-brand-700 hover:underline">
              View all →
            </Link>
          </div>
          <div className="divide-y divide-slate-100">
            {cattle.slice(0, 6).map((c: any) => {
              const latest = c.chdiHistory[0];
              const badge = getCHDIBadgeConfig(latest?.status ?? "abstain");
              return (
                <Link
                  key={c.id}
                  href={`/farmer/cattle/${c.id}`}
                  id={`cattle-row-${c.id}`}
                  className="flex items-center gap-4 p-4 hover:bg-slate-50 transition-colors"
                >
                  <div className="w-10 h-10 bg-brand-100 rounded-xl flex items-center justify-center font-bold text-brand-700 text-sm">
                    {c.name?.[0]?.toUpperCase() ?? "C"}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-slate-900 truncate">{c.name ?? c.tagId}</p>
                    <p className="text-xs text-slate-500">{c.breed}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    {latest && (
                      <span className="text-lg font-bold text-slate-700">{Math.round(latest.score)}</span>
                    )}
                    <span className={`badge-${latest?.status ?? "abstain"}`}>
                      <span className={`w-1.5 h-1.5 rounded-full ${badge.dot}`}></span>
                      {badge.label}
                    </span>
                  </div>
                </Link>
              );
            })}
            {cattle.length === 0 && (
              <div className="p-8 text-center text-slate-400">
                <IconCattle className="w-10 h-10 text-slate-300 mx-auto mb-2" />
                <p className="font-medium">No cattle added yet</p>
                <Link href="/farmer/cattle/new" className="btn-primary mt-3 inline-flex">Add your first animal</Link>
              </div>
            )}
          </div>
        </div>

        {/* Right column */}
        <div className="space-y-6">
          {/* Upcoming vaccinations */}
          <div className="card">
            <div className="p-4 border-b border-slate-100">
              <h2 className="font-semibold text-slate-900 flex items-center gap-2">
                <IconSyringe className="w-4 h-4 text-brand-700" />
                Upcoming Vaccinations
              </h2>
            </div>
            <div className="divide-y divide-slate-100">
              {upcomingVaccinations.slice(0, 4).map((v: any) => (
                <div key={v.id} className="p-3.5 flex items-center gap-3">
                  <div className={`w-2 h-2 rounded-full ${v.status === "overdue" ? "bg-red-500" : "bg-amber-500"}`}></div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-800 truncate">{v.vaccineType}</p>
                    <p className="text-xs text-slate-500">{v.cattle.name ?? v.cattle.tagId}</p>
                  </div>
                  <p className="text-xs text-slate-400 whitespace-nowrap">
                    {new Date(v.dueAt).toLocaleDateString("en-IN", { day: "numeric", month: "short" })}
                  </p>
                </div>
              ))}
              {upcomingVaccinations.length === 0 && (
                <p className="p-4 text-sm text-slate-400 text-center">No upcoming vaccinations</p>
              )}
            </div>
          </div>

          {/* Recent CHDI activity */}
          <div className="card">
            <div className="p-4 border-b border-slate-100">
              <h2 className="font-semibold text-slate-900 flex items-center gap-2">
                <IconActivity className="w-4 h-4 text-brand-700" />
                Recent Health Events
              </h2>
            </div>
            <div className="divide-y divide-slate-100">
              {recentCHDI.map((e: any) => {
                const badge = getCHDIBadgeConfig(e.status);
                return (
                  <div key={e.id} className="p-3.5 flex items-center gap-3">
                    <span className={`w-2 h-2 rounded-full ${badge.dot}`}></span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-slate-700 truncate">
                        {e.cattle.name ?? e.cattle.tagId} → <span className={badge.color}>{badge.label}</span>
                      </p>
                      <p className="text-xs text-slate-400">{timeAgo(e.timestamp)}</p>
                    </div>
                    <p className="text-sm font-bold text-slate-600">{Math.round(e.score)}</p>
                  </div>
                );
              })}
              {recentCHDI.length === 0 && (
                <p className="p-4 text-sm text-slate-400 text-center">No health events yet</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function getGreeting() {
  const h = new Date().getHours();
  if (h < 12) return "morning";
  if (h < 17) return "afternoon";
  return "evening";
}
