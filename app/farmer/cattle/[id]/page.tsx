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
    <div className="p-8 space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between flex-wrap gap-4">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-brand-100 rounded-2xl flex items-center justify-center font-bold text-brand-700 text-xl">
            {(cattle.name ?? cattle.tagId)[0]}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-slate-900">
                {cattle.name ?? cattle.tagId}
              </h1>
              {cattle.ageGroup && (
                <span className="text-xs px-2 py-0.5 rounded-md font-semibold capitalize bg-slate-100 text-slate-700 border border-slate-200">
                  {cattle.ageGroup}
                </span>
              )}
              <span className="text-xs px-2 py-0.5 rounded-md font-semibold capitalize bg-brand-50 text-brand-800 border border-brand-200">
                {cattle.purpose}
              </span>
            </div>
            <div className="flex items-center gap-3 mt-1.5 flex-wrap">
              <p className="text-slate-500 text-sm">
                {cattle.breed} · {calcAge(cattle.dob)}
              </p>
              <span className="font-mono text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded-lg font-semibold">
                {cattle.tagId}
              </span>
              <span className={`badge-${isAbstaining ? "abstain" : latest?.status ?? "abstain"}`}>
                <span className={`w-1.5 h-1.5 rounded-full ${badge.dot}`}></span>
                {isAbstaining ? "Abstaining (Calibrating)" : badge.label}
              </span>
            </div>
          </div>
        </div>

        {/* Header Actions */}
        <div className="flex items-center gap-3">
          <Link
            href={`/farmer/cattle/${cattle.id}/edit`}
            id="edit-cattle-details-btn"
            className="btn-secondary py-2 px-3.5 text-sm font-semibold flex items-center gap-2 hover:border-brand-300 hover:text-brand-900 transition-all shadow-sm"
          >
            <svg className="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            <span>Edit Details</span>
          </Link>
        </div>
      </div>

      {/* CHDI Score or Abstaining Baseline Hero */}
      {isAbstaining ? (
        // 6. UI STATE ON CATTLE PROFILE while abstaining:
        // Show "Building health baseline — X/7 entries logged, needs ~2–3 weeks of data"
        <div className="rounded-2xl p-6 border-2 bg-slate-50 border-slate-200 animate-fade-in">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse" />
              <h2 className="font-semibold text-slate-800">Health Baseline Calibration</h2>
            </div>
            <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-200 text-slate-700 uppercase tracking-wide">
              Status: Abstaining
            </span>
          </div>

          <div className="space-y-4">
            <div>
              <p className="text-xl font-bold text-slate-900">
                Building health baseline — {minLogged}/7 entries logged, needs ~2–3 weeks of data
              </p>
              <p className="text-sm text-slate-600 mt-1">
                CHDI scoring abstains until at least {MIN_ENTRIES_FOR_BASELINE} entries across {MIN_DAYS_FOR_BASELINE} distinct days are recorded per signal. Automatic vet alerts activate once the baseline is complete.
              </p>
            </div>

            {/* Visual progress bar */}
            <div>
              <div className="flex justify-between text-xs text-slate-600 mb-1.5 font-medium">
                <span>Calibration progress (limiting signal)</span>
                <span className="font-semibold">{minLogged} / {MIN_ENTRIES_FOR_BASELINE} entries</span>
              </div>
              <div className="h-3 bg-slate-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-brand-600 rounded-full transition-all duration-500"
                  style={{ width: `${Math.round((minLogged / MIN_ENTRIES_FOR_BASELINE) * 100)}%` }}
                />
              </div>
            </div>

            {/* Signal-by-signal breakdown status */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-1">
              <div className={`p-3 rounded-xl border text-xs ${thresholdStatus.details.weight.isMet ? "bg-emerald-50 border-emerald-200" : "bg-white border-slate-200"}`}>
                <div className="flex items-center justify-between font-medium">
                  <span>Weight</span>
                  <span className={thresholdStatus.details.weight.isMet ? "text-emerald-700 font-bold" : "text-slate-500"}>
                    {thresholdStatus.details.weight.isMet ? "✓ Ready" : `${thresholdStatus.details.weight.entries}/7`}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 mt-0.5">{thresholdStatus.details.weight.distinctDays}/5 days</p>
              </div>

              <div className={`p-3 rounded-xl border text-xs ${thresholdStatus.details.feed.isMet ? "bg-emerald-50 border-emerald-200" : "bg-white border-slate-200"}`}>
                <div className="flex items-center justify-between font-medium">
                  <span>Feed</span>
                  <span className={thresholdStatus.details.feed.isMet ? "text-emerald-700 font-bold" : "text-slate-500"}>
                    {thresholdStatus.details.feed.isMet ? "✓ Ready" : `${thresholdStatus.details.feed.entries}/7`}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 mt-0.5">{thresholdStatus.details.feed.distinctDays}/5 days</p>
              </div>

              <div className={`p-3 rounded-xl border text-xs ${thresholdStatus.details.activity.isMet ? "bg-emerald-50 border-emerald-200" : "bg-white border-slate-200"}`}>
                <div className="flex items-center justify-between font-medium">
                  <span>Activity</span>
                  <span className={thresholdStatus.details.activity.isMet ? "text-emerald-700 font-bold" : "text-slate-500"}>
                    {thresholdStatus.details.activity.isMet ? "✓ Ready" : `${thresholdStatus.details.activity.entries}/7`}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 mt-0.5">{thresholdStatus.details.activity.distinctDays}/5 days</p>
              </div>

              {cattle.purpose === "dairy" && thresholdStatus.details.milk && (
                <div className={`p-3 rounded-xl border text-xs ${thresholdStatus.details.milk.isMet ? "bg-emerald-50 border-emerald-200" : "bg-white border-slate-200"}`}>
                  <div className="flex items-center justify-between font-medium">
                    <span>Milk Yield</span>
                    <span className={thresholdStatus.details.milk.isMet ? "text-emerald-700 font-bold" : "text-slate-500"}>
                      {thresholdStatus.details.milk.isMet ? "✓ Ready" : `${thresholdStatus.details.milk.entries}/7`}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 mt-0.5">{thresholdStatus.details.milk.distinctDays}/5 days</p>
                </div>
              )}
            </div>
          </div>
        </div>
      ) : latest && latest.score !== null ? (
        /* Regular CHDI Score hero when threshold met */
        <div
          className={`rounded-2xl p-6 border-2 ${
            latest.status === "at-risk"
              ? "bg-red-50 border-red-200"
              : latest.status === "watch"
              ? "bg-amber-50 border-amber-200"
              : latest.status === "healthy"
              ? "bg-emerald-50 border-emerald-200"
              : "bg-slate-50 border-slate-200"
          }`}
        >
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-semibold text-slate-700">CHDI Score</h2>
            <span className="text-xs text-slate-400">{timeAgo(latest.timestamp)}</span>
          </div>
          <div className="flex items-end gap-4">
            <div>
              <span className={`text-5xl font-bold ${badge.color}`}>
                {Math.round(latest.score)}
              </span>
              <span className="text-slate-400 text-lg"> / 100</span>
            </div>
            <div className="flex-1">
              <div className="h-3 bg-white/80 rounded-full overflow-hidden mb-1">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    latest.status === "healthy"
                      ? "bg-emerald-500"
                      : latest.status === "watch"
                      ? "bg-amber-500"
                      : latest.status === "at-risk"
                      ? "bg-red-500"
                      : "bg-slate-400"
                  }`}
                  style={{ width: `${Math.round(latest.score)}%` }}
                />
              </div>
              <p className={`text-sm ${badge.color}`}>
                Confidence: {Math.round(latest.confidence * 100)}%
              </p>
            </div>
          </div>

          {/* Plain-language explanation */}
          {Array.isArray(latest.topFactors) &&
            (latest.topFactors as Array<{ farmerExplanation: string }>).length > 0 && (
              <div className="mt-4 p-3 bg-white/60 rounded-xl text-sm text-slate-700">
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
