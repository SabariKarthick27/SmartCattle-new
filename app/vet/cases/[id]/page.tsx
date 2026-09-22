import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { getCHDIBadgeConfig, timeAgo, getUrgencyConfig } from "@/lib/utils";
import { notFound } from "next/navigation";
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
  const snapshot = vetCase.chdiSnapshot as Record<string, unknown>;
  const topFactors = (snapshot?.topFactors as Array<{ factor: string; contribution: number; direction: string; vetExplanation: string }>) ?? [];

  return (
    <div className="p-8 space-y-6 max-w-5xl">
      <div className="flex items-center gap-2 text-sm text-slate-500 mb-2">
        <a href="/vet" className="hover:text-slate-700">← Case Queue</a>
        <span>/</span>
        <span>Case #{id.slice(-6)}</span>
      </div>

      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 bg-brand-100 rounded-2xl flex items-center justify-center font-bold text-brand-700 text-lg">
            {(vetCase.cattle.name ?? vetCase.cattle.tagId)[0]}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900">
              {vetCase.cattle.name ?? vetCase.cattle.tagId}
            </h1>
            <div className="flex gap-3 mt-1">
              <span className="text-slate-500 text-sm">{vetCase.cattle.breed}</span>
              <span className={`badge-${vetCase.urgency}`}>{vetCase.urgency} urgency</span>
              <span className={`badge-${latest?.status ?? "abstain"}`}>
                <span className={`w-1.5 h-1.5 rounded-full ${badge.dot}`}></span>
                CHDI: {latest ? Math.round(latest.score) : "—"}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: CHDI Details */}
        <div className="lg:col-span-2 space-y-6">
          {/* CHDI Snapshot at case creation */}
          <div className="card p-6">
            <h2 className="font-semibold text-slate-900 mb-4">CHDI at Case Creation</h2>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-slate-50 rounded-xl p-3">
                <p className="text-xs text-slate-500 mb-1">CHDI Score</p>
                <p className={`text-2xl font-bold ${badge.color}`}>
                  {snapshot.score != null ? Math.round(Number(snapshot.score)) : "—"}
                </p>
              </div>
              <div className="bg-slate-50 rounded-xl p-3">
                <p className="text-xs text-slate-500 mb-1">Confidence</p>
                <p className="text-2xl font-bold text-slate-700">
                  {snapshot.confidence != null ? `${Math.round(Number(snapshot.confidence) * 100)}%` : "—"}
                </p>
              </div>
            </div>

            {/* Full permutation importance breakdown (vet level) */}
            {topFactors.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold text-slate-700 mb-3">Signal Contributions (Permutation Importance)</h3>
                <div className="space-y-2">
                  {topFactors.map((f, i) => (
                    <div key={i} className="flex items-center gap-3">
                      <span className="text-xs text-slate-400 w-4">{i + 1}.</span>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs font-medium text-slate-700">{f.factor?.replace(/([A-Z])/g, " $1").trim()}</span>
                          <span className={`text-xs font-bold ${f.direction === "down" ? "text-red-600" : "text-emerald-600"}`}>
                            {f.direction === "down" ? "↓" : "↑"} {Math.round((f.contribution ?? 0) * 100)}%
                          </span>
                        </div>
                        <div className="h-1.5 bg-slate-200 rounded-full">
                          <div
                            className={`h-full rounded-full ${f.direction === "down" ? "bg-red-400" : "bg-emerald-400"}`}
                            style={{ width: `${Math.round((f.contribution ?? 0) * 100)}%` }}
                          />
                        </div>
                        <p className="text-xs text-slate-400 mt-0.5">{f.vetExplanation}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Farmer info & symptoms */}
          <div className="card p-6">
            <h2 className="font-semibold text-slate-900 mb-3">Farmer Report</h2>
            <div className="grid grid-cols-3 gap-3 mb-3 text-sm">
              <div><p className="text-xs text-slate-400">Farmer</p><p className="font-medium">{vetCase.farmer.name}</p></div>
              <div><p className="text-xs text-slate-400">Phone</p><p className="font-medium">{vetCase.farmer.phone}</p></div>
              <div><p className="text-xs text-slate-400">Reported</p><p className="font-medium">{timeAgo(vetCase.createdAt)}</p></div>
            </div>
            {vetCase.symptoms && (
              <div className="bg-amber-50 rounded-xl p-3 border border-amber-200">
                <p className="text-xs font-semibold text-amber-700 mb-1">Observed symptoms:</p>
                <p className="text-sm text-amber-900">{vetCase.symptoms}</p>
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
