import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import Link from "next/link";
import { getCHDIBadgeConfig, fmtDate } from "@/lib/utils";
import {
  IconBell,
  IconShieldAlert,
  IconStethoscope,
  IconCheckCircle,
} from "@/components/icons";

export default async function NotificationsPage() {
  const session = await getServerSession(authOptions);
  if (!session) return null;

  // 1. Fetch farmer's cattle
  const farmerCattle = await prisma.cattle.findMany({
    where: { farmerId: session.user.id, isActive: true },
    select: { id: true, tagId: true, name: true, region: true },
  });

  const cattleIds = farmerCattle.map((c) => c.id);
  const farmerRegion = session.user.assignedRegion || farmerCattle[0]?.region || "Tamil Nadu - Coimbatore";

  // 2. Fetch CHDI score alerts (scores < 75 or status watch/at-risk)
  const healthAlerts = await prisma.cHDIEntry.findMany({
    where: {
      cattleId: { in: cattleIds },
      status: { in: ["watch", "at-risk"] },
    },
    include: { cattle: { select: { tagId: true, name: true } } },
    orderBy: { timestamp: "desc" },
    take: 10,
  });

  // 3. Fetch Vet Cases updates
  const vetCases = await prisma.vetCase.findMany({
    where: { farmerId: session.user.id },
    include: {
      cattle: { select: { tagId: true, name: true } },
      vet: { select: { name: true, phone: true } },
    },
    orderBy: { createdAt: "desc" },
    take: 10,
  });

  // 4. Fetch Vaccinations
  const vaccinations = await prisma.vaccinationRecord.findMany({
    where: { cattleId: { in: cattleIds } },
    include: { cattle: { select: { tagId: true, name: true } } },
    orderBy: { dueAt: "asc" },
    take: 10,
  });

  // 5. Fetch Regional Alerts
  const regionAlerts = await prisma.regionAlert.findMany({
    where: { region: farmerRegion, status: "active" },
    orderBy: { triggeredAt: "desc" },
    take: 5,
  });

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="pb-4 border-b border-slate-200">
        <div className="flex items-center gap-2">
          <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
            Alerts &amp; Messages
          </h1>
          <span className="text-xs font-mono font-bold px-2 py-0.5 bg-slate-200 text-slate-700 rounded">
            NOTIFICATIONS
          </span>
        </div>
      </div>

      {/* Region Outbreak Banner */}
      {regionAlerts.length > 0 && (
        <div className="space-y-3">
          {regionAlerts.map((alert) => (
            <div
              key={alert.id}
              className="p-4 rounded-xl bg-red-50 border border-red-300 text-red-900 flex items-start justify-between shadow-xs"
            >
              <div className="flex items-start gap-3">
                <IconShieldAlert className="w-5 h-5 text-red-700 shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-bold text-red-900 text-sm">
                    District Disease Warning ({alert.region})
                  </h3>
                  <p className="text-xs text-red-800 mt-0.5">
                    Contagious animal sickness detected in your district. Severity: <span className="font-bold uppercase">{alert.severity}</span>. Keep your cows monitored and wash pens thoroughly.
                  </p>
                  <p className="text-[11px] font-mono text-red-700 mt-1 font-semibold">
                    Posted {fmtDate(alert.triggeredAt)}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Notifications List */}
      <div className="space-y-3">
        {/* Health Alerts */}
        {healthAlerts.map((alert) => {
          const badge = getCHDIBadgeConfig(alert.status);
          const cattleName = alert.cattle.name || alert.cattle.tagId;
          return (
            <div
              key={alert.id}
              className="card p-4 bg-white border border-slate-300 hover:border-slate-400 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-l-4 border-l-amber-500 rounded-lg shadow-xs"
            >
              <div className="flex items-start gap-3">
                <div className="w-9 h-9 bg-amber-50 text-amber-800 border border-amber-200 rounded-lg flex items-center justify-center font-bold shrink-0">
                  <IconShieldAlert className="w-5 h-5 text-amber-700" />
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-0.5">
                    <h4 className="font-bold text-slate-950 text-sm">
                      Health Check Warning for {cattleName}
                    </h4>
                    <span className={`badge-${alert.status} text-[10px]`}>
                      {badge.label}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600">
                    Health score dropped to <span className="font-bold text-amber-800 font-mono">{alert.score != null ? Math.round(alert.score) : "—"}/100</span>. Please check feed and milk today.
                  </p>
                  <p className="text-[10px] font-mono text-slate-400 mt-0.5">
                    {fmtDate(alert.timestamp)}
                  </p>
                </div>
              </div>
              <Link
                href={`/farmer/cattle/${alert.cattleId}`}
                className="btn btn-secondary btn-sm text-xs font-semibold shrink-0"
              >
                View Cow →
              </Link>
            </div>
          );
        })}

        {/* Vet Cases */}
        {vetCases.map((vc) => {
          const cattleName = vc.cattle.name || vc.cattle.tagId;
          return (
            <div
              key={vc.id}
              className={`card p-4 bg-white border border-slate-300 hover:border-slate-400 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-l-4 rounded-lg shadow-xs ${
                vc.status === "open" ? "border-l-blue-500" : "border-l-emerald-500"
              }`}
            >
              <div className="flex items-start gap-3">
                <div className={`w-9 h-9 rounded-lg border flex items-center justify-center shrink-0 ${
                  vc.status === "open" ? "bg-blue-50 border-blue-200 text-blue-800" : "bg-emerald-50 border-emerald-200 text-emerald-800"
                }`}>
                  <IconStethoscope className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-0.5">
                    <h4 className="font-bold text-slate-950 text-sm">
                      {vc.symptoms?.includes("Weekly Health Analysis")
                        ? `Weekly Health Report (${cattleName})`
                        : `Doctor Visit for ${cattleName}`}
                    </h4>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold font-mono ${
                      vc.status === "open" ? "bg-blue-100 text-blue-800" : "bg-emerald-100 text-emerald-800"
                    }`}>
                      {vc.status.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600">
                    {vc.treatment ? `Prescription: ${vc.treatment}` : vc.diagnosis ? `Doctor Diagnosis: ${vc.diagnosis}` : `Reported: ${vc.symptoms ?? "Doctor is reviewing"}`}
                  </p>
                  <p className="text-[10px] font-mono text-slate-400 mt-0.5">
                    Vet: {vc.vet?.name ? (vc.vet.name.startsWith("Dr.") ? vc.vet.name : `Dr. ${vc.vet.name}`) : "Dr. Sivanarasimman S"} · {fmtDate(vc.createdAt)}
                  </p>
                </div>
              </div>
              <Link
                href={`/farmer/cattle/${vc.cattleId}`}
                className="btn btn-secondary btn-sm text-xs font-semibold shrink-0"
              >
                View Details →
              </Link>
            </div>
          );
        })}

        {/* Vaccination Alerts */}
        {vaccinations.map((vac) => {
          const cattleName = vac.cattle.name || vac.cattle.tagId;
          const isOverdue = new Date(vac.dueAt) < new Date() && vac.status !== "done";
          return (
            <div
              key={vac.id}
              className={`card p-4 bg-white border border-slate-300 hover:border-slate-400 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-l-4 rounded-lg shadow-xs ${
                isOverdue ? "border-l-red-500" : vac.status === "done" ? "border-l-emerald-500" : "border-l-indigo-500"
              }`}
            >
              <div className="flex items-start gap-3">
                <div className="w-9 h-9 bg-emerald-50 border border-emerald-200 text-emerald-900 rounded-lg flex items-center justify-center font-bold shrink-0">
                  <IconBell className="w-4 h-4 text-emerald-800" />
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-0.5">
                    <h4 className="font-bold text-slate-950 text-sm">
                      Upcoming Vaccine: {vac.vaccineType}
                    </h4>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold font-mono ${
                      isOverdue ? "bg-red-100 text-red-800" : vac.status === "done" ? "bg-emerald-100 text-emerald-800" : "bg-indigo-100 text-indigo-800"
                    }`}>
                      {isOverdue ? "OVERDUE" : vac.status.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600">
                    Cow: <span className="font-bold text-slate-900">{cattleName}</span> · Due date: {fmtDate(vac.dueAt)}
                  </p>
                </div>
              </div>
              <Link
                href={`/farmer/cattle/${vac.cattleId}`}
                className="btn btn-secondary btn-sm text-xs font-semibold shrink-0"
              >
                Mark Vaccine Given →
              </Link>
            </div>
          );
        })}

        {healthAlerts.length === 0 && vetCases.length === 0 && vaccinations.length === 0 && (
          <div className="card p-12 text-center bg-white border border-slate-300 shadow-xs rounded-xl space-y-2">
            <IconCheckCircle className="w-10 h-10 text-emerald-600 mx-auto" />
            <h3 className="text-base font-bold text-slate-900">All Clear! No Pending Alerts</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">Your cattle are healthy with no urgent doctor requests or overdue vaccines.</p>
          </div>
        )}
      </div>
    </div>
  );
}
