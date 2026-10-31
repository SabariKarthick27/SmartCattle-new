/**
 * SmartCattle — CHDI Pipeline Orchestrator
 * lib/chdi/pipeline.ts
 *
 * Orchestrates the full health scoring workflow:
 * 1. Checks baseline data sufficiency threshold (N >= 7 entries across >= 5 days)
 * 2. Fetches latest vitals & sends to Python FastAPI ML Microservice (port 8000)
 * 3. Persists CHDIEntry with LOCO factor attributions
 * 4. Automatically creates VetCase tickets for Watch / At-Risk clinical triage
 */

import prisma from "@/lib/prisma";
import { computeCHDI, type DeviationVector } from "./anomaly";
import { MIN_ENTRIES_FOR_BASELINE, MIN_DAYS_FOR_BASELINE } from "@/lib/constants";

export interface BaselineThresholdStatus {
  isMet: boolean;
  minEntries: number;
  details: {
    weight: { entries: number; distinctDays: number; isMet: boolean };
    feed: { entries: number; distinctDays: number; isMet: boolean };
    activity: { entries: number; distinctDays: number; isMet: boolean };
    milk?: { entries: number; distinctDays: number; isMet: boolean };
  };
}

export interface CHDIPipelineResult {
  score: number | null;
  status: "healthy" | "watch" | "at-risk" | "abstain";
  confidence: number;
  triageBand?: string;
  topFactors?: any[];
  entryId?: string;
  farmerText?: string;
  vetText?: string;
}

export function checkBaselineThresholdFromLogs(
  weights: { timestamp: Date | string }[],
  feeds: { timestamp: Date | string }[],
  activities: { timestamp: Date | string }[],
  milks: { timestamp: Date | string }[] = [],
  purpose: string = "dairy"
): BaselineThresholdStatus {
  const getDayKey = (d: Date | string) => (typeof d === "string" ? d.split("T")[0] : d.toISOString().split("T")[0]);

  const wDays = new Set(weights.map((w) => getDayKey(w.timestamp)));
  const fDays = new Set(feeds.map((f) => getDayKey(f.timestamp)));
  const aDays = new Set(activities.map((a) => getDayKey(a.timestamp)));
  const mDays = new Set(milks.map((m) => getDayKey(m.timestamp)));

  const wMet = weights.length >= MIN_ENTRIES_FOR_BASELINE && wDays.size >= MIN_DAYS_FOR_BASELINE;
  const fMet = feeds.length >= MIN_ENTRIES_FOR_BASELINE && fDays.size >= MIN_DAYS_FOR_BASELINE;
  // Activity is OPTIONAL — farmers without sensors are not required to log it.
  // If activity entries exist they are included in the CHDI vector; otherwise omitted.
  const aMet = activities.length >= MIN_ENTRIES_FOR_BASELINE && aDays.size >= MIN_DAYS_FOR_BASELINE;
  const mMet =
    purpose !== "dairy" ||
    (milks.length >= MIN_ENTRIES_FOR_BASELINE && mDays.size >= MIN_DAYS_FOR_BASELINE);

  // Only Weight + Feed + Milk (dairy) are REQUIRED for the baseline gate.
  // Activity / Rumination / Temperature are sensor-optional bonus signals.
  const isMet = wMet && fMet && mMet;
  const requiredEntryCounts = [weights.length, feeds.length];
  if (purpose === "dairy") requiredEntryCounts.push(milks.length);
  const minEntries = Math.min(...requiredEntryCounts);

  return {
    isMet,
    minEntries,
    details: {
      weight: { entries: weights.length, distinctDays: wDays.size, isMet: wMet },
      feed: { entries: feeds.length, distinctDays: fDays.size, isMet: fMet },
      // activity is shown as optional/bonus in the UI but not a gate
      activity: { entries: activities.length, distinctDays: aDays.size, isMet: aMet },
      ...(purpose === "dairy"
        ? { milk: { entries: milks.length, distinctDays: mDays.size, isMet: mMet } }
        : {}),
    },
  };
}

/**
 * Check whether an animal meets the minimum-data threshold (N >= 7 entries across >= 5 days).
 */
export async function checkBaselineThreshold(
  cattleId: string,
  purpose: string = "dairy"
): Promise<BaselineThresholdStatus> {
  const [weights, feeds, activities, milks] = await Promise.all([
    prisma.weightLog.findMany({ where: { cattleId }, select: { timestamp: true } }),
    prisma.feedLog.findMany({ where: { cattleId }, select: { timestamp: true } }),
    prisma.activityLog.findMany({ where: { cattleId }, select: { timestamp: true } }),
    purpose === "dairy"
      ? prisma.milkLog.findMany({ where: { cattleId }, select: { timestamp: true } })
      : Promise.resolve([]),
  ]);

  return checkBaselineThresholdFromLogs(weights, feeds, activities, milks, purpose);
}

/**
 * Run the full CHDI pipeline for an animal after new data has been logged.
 */
export async function runCHDIPipeline(
  cattleId: string,
  actorId: string
): Promise<CHDIPipelineResult | null> {
  try {
    const cattle = await prisma.cattle.findUnique({
      where: { id: cattleId },
      select: { id: true, farmerId: true, region: true, purpose: true },
    });
    if (!cattle) throw new Error(`Cattle ${cattleId} not found`);

    // Check minimum-data threshold
    const thresholdStatus = await checkBaselineThreshold(
      cattleId,
      cattle.purpose ?? "dairy"
    );

    if (!thresholdStatus.isMet) {
      const entriesLogged = Math.min(MIN_ENTRIES_FOR_BASELINE, thresholdStatus.minEntries);
      const explanationText = `Building baseline profile — ${entriesLogged}/${MIN_ENTRIES_FOR_BASELINE} entries logged (needs ~2 weeks of data).`;

      const chdiEntry = await prisma.cHDIEntry.create({
        data: {
          cattleId,
          score: null,
          status: "abstain",
          confidence: 0,
          topFactors: [
            {
              factor: "Building Baseline",
              contribution: 0,
              direction: "up",
              plainLabel: "Baseline Calibration",
              farmerExplanation: explanationText,
              vetExplanation: `Threshold check pending: Requires at least ${MIN_ENTRIES_FOR_BASELINE} entries across ${MIN_DAYS_FOR_BASELINE} days.`,
            },
          ],
        },
      });

      await prisma.auditLog.create({
        data: {
          actorId,
          actorRole: "system",
          action: "chdi_computed",
          targetId: cattleId,
          metadata: {
            score: null,
            status: "abstain",
            confidence: 0,
            chdiEntryId: chdiEntry.id,
            reason: "below_minimum_data_threshold",
            entriesLogged,
          },
        },
      });

      return {
        score: null,
        status: "abstain",
        confidence: 0,
        triageBand: "Abstain (Building Baseline)",
        entryId: chdiEntry.id,
        topFactors: chdiEntry.topFactors as any[],
        farmerText: explanationText,
        vetText: `Threshold check pending: Requires at least ${MIN_ENTRIES_FOR_BASELINE} entries across ${MIN_DAYS_FOR_BASELINE} days.`,
      };
    }

    // Get latest vitals across all signals
    const [latestWeight, latestFeed, latestActivity, latestMilk, latestTemp, latestRum, recentScans] =
      await Promise.all([
        prisma.weightLog.findFirst({ where: { cattleId }, orderBy: { timestamp: "desc" } }),
        prisma.feedLog.findFirst({ where: { cattleId }, orderBy: { timestamp: "desc" } }),
        prisma.activityLog.findFirst({ where: { cattleId }, orderBy: { timestamp: "desc" } }),
        cattle.purpose === "dairy"
          ? prisma.milkLog.findFirst({ where: { cattleId }, orderBy: { timestamp: "desc" } })
          : Promise.resolve(null),
        (prisma as any).temperatureLog?.findFirst({ where: { cattleId }, orderBy: { timestamp: "desc" } }) || Promise.resolve(null),
        (prisma as any).ruminationLog?.findFirst({ where: { cattleId }, orderBy: { timestamp: "desc" } }) || Promise.resolve(null),
        prisma.scanLog.count({
          where: { cattleId, timestamp: { gte: new Date(Date.now() - 7 * 86400000) } },
        }),
      ]);

    // Build deviation vector with only the signals that are actually available.
    // Activity, Rumination, and Temperature are sensor-optional bonus signals.
    // If a farmer has no sensors, Weight + Feed + Milk alone are sufficient.
    const deviationVector: DeviationVector = {
      weightDeviation: latestWeight ? (latestWeight.value - 350) / 15 : 0,
      feedDeviation: latestFeed ? (latestFeed.quantity - 12) / 1.5 : 0,
      scanFrequency: recentScans / 7,
    };

    if (cattle.purpose === "dairy" && latestMilk) {
      deviationVector.milkDeviation = (latestMilk.litres - 25) / 3.0;
    }
    // Activity is optional — only included when a sensor or manual score exists
    if (latestActivity) {
      deviationVector.activityDeviation = (latestActivity.value - 65) / 8;
    }
    // Temperature and Rumination are sensor-only optional enrichment signals
    if (latestTemp) {
      deviationVector.temperatureDeviation = (latestTemp.value - 38.6) / 0.4;
    }
    if (latestRum) {
      deviationVector.ruminationDeviation = (latestRum.minutes - 500) / 40.0;
    }

    // Invoke dedicated Python FastAPI ML Microservice
    const chdiResult = await computeCHDI(deviationVector, cattleId);

    // Persist CHDIEntry with LOCO feature attributions
    const chdiEntry = await prisma.cHDIEntry.create({
      data: {
        cattleId,
        score: chdiResult.score,
        status: chdiResult.status,
        confidence: chdiResult.confidence,
        topFactors: JSON.parse(JSON.stringify(chdiResult.topFactors || [])),
      },
    });

    // Audit log
    await prisma.auditLog.create({
      data: {
        actorId,
        actorRole: "system",
        action: "chdi_computed",
        targetId: cattleId,
        metadata: {
          score: chdiResult.score,
          status: chdiResult.status,
          confidence: chdiResult.confidence,
          chdiEntryId: chdiEntry.id,
        },
      },
    });

    // Auto-create VetCase if watch or at-risk
    if (chdiResult.status === "watch" || chdiResult.status === "at-risk") {
      const existingCase = await prisma.vetCase.findFirst({
        where: {
          cattleId,
          status: { in: ["open", "in_progress"] },
        },
      });

      if (!existingCase) {
        await prisma.vetCase.create({
          data: {
            cattleId,
            farmerId: cattle.farmerId,
            urgency: chdiResult.status === "at-risk" ? "high" : "medium",
            chdiSnapshot: JSON.parse(
              JSON.stringify({
                ...chdiResult,
                topFactors: chdiResult.topFactors || [],
                vetSummary: chdiResult.vetText ?? "Clinical deviation flagged by Python ML service.",
                farmerSummary: chdiResult.farmerText ?? "Advisory alert from Python ML service.",
              })
            ),
          },
        });

        await prisma.auditLog.create({
          data: {
            actorId,
            actorRole: "system",
            action: "vet_case_auto_created",
            targetId: cattleId,
            metadata: {
              status: chdiResult.status,
              score: chdiResult.score,
            },
          },
        });
      }
    }

    return {
      score: chdiResult.score,
      status: chdiResult.status,
      confidence: chdiResult.confidence,
      triageBand:
        chdiResult.status === "healthy"
          ? "Healthy Baseline (CHDI >= 75)"
          : chdiResult.status === "watch"
          ? "Watch (Advisory Bound 50–74)"
          : chdiResult.status === "at-risk"
          ? "At-Risk (Critical Bound < 50)"
          : "Abstain",
      topFactors: chdiResult.topFactors,
      entryId: chdiEntry.id,
      farmerText: chdiResult.farmerText,
      vetText: chdiResult.vetText,
    };
  } catch (error) {
    console.error(`Error running CHDI pipeline for cattle ${cattleId}:`, error);
    return null;
  }
}
