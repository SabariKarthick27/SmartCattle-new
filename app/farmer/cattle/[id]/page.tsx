import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { getCHDIBadgeConfig, calcAge, timeAgo } from "@/lib/utils";
import Link from "next/link";
import { notFound } from "next/navigation";
import CattleProfileClient from "./CattleProfileClient";
import { checkBaselineThreshold } from "@/lib/chdi/pipeline";
import { MIN_ENTRIES_FOR_BASELINE, MIN_DAYS_FOR_BASELINE } from "@/lib/constants";

export default async function CattleProfilePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const session = await getServerSession(authOptions);

  const cattle = await prisma.cattle.findUnique({
    where: { id },
    include: {
      chdiHistory: {
        orderBy: { timestamp: "desc" },
        take: 90,
      },
      weightLogs: { orderBy: { timestamp: "desc" }, take: 60 },
      feedLogs: { orderBy: { timestamp: "desc" }, take: 60 },
      activityLogs: { orderBy: { timestamp: "desc" }, take: 60 },
      milkLogs: { orderBy: { timestamp: "desc" }, take: 60 },
      vaccinationLogs: { orderBy: { createdAt: "desc" } },
      vaccinations: { orderBy: { dueAt: "asc" } },
      vetCases: {
        orderBy: { createdAt: "desc" },
        take: 5,
        include: { vet: { select: { name: true } } },
      },
    },
  });

  if (!cattle) notFound();

  // Access control
  if (
    session!.user.role === "farmer" &&
    cattle.farmerId !== session!.user.id
  ) {
    notFound();
  }

  // Check baseline threshold
  const thresholdStatus = await checkBaselineThreshold(id, cattle.purpose ?? "dairy");
  const latest = cattle.chdiHistory[0];
  const isAbstaining =
    !thresholdStatus.isMet ||
    latest?.status === "abstain" ||
    latest?.score === null ||
    latest?.score === undefined;

  const badge = getCHDIBadgeConfig(isAbstaining ? "abstain" : latest?.status ?? "abstain");
  const minLogged = Math.min(MIN_ENTRIES_FOR_BASELINE, thresholdStatus.minEntries);

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-start justify-between flex-wrap gap-4 pb-4 border-b border-slate-200">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 bg-[#123326] text-emerald-300 rounded-xl flex items-center justify-center font-bold text-xl shadow-sm border border-[#0b2219]">
            {(cattle.name ?? cattle.tagId)[0]}
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h1 className="text-2xl font-bold text-slate-900 font-display">
                {cattle.name ?? cattle.tagId}
              </h1>
              {cattle.ageGroup && (
                <span className="text-xs px-2 py-0.5 rounded font-mono font-semibold capitalize bg-slate-100 text-slate-700 border border-slate-200">
                  {cattle.ageGroup}
                </span>
              )}
              <span className="text-xs px-2 py-0.5 rounded font-mono font-semibold capitalize bg-emerald-50 text-emerald-800 border border-emerald-200">
                {cattle.purpose}
              </span>
            </div>
            <div className="flex items-center gap-3 mt-1.5 flex-wrap">
              <p className="text-slate-600 text-xs font-medium">
                {cattle.breed} · {calcAge(cattle.dob)}
              </p>
              <span className="font-mono text-xs bg-slate-100 text-slate-700 px-2 py-0.5 rounded font-bold border border-slate-200">
                Tag #{cattle.tagId}
              </span>
              <span className={`badge-${isAbstaining ? "abstain" : latest?.status ?? "abstain"}`}>
                <span className={`w-1.5 h-1.5 rounded-full ${badge.dot}`}></span>
                {isAbstaining ? "Calibrating baseline" : badge.label}
              </span>
            </div>
          </div>
        </div>

        {/* Header Actions */}
        <div className="flex items-center gap-3">
          <Link
            href={`/farmer/cattle/${cattle.id}/edit`}
            id="edit-cattle-details-btn"
            className="btn btn-secondary btn-sm flex items-center gap-1.5 text-xs font-semibold"
          >
            <svg className="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            <span>Edit Details</span>
          </Link>
        </div>
      </div>

      {/* CHDI Score or Abstaining Baseline Hero */}
      {isAbstaining ? (
        <div className="rounded-xl p-5 border border-slate-300 bg-white shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse" />
              <h2 className="font-bold text-sm text-slate-800 uppercase font-mono tracking-wider">Health Baseline Learning</h2>
            </div>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-amber-50 text-amber-900 border border-amber-200">
              LEARNING HABITS
            </span>
          </div>

          <div className="space-y-3">
            <div>
              <p className="text-lg font-bold text-slate-900">
                Getting to know your cow — {minLogged}/7 check-ins recorded
              </p>
              <p className="text-xs text-slate-600 mt-0.5">
                The smart health baseline is calculated on a 7-day weekly cycle once at least {MIN_ENTRIES_FOR_BASELINE} entries across {MIN_DAYS_FOR_BASELINE} days are logged. Keep recording weight and milk every few days!
              </p>
            </div>

            {/* Visual progress bar */}
            <div>
              <div className="flex justify-between text-xs text-slate-600 mb-1 font-mono font-semibold">
                <span>Learning Progress</span>
                <span>{minLogged} / {MIN_ENTRIES_FOR_BASELINE} check-ins</span>
              </div>
              <div className="h-2.5 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
                <div
                  className="h-full bg-[#123326] rounded-full transition-all duration-500"
                  style={{ width: `${Math.round((minLogged / MIN_ENTRIES_FOR_BASELINE) * 100)}%` }}
                />
              </div>
            </div>

            {/* Signal-by-signal breakdown status */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1">
              <div className={`p-2.5 rounded-lg border text-xs ${thresholdStatus.details.weight.isMet ? "bg-emerald-50 border-emerald-200" : "bg-[#f8faf9] border-slate-200"}`}>
                <div className="flex items-center justify-between font-semibold">
                  <span>Weight</span>
                  <span className={thresholdStatus.details.weight.isMet ? "text-emerald-800 font-bold" : "text-slate-500 font-mono"}>
                    {thresholdStatus.details.weight.isMet ? "✓ Ready" : `${thresholdStatus.details.weight.entries}/7`}
                  </span>
                </div>
                <p className="text-[10px] font-mono text-slate-400 mt-0.5">{thresholdStatus.details.weight.distinctDays}/5 days</p>
              </div>

              <div className={`p-2.5 rounded-lg border text-xs ${thresholdStatus.details.feed.isMet ? "bg-emerald-50 border-emerald-200" : "bg-[#f8faf9] border-slate-200"}`}>
                <div className="flex items-center justify-between font-semibold">
                  <span>Feed</span>
                  <span className={thresholdStatus.details.feed.isMet ? "text-emerald-800 font-bold" : "text-slate-500 font-mono"}>
                    {thresholdStatus.details.feed.isMet ? "✓ Ready" : `${thresholdStatus.details.feed.entries}/7`}
                  </span>
                </div>
                <p className="text-[10px] font-mono text-slate-400 mt-0.5">{thresholdStatus.details.feed.distinctDays}/5 days</p>
              </div>

              <div className={`p-2.5 rounded-lg border text-xs ${thresholdStatus.details.activity.isMet ? "bg-emerald-50 border-emerald-200" : "bg-[#f8faf9] border-slate-200"}`}>
                <div className="flex items-center justify-between font-semibold">
                  <span>Activity</span>
                  <span className={thresholdStatus.details.activity.isMet ? "text-emerald-800 font-bold" : "text-slate-500 font-mono"}>
                    {thresholdStatus.details.activity.isMet ? "✓ Ready" : `${thresholdStatus.details.activity.entries}/7`}
                  </span>
                </div>
                <p className="text-[10px] font-mono text-slate-400 mt-0.5">{thresholdStatus.details.activity.distinctDays}/5 days</p>
              </div>

              {cattle.purpose === "dairy" && thresholdStatus.details.milk && (
                <div className={`p-2.5 rounded-lg border text-xs ${thresholdStatus.details.milk.isMet ? "bg-emerald-50 border-emerald-200" : "bg-[#f8faf9] border-slate-200"}`}>
                  <div className="flex items-center justify-between font-semibold">
                    <span>Milk Yield</span>
                    <span className={thresholdStatus.details.milk.isMet ? "text-emerald-800 font-bold" : "text-slate-500 font-mono"}>
                      {thresholdStatus.details.milk.isMet ? "✓ Ready" : `${thresholdStatus.details.milk.entries}/7`}
                    </span>
                  </div>
                  <p className="text-[10px] font-mono text-slate-400 mt-0.5">{thresholdStatus.details.milk.distinctDays}/5 days</p>
                </div>
              )}
            </div>
          </div>
        </div>
      ) : latest && latest.score !== null ? (
        /* Regular CHDI Score hero when threshold met */
        <div
          className={`rounded-xl p-5 border shadow-xs ${
            latest.status === "at-risk"
              ? "bg-red-50/80 border-red-300"
              : latest.status === "watch"
              ? "bg-amber-50/80 border-amber-300"
              : latest.status === "healthy"
              ? "bg-emerald-50/80 border-emerald-300"
              : "bg-slate-50 border-slate-300"
          }`}
        >
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-bold text-xs uppercase font-mono tracking-wider text-slate-800">Overall Health Score</h2>
            <span className="text-xs font-mono text-slate-500">{timeAgo(latest.timestamp)}</span>
          </div>
          <div className="flex items-end gap-4">
            <div>
              <span className={`text-4xl sm:text-5xl font-extrabold font-display tnum ${badge.color}`}>
                {Math.round(latest.score)}
              </span>
              <span className="text-slate-400 text-base font-mono font-bold"> / 100</span>
            </div>
            <div className="flex-1">
              <div className="h-2.5 bg-white/90 rounded-full overflow-hidden mb-1 border border-slate-200/50">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    latest.status === "healthy"
                      ? "bg-emerald-600"
                      : latest.status === "watch"
                      ? "bg-amber-500"
                      : latest.status === "at-risk"
                      ? "bg-red-600"
                      : "bg-slate-400"
                  }`}
                  style={{ width: `${Math.round(latest.score)}%` }}
                />
              </div>
              <p className={`text-xs font-medium ${badge.color}`}>
                Status: {badge.label} · Confidence {Math.round(latest.confidence * 100)}%
              </p>
            </div>
          </div>

          {/* Plain-language explanation */}
          {Array.isArray(latest.topFactors) &&
            (latest.topFactors as Array<{ farmerExplanation: string }>).length > 0 && (
              <div className="mt-3 p-3 bg-white/80 rounded-lg text-xs text-slate-800 border border-slate-200/70 font-medium">
                {(latest.topFactors as Array<{ farmerExplanation: string }>)[0]?.farmerExplanation}
              </div>
            )}
        </div>
      ) : null}

      {/* Client interactive section */}
      <CattleProfileClient
        cattleId={id}
        purpose={cattle.purpose ?? "dairy"}
        isAbstaining={isAbstaining}
        minLogged={minLogged}
        chdiHistory={cattle.chdiHistory.map((e) => ({
          score: e.score,
          status: e.status,
          timestamp: e.timestamp.toISOString(),
        }))}
        weightLogs={cattle.weightLogs.map((l) => ({
          value: l.value,
          timestamp: l.timestamp.toISOString(),
          source: l.source,
        }))}
        feedLogs={cattle.feedLogs.map((l) => ({
          quantity: l.quantity,
          feedType: l.feedType,
          timestamp: l.timestamp.toISOString(),
          source: l.source,
        }))}
        milkLogs={cattle.milkLogs.map((m) => ({
          id: m.id,
          litres: m.litres,
          timestamp: m.timestamp.toISOString(),
          source: m.source,
        }))}
        vaccinationLogs={cattle.vaccinationLogs.map((vl) => ({
          id: vl.id,
          vaccineName: vl.vaccineName,
          dateGiven: vl.dateGiven?.toISOString() ?? null,
          nextDueDate: vl.nextDueDate?.toISOString() ?? null,
        }))}
        vaccinations={cattle.vaccinations.map((v) => ({
          id: v.id,
          vaccineType: v.vaccineType,
          dueAt: v.dueAt.toISOString(),
          status: v.status,
          administeredAt: v.administeredAt?.toISOString() ?? null,
        }))}
        vetCases={cattle.vetCases.map((c) => ({
          id: c.id,
          status: c.status,
          urgency: c.urgency,
          createdAt: c.createdAt.toISOString(),
          vetName: c.vet?.name ?? null,
          diagnosis: c.diagnosis,
        }))}
        farmerRole={session!.user.role === "farmer"}
      />
    </div>
  );
}
