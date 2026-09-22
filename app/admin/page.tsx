import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import Link from "next/link";
import {
  IconOverview,
  IconUsers,
  IconAudit,
  IconShieldAlert,
} from "@/components/icons";

export default async function AdminOverview() {
  const session = await getServerSession(authOptions);

  const [
    totalCattle, totalFarmers, totalVets, pendingApprovals, openCases, resolvedThisMonth, regionAlerts
  ] = await Promise.all([
    prisma.cattle.count({ where: { isActive: true } }),
    prisma.user.count({ where: { role: "farmer", isVerified: true } }),
    prisma.user.count({ where: { role: "vet", isVerified: true } }),
    prisma.user.count({ where: { isVerified: false, isActive: true } }),
    prisma.vetCase.count({ where: { status: { in: ["open", "in_progress"] } } }),
    prisma.vetCase.count({ where: { status: "resolved", resolvedAt: { gte: new Date(new Date().getFullYear(), new Date().getMonth(), 1) } } }),
    prisma.regionAlert.count({ where: { status: "active" } }),
  ]);

  const recentActivity = await prisma.auditLog.findMany({
    orderBy: { timestamp: "desc" },
    take: 8,
    include: { actor: { select: { name: true, role: true } } },
  });

  const pendingUsers = await prisma.user.findMany({
    where: { isVerified: false, isActive: true },
    orderBy: { createdAt: "desc" },
    take: 5,
    select: { id: true, name: true, email: true, role: true, createdAt: true },
  });

  const stats = [
    { label: "Total Cattle", value: totalCattle, gradient: "from-emerald-500 to-emerald-600" },
    { label: "Active Farmers", value: totalFarmers, gradient: "from-teal-500 to-teal-600" },
    { label: "Active Vets", value: totalVets, gradient: "from-blue-500 to-blue-600" },
    { label: "Pending Approvals", value: pendingApprovals, gradient: "from-amber-500 to-amber-600", alert: pendingApprovals > 0 },
    { label: "Open Cases", value: openCases, gradient: "from-orange-500 to-orange-600" },
    { label: "Resolved This Month", value: resolvedThisMonth, gradient: "from-slate-500 to-slate-600" },
  ];

  return (
    <div className="p-8 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2.5">
            <IconOverview className="w-6 h-6 text-slate-800" />
            Admin Console
          </h1>
          <p className="text-slate-500 mt-1">SmartCattle platform overview and system metrics</p>
        </div>
        {regionAlerts > 0 && (
          <div className="flex items-center gap-2 bg-red-50 border border-red-200 rounded-xl px-4 py-2.5">
            <IconShieldAlert className="w-4 h-4 text-red-600 shrink-0" />
            <span className="text-red-700 text-sm font-medium">{regionAlerts} active regional alert{regionAlerts > 1 ? "s" : ""}</span>
          </div>
        )}
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {stats.map((s) => (
          <div key={s.label} className={`rounded-2xl p-4 bg-gradient-to-br ${s.gradient} text-white relative overflow-hidden ${s.alert ? "ring-2 ring-amber-400 ring-offset-2" : ""}`}>
            <div className="text-3xl font-bold mt-1">{s.value}</div>
            <div className="text-white/80 text-xs mt-1 font-medium">{s.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pending approvals */}
        <div className="card">
          <div className="p-5 border-b border-slate-100 flex items-center justify-between">
            <h2 className="font-semibold text-slate-900 flex items-center gap-2">
              <IconUsers className="w-4 h-4 text-brand-700" />
              Pending Approvals
            </h2>
            <Link href="/admin/users?verified=false" className="text-sm text-brand-700 hover:underline">View all →</Link>
          </div>
          <div className="divide-y divide-slate-100">
            {pendingUsers.map((u) => (
              <div key={u.id} className="p-4 flex items-center gap-3">
                <div className="w-9 h-9 bg-amber-100 rounded-full flex items-center justify-center">
                  <span className="text-amber-700 text-sm font-bold">{u.name[0]}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-slate-900 truncate">{u.name}</p>
                  <p className="text-xs text-slate-500">{u.email} · {u.role}</p>
                </div>
                <Link href={`/admin/users`} id={`approve-${u.id}`} className="btn-primary btn-sm">Review</Link>
              </div>
            ))}
            {pendingUsers.length === 0 && (
              <p className="p-5 text-slate-400 text-sm text-center">No pending approvals</p>
            )}
          </div>
        </div>

        {/* Recent audit log */}
        <div className="card">
          <div className="p-5 border-b border-slate-100 flex items-center justify-between">
            <h2 className="font-semibold text-slate-900 flex items-center gap-2">
              <IconAudit className="w-4 h-4 text-brand-700" />
              Recent Activity
            </h2>
            <Link href="/admin/audit" className="text-sm text-brand-700 hover:underline">Full log →</Link>
          </div>
          <div className="divide-y divide-slate-100">
            {recentActivity.map((log) => (
              <div key={log.id} className="px-4 py-3 flex items-center gap-3">
                <div className="w-7 h-7 bg-slate-100 rounded-lg flex items-center justify-center text-xs font-semibold text-slate-600 uppercase">
                  {log.actorRole?.[0]}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-slate-700 truncate">
                    <span className="font-medium">{log.actor.name}</span> — {log.action.replace(/_/g, " ")}
                  </p>
                </div>
                <p className="text-xs text-slate-400 whitespace-nowrap">
                  {new Date(log.timestamp).toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" })}
                </p>
              </div>
            ))}
            {recentActivity.length === 0 && (
              <p className="p-5 text-slate-400 text-sm text-center">No activity yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
