import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { getCHDIBadgeConfig, getUrgencyConfig, timeAgo } from "@/lib/utils";
import Link from "next/link";
import { IconStethoscope } from "@/components/icons";

export default async function VetQueuePage() {
  const session = await getServerSession(authOptions);

  const cases = await prisma.vetCase.findMany({
    where: {
      status: { in: ["open", "in_progress"] },
      OR: [
        { vetId: session!.user.id },
        { vetId: null },
      ],
    },
    include: {
      cattle: {
        select: {
          tagId: true, breed: true, name: true, region: true,
          chdiHistory: {
            orderBy: { timestamp: "desc" },
            take: 5,
            select: { score: true, status: true, timestamp: true },
          },
        },
      },
      farmer: { select: { name: true, phone: true } },
    },
    orderBy: [{ urgency: "desc" }, { createdAt: "asc" }],
  });

  const urgencyOrder: Record<string, number> = { critical: 0, high: 1, medium: 2, low: 3 };
  const sorted = [...cases].sort((a, b) => (urgencyOrder[a.urgency] ?? 9) - (urgencyOrder[b.urgency] ?? 9));

  const stats = {
    total: cases.length,
    critical: cases.filter((c) => c.urgency === "critical").length,
    high: cases.filter((c) => c.urgency === "high").length,
    unassigned: cases.filter((c) => !c.vetId).length,
  };

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2.5">
            <IconStethoscope className="w-6 h-6 text-teal-700" />
            Case Queue
          </h1>
          <p className="text-slate-500 mt-1">Cases requiring veterinary evaluation and diagnosis</p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Open Cases", value: stats.total, color: "text-slate-900", bg: "bg-white" },
          { label: "Critical", value: stats.critical, color: "text-red-700", bg: "bg-red-50" },
          { label: "High Priority", value: stats.high, color: "text-orange-700", bg: "bg-orange-50" },
          { label: "Unassigned", value: stats.unassigned, color: "text-amber-700", bg: "bg-amber-50" },
        ].map((s) => (
          <div key={s.label} className={`card p-4 ${s.bg}`}>
            <div className={`text-2xl font-bold ${s.color}`}>{s.value}</div>
            <div className="text-xs text-slate-500 mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Cases table */}
      <div className="card overflow-hidden">
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Animal</th>
                <th>Farmer</th>
                <th>Region</th>
                <th>CHDI Score</th>
                <th>Urgency</th>
                <th>Status</th>
                <th>Requested</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((c) => {
                const latestCHDI = c.cattle.chdiHistory[0];
                const badge = getCHDIBadgeConfig(latestCHDI?.status ?? "abstain");
                const urgency = getUrgencyConfig(c.urgency);
                return (
                  <tr key={c.id}>
                    <td>
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-brand-100 rounded-lg flex items-center justify-center font-bold text-brand-700 text-xs">
                          {(c.cattle.name ?? c.cattle.tagId)[0]}
                        </div>
                        <div>
                          <p className="font-medium text-slate-900">{c.cattle.name ?? c.cattle.tagId}</p>
                          <p className="text-xs text-slate-500">{c.cattle.breed}</p>
                        </div>
                      </div>
                    </td>
                    <td>
                      <p className="text-slate-700">{c.farmer.name}</p>
                      <p className="text-xs text-slate-400">{c.farmer.phone}</p>
                    </td>
                    <td className="text-slate-600">{c.cattle.region ?? "—"}</td>
                    <td>
                      {latestCHDI ? (
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-slate-800">{Math.round(latestCHDI.score)}</span>
                          <span className={`badge-${latestCHDI.status}`}>
                            <span className={`w-1.5 h-1.5 rounded-full ${badge.dot}`}></span>
                            {badge.label}
                          </span>
                        </div>
                      ) : "—"}
                    </td>
                    <td><span className={`badge-${c.urgency}`}>{c.urgency}</span></td>
                    <td>
                      <span className={`text-xs font-medium px-2 py-1 rounded-full ${c.status === "in_progress" ? "bg-blue-100 text-blue-700" : "bg-slate-100 text-slate-600"}`}>
                        {c.status.replace("_", " ")}
                      </span>
                    </td>
                    <td className="text-slate-400 text-xs">{timeAgo(c.createdAt)}</td>
                    <td>
                      <Link
                        href={`/vet/cases/${c.id}`}
                        id={`case-view-${c.id}`}
                        className="btn-secondary btn-sm"
                      >
                        View →
                      </Link>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          {cases.length === 0 && (
            <div className="p-12 text-center text-slate-400">
              <IconStethoscope className="w-10 h-10 text-slate-300 mx-auto mb-2" />
              <p className="font-medium">No open cases</p>
              <p className="text-sm mt-1">All cases have been resolved or are not yet assigned</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
