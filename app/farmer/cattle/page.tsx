import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { getCHDIBadgeConfig, calcAge } from "@/lib/utils";
import Link from "next/link";
import { IconScan, IconCow } from "@/components/icons";
import CattleQrModal from "@/components/CattleQrModal";

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
    <div className="p-4 sm:p-6 lg:p-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-950 tracking-tight font-display">
              My Cattle
            </h1>
            <span className="text-xs font-mono font-bold px-2 py-0.5 bg-slate-200 text-slate-700 rounded">
              {cattle.length} COWS
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <Link href="/farmer/scan" className="btn btn-secondary btn-sm font-mono text-xs font-bold">
            <IconScan className="w-4 h-4 text-emerald-700" />
            <span>Scan Tag</span>
          </Link>
          <Link href="/farmer/cattle/new" id="new-cattle-btn" className="btn btn-primary btn-sm font-semibold text-xs">
            + Add New Cow
          </Link>
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
                className="card p-4 bg-white border border-slate-300 hover:border-slate-400 shadow-xs flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start justify-between mb-3">
                    <Link
                      href={`/farmer/cattle/${c.id}`}
                      className="w-10 h-10 bg-[#123326] text-emerald-300 rounded-lg flex items-center justify-center font-mono font-bold text-sm shadow-xs"
                    >
                      {c.tagId.slice(-4)}
                    </Link>
                    <div className="flex items-center gap-1.5">
                      <span className={`badge-${latest?.status ?? "abstain"}`}>
                        {badge.label}
                      </span>
                      <CattleQrModal
                        cattle={{
                          id: c.id,
                          tagId: c.tagId,
                          name: c.name,
                          breed: c.breed,
                          qrToken: c.qrToken,
                          gender: c.gender,
                          dob: c.dob,
                        }}
                        variant="icon"
                      />
                      <Link
                        href={`/farmer/cattle/${c.id}/edit`}
                        id={`edit-cattle-btn-${c.id}`}
                        className="p-1.5 text-slate-400 hover:text-slate-900 rounded hover:bg-slate-100 transition-colors"
                        title="Edit Cow Details"
                      >
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                        </svg>
                      </Link>
                    </div>
                  </div>

                  <Link href={`/farmer/cattle/${c.id}`} className="block">
                    <h3 className="font-bold text-slate-950 text-base hover:text-emerald-900 transition-colors">
                      {c.name ?? c.tagId}
                    </h3>
                    <p className="text-xs text-slate-500 mb-3">{c.breed} · {c.gender} · {calcAge(c.dob)}</p>

                    <div className="grid grid-cols-2 gap-2 mb-3">
                      <div className="bg-[#f8faf9] border border-slate-200 rounded p-2">
                        <p className="text-[10px] font-mono uppercase text-slate-500">Ear Tag</p>
                        <p className="text-xs font-mono font-bold text-slate-800 truncate">{c.tagId}</p>
                      </div>
                      <div className="bg-[#f8faf9] border border-slate-200 rounded p-2">
                        <p className="text-[10px] font-mono uppercase text-slate-500">Health Score</p>
                        <p className={`text-xs font-mono font-bold ${badge.color}`}>
                          {latest && latest.score != null ? Math.round(latest.score) : "—"}
                          {latest && latest.score != null && <span className="text-[10px] font-normal text-slate-400"> / 100</span>}
                        </p>
                      </div>
                    </div>

                    {/* CHDI mini progress indicator */}
                    {latest && latest.score != null && (
                      <div className="h-1.5 bg-slate-200 rounded-full overflow-hidden mb-3">
                        <div
                          className={`h-full rounded-full ${
                            latest.status === "healthy" ? "bg-emerald-600" :
                            latest.status === "watch" ? "bg-amber-500" :
                            latest.status === "at-risk" ? "bg-red-600" : "bg-slate-400"
                          }`}
                          style={{ width: `${Math.min(100, Math.max(5, Math.round(latest.score)))}%` }}
                        />
                      </div>
                    )}
                  </Link>
                </div>

                <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] font-mono text-slate-500">
                  <span>{c._count.weightLogs + c._count.feedLogs} logs recorded</span>
                  <div className="flex items-center gap-2">
                    <CattleQrModal
                      cattle={{
                        id: c.id,
                        tagId: c.tagId,
                        name: c.name,
                        breed: c.breed,
                        qrToken: c.qrToken,
                        gender: c.gender,
                        dob: c.dob,
                      }}
                      variant="pill"
                    />
                    <Link
                      href={`/farmer/cattle/${c.id}`}
                      className="font-bold text-emerald-900 hover:underline"
                    >
                      View Details →
                    </Link>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="card p-12 text-center text-slate-400 border border-slate-300 space-y-3">
          <IconCow className="w-10 h-10 text-slate-300 mx-auto" />
          <h3 className="font-bold text-base text-slate-800">No Cattle Added Yet</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Click &quot;Add New Cow&quot; to add your first animal and get a printable QR ear tag.
          </p>
          <div className="pt-2">
            <Link href="/farmer/cattle/new" className="btn btn-primary btn-sm">
              + Add First Cow
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
