import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { getCHDIBadgeConfig, timeAgo } from "@/lib/utils";
import Link from "next/link";
import { IconStethoscope } from "@/components/icons";

export default async function VetQueuePage() {
  const session = await getServerSession(authOptions);

  const fetchCases = async () => {
    return prisma.vetCase.findMany({
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
      orderBy: [{ urgency: "desc" }, { createdAt: "desc" }],
    });
  };

  let cases: any[] = [];
  try {
    cases = await fetchCases();
  } catch (err) {
    // Graceful automatic retry to handle Neon serverless compute wake-up delay
    try {
      await new Promise((res) => setTimeout(res, 1200));
      cases = await fetchCases();
    } catch (e2) {
      console.error("Neon DB retry failed:", e2);
      cases = [];
    }
  }

  const urgencyOrder: Record<string, number> = { critical: 0, high: 1, medium: 2, low: 3 };
  const sorted = [...cases].sort((a, b) => {
    const diff = (urgencyOrder[a.urgency] ?? 9) - (urgencyOrder[b.urgency] ?? 9);
    if (diff !== 0) return diff;
    return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
  });

  const stats = {
    total: cases.length,
    critical: cases.filter((c) => c.urgency === "critical").length,
    high: cases.filter((c) => c.urgency === "high").length,
    unassigned: cases.filter((c) => !c.vetId).length,
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
              Urgent Cattle Cases &amp; Queue
            </h1>
            <span className="text-xs font-mono font-bold px-2 py-0.5 bg-red-100 text-red-900 rounded border border-red-300">
              {stats.critical} CRITICAL
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Link href="/vet/weekly-analysis" className="btn btn-secondary btn-sm text-xs">
            Weekly Reports →
          </Link>
        </div>
      </div>

      {/* Stats Summary Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { label: "Total Cases", value: stats.total, badge: "QUEUE", color: "text-slate-900", border: "border-slate-300" },
          { label: "Critical Cases", value: stats.critical, badge: "URGENT", color: "text-red-700", border: "border-red-300" },
          { label: "High Risk Cows", value: stats.high, badge: "HIGH", color: "text-orange-700", border: "border-orange-300" },
          { label: "New / Unclaimed", value: stats.unassigned, badge: "NEW", color: "text-amber-700", border: "border-amber-300" },
        ].map((s) => (
          <div key={s.label} className={`card p-3.5 bg-white border ${s.border} flex flex-col justify-between shadow-xs`}>
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

      {/* Triage Cases Table */}
      <div className="card overflow-hidden border border-slate-300 bg-white shadow-xs">
        <div className="p-3 bg-[#f8faf9] border-b border-slate-200 flex items-center justify-between">
          <span className="text-xs font-mono font-bold uppercase text-slate-700">
            Active Case List ({sorted.length} Waiting)
          </span>
          <span className="text-[10px] font-mono text-slate-500">Sorted by Urgency</span>
        </div>

        <div className="table-container border-0 rounded-none">
          <table className="table">
            <thead>
              <tr>
                <th>Cattle &amp; Tag</th>
                <th>Farmer Contact</th>
                <th>District</th>
                <th>Health Score</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Reported</th>
                <th className="text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((c) => {
                const latestCHDI = c.cattle.chdiHistory[0];
                const badge = getCHDIBadgeConfig(latestCHDI?.status ?? "abstain");
                return (
                  <tr key={c.id} className="hover:bg-[#f8faf9] transition-colors">
                    <td>
                      <div className="flex items-center gap-2.5">
                        <div className="w-8 h-8 bg-[#0f3d32] text-emerald-300 rounded font-mono font-bold text-xs flex items-center justify-center">
                          {c.cattle.tagId.slice(-4)}
                        </div>
                        <div>
                          <p className="font-bold text-slate-900 text-xs">{c.cattle.name ?? c.cattle.tagId}</p>
                          <p className="text-[11px] font-mono text-slate-500">{c.cattle.tagId} · {c.cattle.breed}</p>

                        </div>
                      </div>
                    </td>
                    <td>
                      <p className="text-xs font-semibold text-slate-800">{c.farmer.name}</p>
                      <p className="text-[11px] font-mono text-slate-500">{c.farmer.phone}</p>
                    </td>
                    <td className="text-xs font-mono text-slate-600">{c.cattle.region ?? "—"}</td>
                    <td>
                      {latestCHDI && latestCHDI.score !== null ? (
                        <div className="flex items-center gap-2">
                          <span className="font-mono font-bold text-slate-900 text-xs tnum">
                            {Math.round(latestCHDI.score)}
                          </span>
                          <span className={`badge-${latestCHDI.status} text-[10px]`}>
                            {badge.label}
                          </span>
                        </div>
                      ) : (
                        <span className="text-slate-400 text-xs">—</span>
                      )}
                    </td>
                    <td>
                      <span className={`badge-${c.urgency} text-[10px]`}>
                        {c.urgency.toUpperCase()}
                      </span>
                    </td>
                    <td>
                      <span className="text-[11px] font-mono font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200 uppercase">
                        {c.status.replace("_", " ")}
                      </span>
                    </td>
                    <td className="text-slate-500 text-[11px] font-mono whitespace-nowrap">{timeAgo(c.createdAt)}</td>
                    <td className="text-right">
                      <Link
                        href={`/vet/cases/${c.id}`}
                        prefetch={true}
                        id={`case-view-${c.id}`}
                        className="btn btn-secondary btn-sm text-xs font-semibold"
                      >
                        Diagnose →
                      </Link>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>

          {cases.length === 0 && (
            <div className="p-12 text-center text-slate-400 space-y-2">
              <IconStethoscope className="w-8 h-8 text-slate-300 mx-auto" />
              <p className="font-bold text-sm text-slate-700">No Pending Urgent Cases</p>
              <p className="text-xs text-slate-500">All cattle in your area are currently healthy or treated.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
