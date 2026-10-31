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

      {/* Stacked Layout: Case Summary Top, Diagnosis Horizontal Below */}
      <div className="space-y-6">
        {/* Full-width Case Summary */}
        <div className="card p-5 bg-white border border-slate-300 shadow-xs rounded-xl space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <h2 className="font-bold text-sm text-slate-900 uppercase font-mono tracking-wider">
              Case Summary &amp; Vitals
            </h2>
            <span className={`text-xs px-2.5 py-0.5 rounded-full font-bold uppercase font-mono ${badge.bg} ${badge.color}`}>
              Score: {snapshot.score != null ? Math.round(Number(snapshot.score)) : latest?.score != null ? Math.round(Number(latest.score)) : "—"}/100
            </span>
          </div>

          {/* Essential Contact & Meta Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
            <div>
              <p className="text-[10px] text-slate-400 uppercase font-mono font-bold">Farmer</p>
              <p className="font-bold text-slate-900 text-sm mt-0.5">{vetCase.farmer.name}</p>
            </div>
            <div>
              <p className="text-[10px] text-slate-400 uppercase font-mono font-bold">Phone</p>
              <p className="font-mono font-bold text-slate-800 mt-0.5">{vetCase.farmer.phone}</p>
            </div>
            <div>
              <p className="text-[10px] text-slate-400 uppercase font-mono font-bold">Logged</p>
              <p className="text-slate-700 mt-0.5">{timeAgo(vetCase.createdAt)}</p>
            </div>
          </div>

          {/* Observed Symptoms */}
          {vetCase.symptoms && (
            <div className="bg-amber-50 rounded-lg p-3.5 border border-amber-200/80">
              <p className="text-[10px] font-bold text-amber-900 font-mono uppercase tracking-wider mb-1">
                Reported Symptoms / Reason:
              </p>
              <p className="text-xs text-amber-950 leading-relaxed font-medium">
                {vetCase.symptoms}
              </p>
            </div>
          )}
        </div>

        {/* Full-width Clinical Diagnosis Form Horizontal Below */}
        <VetDiagnoseClient
          caseId={id}
          cattleId={vetCase.cattleId}
          breed={vetCase.cattle.breed}
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
  );
}
