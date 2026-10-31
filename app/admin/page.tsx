import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import Link from "next/link";
import RecentSystemActivity from "./RecentSystemActivity";
import {
  IconUsers,
  IconAudit,
  IconShieldAlert,
} from "@/components/icons";

export default async function AdminOverview() {
  const session = await getServerSession(authOptions);

  const [
    totalCattle,
    totalFarmers,
    totalVets,
    pendingApprovals,
    openCases,
    resolvedThisMonth,
    regionAlerts,
    recentActivity,
    pendingUsers,
  ] = await Promise.all([
    prisma.cattle.count({ where: { isActive: true } }),
    prisma.user.count({ where: { role: "farmer", isVerified: true } }),
    prisma.user.count({ where: { role: "vet", isVerified: true } }),
    prisma.user.count({ where: { isVerified: false, isActive: true } }),
    prisma.vetCase.count({ where: { status: { in: ["open", "in_progress"] } } }),
    prisma.vetCase.count({ where: { status: "resolved", resolvedAt: { gte: new Date(new Date().getFullYear(), new Date().getMonth(), 1) } } }),
    prisma.regionAlert.count({ where: { status: "active" } }),
    prisma.auditLog.findMany({
      orderBy: { timestamp: "desc" },
      take: 8,
      include: { actor: { select: { name: true, role: true } } },
    }),
    prisma.user.findMany({
      where: { isVerified: false, isActive: true },
      orderBy: { createdAt: "desc" },
      take: 5,
      select: { id: true, name: true, email: true, role: true, createdAt: true },
    }),
  ]);

  const stats = [
    { label: "Total Cattle", value: totalCattle, badge: "HERD", color: "text-slate-950", border: "border-slate-300" },
    { label: "Active Farmers", value: totalFarmers, badge: "FARMERS", color: "text-emerald-800", border: "border-emerald-300" },
    { label: "Active Vets", value: totalVets, badge: "DOCTORS", color: "text-blue-800", border: "border-blue-300" },
    { label: "Pending Approvals", value: pendingApprovals, badge: "NEW", color: pendingApprovals > 0 ? "text-amber-800" : "text-slate-700", border: pendingApprovals > 0 ? "border-amber-400 bg-amber-50/40" : "border-slate-300" },
    { label: "Active Vet Cases", value: openCases, badge: "TRIAGE", color: "text-red-800", border: "border-red-300" },
    { label: "Resolved (Month)", value: resolvedThisMonth, badge: "CLEARED", color: "text-slate-800", border: "border-slate-300" },
  ];

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
              System Admin Dashboard
            </h1>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 bg-slate-900 text-white rounded">
              ADMIN
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Admin: {session?.user?.name ?? "Administrator"}
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          {regionAlerts > 0 && (
            <div className="flex items-center gap-1.5 bg-red-50 border border-red-300 rounded px-2.5 py-1 text-xs font-mono font-bold text-red-800">
              <IconShieldAlert className="w-3.5 h-3.5 text-red-600 shrink-0" />
              <span>{regionAlerts} ACTIVE REGIONAL ALERTS</span>
            </div>
          )}
          <Link href="/admin/model" className="btn btn-secondary btn-sm text-xs font-semibold">
            Health AI Settings →
          </Link>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {stats.map((s) => (
          <div key={s.label} className={`card p-3.5 bg-white border ${s.border} flex flex-col justify-between shadow-xs rounded-xl`}>
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

      {/* Main Operational Split */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Pending User Approvals */}
        <div className="lg:col-span-7 space-y-4">
          <div className="card border border-slate-300 bg-white overflow-hidden shadow-xs rounded-xl">
            <div className="p-3.5 bg-[#f8faf9] border-b border-slate-200 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <IconUsers className="w-4 h-4 text-slate-800" />
                <h2 className="font-bold text-xs uppercase font-mono text-slate-900 tracking-wider">
                  Pending Account Approvals
                </h2>
              </div>
              <Link href="/admin/users" className="text-xs font-mono font-bold text-emerald-900 hover:underline">
                View All ({pendingApprovals}) →
              </Link>
            </div>

            <div className="divide-y divide-slate-100">
              {pendingUsers.map((u) => (
                <div key={u.id} className="p-3.5 flex items-center justify-between gap-3 hover:bg-slate-50">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <p className="text-xs font-bold text-slate-950 truncate">{u.name}</p>
                      <span className="text-[10px] font-mono font-bold px-1.5 py-0.2 rounded bg-slate-100 text-slate-700 border border-slate-200 uppercase">
                        {u.role}
                      </span>
                    </div>
                    <p className="text-[11px] font-mono text-slate-500 truncate mt-0.5">{u.email}</p>
                  </div>
                  <Link
                    href={`/admin/users?highlight=${u.id}`}
                    className="btn btn-primary btn-sm text-xs font-semibold py-1 px-3"
                  >
                    Review &amp; Approve →
                  </Link>
                </div>
              ))}

              {pendingUsers.length === 0 && (
                <div className="p-8 text-center text-slate-400 text-xs font-mono">
                  No accounts pending verification. All farmers &amp; vets approved.
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Live Recent Activity Logs */}
        <div className="lg:col-span-5 space-y-4">
          <RecentSystemActivity
            initialLogs={recentActivity.map((log) => ({
              id: log.id,
              action: log.action,
              actorRole: log.actorRole,
              timestamp: log.timestamp.toISOString(),
              actor: log.actor,
            }))}
          />
        </div>
      </div>
    </div>
  );
}
