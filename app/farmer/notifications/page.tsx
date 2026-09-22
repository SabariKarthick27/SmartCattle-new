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
    <div className="p-8 space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2.5">
          <IconBell className="w-6 h-6 text-brand-700" />
          Farmer Notifications & Alerts
        </h1>
        <p className="text-slate-500 mt-1">
          Real-time health alerts, veterinary updates, regional warnings, and vaccination schedules
        </p>
      </div>

      {/* Region Outbreak Banner */}
      {regionAlerts.length > 0 && (
        <div className="space-y-3">
          {regionAlerts.map((alert) => (
            <div
              key={alert.id}
              className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 flex items-start justify-between"
            >
              <div className="flex items-start gap-3">
                <IconShieldAlert className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-bold text-amber-900 text-sm">
                    Regional Health Advisory ({alert.region})
                  </h3>
                  <p className="text-xs text-amber-800 mt-0.5">
                    Health anomalies detected in your district. Severity: <span className="font-bold capitalize">{alert.severity}</span>. Keep cattle monitored and maintain hygiene.
                  </p>
                  <p className="text-[11px] text-amber-600 mt-1">
                    Triggered: {fmtDate(alert.triggeredAt)}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Notifications List */}
      <div className="space-y-4">
        {/* Health Alerts */}
        {healthAlerts.map((alert) => {
          const badge = getCHDIBadgeConfig(alert.status);
          const cattleName = alert.cattle.name || alert.cattle.tagId;
          return (
            <div
              key={alert.id}
              className="card p-5 hover:shadow-md transition-shadow flex items-start justify-between border-l-4 border-l-amber-500"
            >
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 bg-amber-100 rounded-xl flex items-center justify-center text-amber-700 font-bold shrink-0">
                  <IconShieldAlert className="w-5 h-5 text-amber-700" />
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="font-bold text-slate-900 text-base">
                      Health Drop Warning for {cattleName}
                    </h4>
                    <span className={`badge-${alert.status}`}>
                      {badge.label}
                    </span>
                  </div>
                  <p className="text-sm text-slate-600">
                    CHDI Health Index dropped to <span className="font-bold text-amber-700">{Math.round(alert.score)}/100</span>. Animal requires observation.
                  </p>
                  <p className="text-xs text-slate-400 mt-1">
                    Recorded on {fmtDate(alert.timestamp)}
                  </p>
                </div>
              </div>
              <Link
                href={`/farmer/cattle/${alert.cattleId}`}
                className="btn-secondary btn-sm"
              >
                View Profile →
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
              className={`card p-5 hover:shadow-md transition-shadow flex items-start justify-between border-l-4 ${
                vc.status === "open" ? "border-l-blue-500" : "border-l-emerald-500"
              }`}
            >
              <div className="flex items-start gap-4">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${
                  vc.status === "open" ? "bg-blue-100 text-blue-700" : "bg-emerald-100 text-emerald-700"
                }`}>
                  <IconStethoscope className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="font-bold text-slate-900 text-base">
                      {vc.symptoms?.includes("Weekly Health Analysis")
                        ? `Weekly Veterinary Health Analysis (${cattleName})`
                        : `Veterinary Case #${vc.id.slice(-6)} (${cattleName})`}
                    </h4>
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                      vc.symptoms?.includes("Weekly Health Analysis")
                        ? "bg-teal-100 text-teal-800"
                        : vc.status === "open" ? "bg-blue-100 text-blue-800" : "bg-emerald-100 text-emerald-800"
                    }`}>
                      {vc.symptoms?.includes("Weekly Health Analysis") ? "WEEKLY REPORT" : vc.status.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-sm text-slate-600">
                    {vc.treatment ? `Vet Notes: ${vc.treatment}` : vc.diagnosis ? `Diagnosis: ${vc.diagnosis}` : `Symptoms reported: ${vc.symptoms ?? "Under vet evaluation"}`}
                  </p>
                  {vc.symptoms?.includes("Weekly Health Analysis") && (
                    <p className="text-xs text-teal-700 font-medium mt-1">
                      Report Period: 7-Day Rolling Weekly Evaluation
                    </p>
                  )}
                  <p className="text-xs text-slate-400 mt-1">
                    Vet: {vc.vet?.name ?? "Assigned District Vet"} · Created {fmtDate(vc.createdAt)}
                  </p>
                </div>
              </div>
              <Link
                href={`/farmer/cattle/${vc.cattleId}`}
                className="btn-secondary btn-sm"
              >
                Case Details →
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
              className={`card p-5 hover:shadow-md transition-shadow flex items-start justify-between border-l-4 ${
                isOverdue ? "border-l-red-500" : vac.status === "done" ? "border-l-emerald-500" : "border-l-indigo-500"
              }`}
            >
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 bg-indigo-100 rounded-xl flex items-center justify-center text-indigo-700 font-bold shrink-0">
                  <svg className="w-5 h-5 text-indigo-700" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19 14.5M14.25 3.104c.251.023.501.05.75.082M19 14.5a3.75 3.75 0 01-7.5 0" />
                  </svg>
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="font-bold text-slate-900 text-base">
                      Vaccination Schedule: {vac.vaccineType}
                    </h4>
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                      isOverdue ? "bg-red-100 text-red-800" : vac.status === "done" ? "bg-emerald-100 text-emerald-800" : "bg-indigo-100 text-indigo-800"
                    }`}>
                      {isOverdue ? "OVERDUE" : vac.status.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-sm text-slate-600">
                    Animal: <span className="font-semibold">{cattleName}</span> · Due date: {fmtDate(vac.dueAt)}
                  </p>
                </div>
              </div>
              <Link
                href={`/farmer/cattle/${vac.cattleId}`}
                className="btn-secondary btn-sm"
              >
                Record Vaccination →
              </Link>
            </div>
          );
        })}

        {healthAlerts.length === 0 && vetCases.length === 0 && vaccinations.length === 0 && (
          <div className="card p-12 text-center">
            <IconCheckCircle className="w-12 h-12 text-emerald-500 mx-auto mb-3" />
            <h3 className="text-lg font-bold text-slate-800 mb-1">All Clear: No Pending Notifications</h3>
            <p className="text-slate-500 text-sm">Your registered cattle have no critical health alerts or pending vaccination warnings.</p>
          </div>
        )}
      </div>
    </div>
  );
}
