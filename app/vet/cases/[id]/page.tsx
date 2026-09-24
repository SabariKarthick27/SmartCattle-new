import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { getCHDIBadgeConfig, timeAgo } from "@/lib/utils";
import { notFound } from "next/navigation";
import Link from "next/link";
import VetDiagnoseClient from "./VetDiagnoseClient";

export default async function VetCasePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const session = await getServerSession(authOptions);

  const vetCase = await prisma.vetCase.findUnique({
    where: { id },
    include: {
      cattle: {
        include: {
          chdiHistory: { orderBy: { timestamp: "desc" }, take: 30 },
          weightLogs: { orderBy: { timestamp: "desc" }, take: 15 },
          feedLogs: { orderBy: { timestamp: "desc" }, take: 15 },
        },
      },
      farmer: { select: { name: true, phone: true, email: true } },
      vet: { select: { name: true } },
    },
  });

  if (!vetCase) notFound();

  const latest = vetCase.cattle.chdiHistory[0];
  const badge = getCHDIBadgeConfig(latest?.status ?? "abstain");
  const snapshot = (vetCase.chdiSnapshot as Record<string, unknown>) ?? {};
  const topFactors = (snapshot?.topFactors as Array<{ factor: string; contribution: number; direction: string; vetExplanation: string }>) ?? [];

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center gap-2 text-xs font-mono text-slate-500 pb-2 border-b border-slate-200">
        <Link href="/vet" className="hover:text-slate-900 font-bold">← Case Queue</Link>
        <span>/</span>
        <span>Case #{id.slice(-6)}</span>
      </div>

      {/* Header */}
      <div className="flex items-start justify-between flex-wrap gap-4">
        <div className="flex items-center gap-3.5">
          <div className="w-12 h-12 bg-[#0f3d32] text-emerald-300 rounded-xl flex items-center justify-center font-bold text-lg font-mono">
            {(vetCase.cattle.name ?? vetCase.cattle.tagId)[0]}
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-slate-950 font-display">
              {vetCase.cattle.name ?? vetCase.cattle.tagId}
            </h1>
            <div className="flex items-center gap-2 mt-1 flex-wrap">
              <span className="text-slate-600 text-xs font-mono font-bold">Tag #{vetCase.cattle.tagId}</span>
              <span className="text-slate-500 text-xs">· {vetCase.cattle.breed}</span>
              <span className={`badge-${vetCase.urgency} text-[10px]`}>{vetCase.urgency.toUpperCase()} PRIORITY</span>
              <span className={`badge-${latest?.status ?? "abstain"} text-[10px]`}>
                <span className={`w-1.5 h-1.5 rounded-full ${badge.dot}`}></span>
                Score: {latest && latest.score !== null ? Math.round(latest.score) : "—"}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: CHDI Details */}
        <div className="lg:col-span-2 space-y-6">
          {/* CHDI Snapshot at case creation */}
          <div className="card p-5 bg-white border border-slate-300 shadow-xs rounded-xl space-y-4">
            <h2 className="font-bold text-sm text-slate-950 uppercase font-mono tracking-wider">
              Health Analysis at Case Creation
            </h2>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-[#f8faf9] rounded-lg p-3 border border-slate-200">
                <p className="text-[10px] font-mono uppercase text-slate-500 font-bold mb-1">Health Score</p>
                <p className={`text-2xl font-extrabold font-display ${badge.color}`}>
                  {snapshot.score != null ? Math.round(Number(snapshot.score)) : "—"}
                </p>
              </div>
              <div className="bg-[#f8faf9] rounded-lg p-3 border border-slate-200">
                <p className="text-[10px] font-mono uppercase text-slate-500 font-bold mb-1">AI Confidence</p>
                <p className="text-2xl font-extrabold text-slate-800 font-display">
                  {snapshot.confidence != null ? `${Math.round(Number(snapshot.confidence) * 100)}%` : "—"}
                </p>
              </div>
            </div>

            {/* Factor breakdown */}
            {topFactors.length > 0 && (
              <div className="pt-2">
                <h3 className="text-xs font-bold text-slate-800 uppercase font-mono mb-2">Key Health Signals</h3>
                <div className="space-y-2">
                  {topFactors.map((f, i) => (
                    <div key={i} className="p-2.5 rounded-lg bg-[#f8faf9] border border-slate-200 text-xs">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-bold text-slate-900">{f.factor?.replace(/([A-Z])/g, " $1").trim()}</span>
                        <span className={`font-mono font-bold ${f.direction === "down" ? "text-red-700" : "text-emerald-700"}`}>
                          {f.direction === "down" ? "↓ Drop" : "↑ High"} {Math.round((f.contribution ?? 0) * 100)}%
                        </span>
                      </div>
                      <p className="text-slate-600 text-[11px]">{f.vetExplanation}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Farmer info & symptoms */}
          <div className="card p-5 bg-white border border-slate-300 shadow-xs rounded-xl space-y-3">
            <h2 className="font-bold text-sm text-slate-950 uppercase font-mono tracking-wider">Farmer Report</h2>
            <div className="grid grid-cols-3 gap-3 text-xs">
              <div><p className="text-[10px] text-slate-400 uppercase font-mono">Farmer</p><p className="font-bold text-slate-900">{vetCase.farmer.name}</p></div>
              <div><p className="text-[10px] text-slate-400 uppercase font-mono">Phone</p><p className="font-mono text-slate-800">{vetCase.farmer.phone}</p></div>
              <div><p className="text-[10px] text-slate-400 uppercase font-mono">Reported</p><p className="text-slate-700">{timeAgo(vetCase.createdAt)}</p></div>
            </div>
            {vetCase.symptoms && (
              <div className="bg-amber-50 rounded-lg p-3 border border-amber-200">
                <p className="text-[11px] font-bold text-amber-900 mb-0.5 font-mono uppercase">Symptoms Observed:</p>
                <p className="text-xs text-amber-950">{vetCase.symptoms}</p>
              </div>
            )}
          </div>
        </div>

        {/* Right: Diagnosis form */}
        <div>
          <VetDiagnoseClient
            caseId={id}
            cattleId={vetCase.cattleId}
            existingDiagnosis={{
              symptoms: vetCase.symptoms ?? "",
              diagnosis: vetCase.diagnosis ?? "",
              treatment: vetCase.treatment ?? "",
              medication: vetCase.medication ?? "",
              followUpDate: vetCase.followUpDate?.toISOString().split("T")[0] ?? "",
              status: vetCase.status,
            }}
            predictedStatus={String(snapshot.status ?? "unknown")}
          />
        </div>
      </div>
    </div>
  );
}
