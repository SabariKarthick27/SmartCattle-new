import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { getCHDIBadgeConfig, calcAge, fmt } from "@/lib/utils";
import Link from "next/link";

export default async function MyCattlePage() {
  const session = await getServerSession(authOptions);

  const cattle = await prisma.cattle.findMany({
    where: { farmerId: session!.user.id, isActive: true },
    include: {
      chdiHistory: { orderBy: { timestamp: "desc" }, take: 1 },
      _count: { select: { weightLogs: true, feedLogs: true } },
    },
    orderBy: { createdAt: "desc" },
  });

  return (
    <div className="p-8 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">My Cattle</h1>
          <p className="text-slate-500 mt-1">{cattle.length} animal{cattle.length !== 1 ? "s" : ""} registered</p>
        </div>
        <div className="flex gap-3">
          <Link href="/farmer/scan" className="btn-secondary">Scan QR</Link>
          <Link href="/farmer/cattle/new" id="new-cattle-btn" className="btn-primary">+ Add Cattle</Link>
        </div>
      </div>

      {/* Grid */}
      {cattle.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {cattle.map((c: any) => {
            const latest = c.chdiHistory[0];
            const badge = getCHDIBadgeConfig(latest?.status ?? "abstain");
            return (
              <div
                key={c.id}
                id={`cattle-card-${c.id}`}
                className="card p-5 hover:shadow-md transition-all duration-200 group flex flex-col justify-between relative"
              >
                <div>
                  <div className="flex items-start justify-between mb-4">
                    <Link
                      href={`/farmer/cattle/${c.id}`}
                      className="w-12 h-12 bg-brand-100 rounded-2xl flex items-center justify-center font-bold text-brand-700 text-lg group-hover:scale-105 transition-transform"
                    >
                      {(c.name ?? c.tagId)[0]}
                    </Link>
                    <div className="flex items-center gap-2">
                      <span className={`badge-${latest?.status ?? "abstain"}`}>
                        <span className={`w-1.5 h-1.5 rounded-full ${badge.dot}`}></span>
                        {badge.label}
                      </span>
                      <Link
                        href={`/farmer/cattle/${c.id}/edit`}
                        id={`edit-cattle-btn-${c.id}`}
                        className="p-1.5 text-slate-400 hover:text-brand-700 hover:bg-brand-50 rounded-lg transition-colors"
                        title="Edit Cattle Details"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                        </svg>
                      </Link>
                    </div>
                  </div>

                  <Link href={`/farmer/cattle/${c.id}`} className="block">
                    <h3 className="font-semibold text-slate-900 text-lg hover:text-brand-700 transition-colors">
                      {c.name ?? c.tagId}
                    </h3>
                    <p className="text-sm text-slate-500 mb-3">{c.breed} · {calcAge(c.dob)}</p>

                    <div className="grid grid-cols-2 gap-3 mb-3">
                      <div className="bg-slate-50 rounded-xl p-2.5">
                        <p className="text-xs text-slate-500">Tag ID</p>
                        <p className="text-sm font-medium text-slate-700 font-mono">{c.tagId}</p>
                      </div>
                      <div className="bg-slate-50 rounded-xl p-2.5">
                        <p className="text-xs text-slate-500">CHDI Score</p>
                        <p className={`text-sm font-bold ${badge.color}`}>
                          {latest ? Math.round(latest.score) : "—"}
                          {latest && <span className="text-xs font-normal"> / 100</span>}
                        </p>
                      </div>
                    </div>

                    {/* CHDI mini bar */}
                    {latest && (
                      <div className="h-1.5 bg-slate-200 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all ${
                            latest.status === "healthy" ? "bg-emerald-500" :
                            latest.status === "watch" ? "bg-amber-500" :
                            latest.status === "at-risk" ? "bg-red-500" : "bg-slate-400"
                          }`}
                          style={{ width: `${Math.round(latest.score)}%` }}
                        />
                      </div>
                    )}

                    <div className="flex justify-between mt-3 text-xs text-slate-400">
                      <span>{c._count.weightLogs} weight logs</span>
                      <span>{c._count.feedLogs} feed logs</span>
                    </div>
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="card p-16 text-center">
          <h3 className="text-xl font-semibold text-slate-800 mb-2">No cattle added yet</h3>
          <p className="text-slate-500 mb-6">Add your first animal to start tracking its health</p>
          <Link href="/farmer/cattle/new" className="btn-primary">+ Add your first animal</Link>
        </div>
      )}
    </div>
  );
}
