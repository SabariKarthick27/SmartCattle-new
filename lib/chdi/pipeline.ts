/**
 * SmartCattle — CHDI Pipeline Orchestrator
 * lib/chdi/pipeline.ts
 *
 * Orchestrates the full health scoring pipeline:
 * New data logged → computeBaseline() → deviation calculated → computeCHDI()
 * → if confidence low, status = abstain (no alert)
 * → if watch/at-risk, auto-create VetCase with CHDI snapshot + explainScore() output
 * → vet confirms/overrides → logged to VetFeedback
 * → periodic retrainClassifier() job
 */

import prisma from "@/lib/prisma";
import { computeBaseline } from "./baseline";
import { computeCHDI, type DeviationVector } from "./anomaly";
import { explainScore } from "./explain";
import { MIN_ENTRIES_FOR_BASELINE, MIN_DAYS_FOR_BASELINE } from "@/lib/constants";

// ─────────────────────────────────────────────────────────────
// Baseline Data Threshold Checker
// ─────────────────────────────────────────────────────────────

export interface BaselineThresholdStatus {
  isMet: boolean;
  minEntries: number; // minimum entries logged across required signals
  details: {
    weight: { entries: number; distinctDays: number; isMet: boolean };
    feed: { entries: number; distinctDays: number; isMet: boolean };
    activity: { entries: number; distinctDays: number; isMet: boolean };
    milk?: { entries: number; distinctDays: number; isMet: boolean };
  };
}

/**
 * Check whether an animal meets the explicit minimum-data threshold:
 * MIN_ENTRIES_FOR_BASELINE = 7 entries across at least MIN_DAYS_FOR_BASELINE = 5
 * distinct calendar days, per required signal type (weight, feed, activity, and milk if dairy).
 * Scan-pattern is supplementary and does not block scoring.
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

  const getDayKey = (d: Date) => d.toISOString().split("T")[0];

  const wDays = new Set(weights.map((w) => getDayKey(w.timestamp)));
  const fDays = new Set(feeds.map((f) => getDayKey(f.timestamp)));
  const aDays = new Set(activities.map((a) => getDayKey(a.timestamp)));
  const mDays = new Set(milks.map((m) => getDayKey(m.timestamp)));

  const wMet = weights.length >= MIN_ENTRIES_FOR_BASELINE && wDays.size >= MIN_DAYS_FOR_BASELINE;
  const fMet = feeds.length >= MIN_ENTRIES_FOR_BASELINE && fDays.size >= MIN_DAYS_FOR_BASELINE;
  const aMet = activities.length >= MIN_ENTRIES_FOR_BASELINE && aDays.size >= MIN_DAYS_FOR_BASELINE;
  const mMet =
    purpose !== "dairy" ||
    (milks.length >= MIN_ENTRIES_FOR_BASELINE && mDays.size >= MIN_DAYS_FOR_BASELINE);

  const isMet = wMet && fMet && aMet && mMet;

  const requiredEntryCounts = [weights.length, feeds.length, activities.length];
  if (purpose === "dairy") requiredEntryCounts.push(milks.length);
  const minEntries = Math.min(...requiredEntryCounts);

  return {
    isMet,
    minEntries,
    details: {
      weight: { entries: weights.length, distinctDays: wDays.size, isMet: wMet },
      feed: { entries: feeds.length, distinctDays: fDays.size, isMet: fMet },
      activity: { entries: activities.length, distinctDays: aDays.size, isMet: aMet },
      ...(purpose === "dairy"
        ? { milk: { entries: milks.length, distinctDays: mDays.size, isMet: mMet } }
        : {}),
    },
  };
}

// ─────────────────────────────────────────────────────────────
// Main pipeline entry point
// ─────────────────────────────────────────────────────────────

/**
 * Run the full CHDI pipeline for an animal after new data has been logged.
 * - If below the minimum data threshold: returns status: "abstain" and skips VetCase creation.
 * - Once threshold is met: runs computeBaseline(), computeCHDI(), and auto-creates VetCase if watch/at-risk.
 *
 * @param cattleId  The cattle to score
 * @param actorId   The user who triggered the log (for audit)
 */
export async function runCHDIPipeline(
  cattleId: string,
  actorId: string
): Promise<void> {
  try {
    const cattle = await prisma.cattle.findUnique({
      where: { id: cattleId },
      select: { id: true, farmerId: true, region: true, purpose: true },
    });
    if (!cattle) throw new Error(`Cattle ${cattleId} not found`);

    // ── Check minimum-data threshold ──────────────────────────
    const thresholdStatus = await checkBaselineThreshold(
      cattleId,
      cattle.purpose ?? "dairy"
    );

    if (!thresholdStatus.isMet) {
      // Below threshold: every new log entry recomputes, but stays in "abstain"
      // and skips VetCase creation.
      const entriesLogged = Math.min(MIN_ENTRIES_FOR_BASELINE, thresholdStatus.minEntries);
      const explanationText = `Building health baseline — ${entriesLogged}/${MIN_ENTRIES_FOR_BASELINE} entries logged, needs ~2–3 weeks of data.`;

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
              vetExplanation: `Threshold check pending: Requires at least ${MIN_ENTRIES_FOR_BASELINE} entries across ${MIN_DAYS_FOR_BASELINE} distinct days for all signals. Currently at ${entriesLogged}/${MIN_ENTRIES_FOR_BASELINE}.`,
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
            minEntriesRequired: MIN_ENTRIES_FOR_BASELINE,
          },
        },
      });

      return; // Skip VetCase creation
    }

    // ── Stage 1: Compute baseline (threshold met) ─────────────
    const baseline = await computeBaseline(cattleId);

    // ── Get latest log values across all signals ──────────────
    const [latestWeight, latestFeed, latestActivity, latestMilk, recentScans] =
      await Promise.all([
        prisma.weightLog.findFirst({
          where: { cattleId },
          orderBy: { timestamp: "desc" },
        }),
        prisma.feedLog.findFirst({
          where: { cattleId },
          orderBy: { timestamp: "desc" },
        }),
        prisma.activityLog.findFirst({
          where: { cattleId },
          orderBy: { timestamp: "desc" },
        }),
        cattle.purpose === "dairy"
          ? prisma.milkLog.findFirst({
              where: { cattleId },
              orderBy: { timestamp: "desc" },
            })
          : Promise.resolve(null),
        prisma.scanLog.count({
          where: {
            cattleId,
            timestamp: { gte: new Date(Date.now() - 7 * 86400000) },
          },
        }),
      ]);

    // ── Build normalized deviation vector (z-scores) ──────────
    const wStd = Math.sqrt(baseline.weight.variance) || 1;
    const fStd = Math.sqrt(baseline.feedIntake.variance) || 1;
    const aStd = Math.sqrt(baseline.activity.variance) || 1;

    const deviationVector: DeviationVector = {
      weightDeviation: latestWeight
        ? (latestWeight.value - baseline.weight.expected) / wStd
        : 0,
      feedDeviation: latestFeed
        ? (latestFeed.quantity - baseline.feedIntake.expected) / fStd
        : 0,
      activityDeviation: latestActivity
        ? (latestActivity.value - baseline.activity.expected) / aStd
        : 0,
      scanFrequency: recentScans / 7, // avg scans/day over last week
    };

    if (cattle.purpose === "dairy" && baseline.milkYield) {
      const mStd = Math.sqrt(baseline.milkYield.variance) || 1;
      deviationVector.milkDeviation = latestMilk
        ? (latestMilk.litres - baseline.milkYield.expected) / mStd
        : 0;
    }

    // ── Stage 2: CHDI score ───────────────────────────────────
    const chdiResult = await computeCHDI(deviationVector, cattleId);

    // ── Stage 2b: Explainability ──────────────────────────────
    const explanation = explainScore(deviationVector);

    // ── Persist CHDIEntry ─────────────────────────────────────
    const chdiEntry = await prisma.cHDIEntry.create({
      data: {
        cattleId,
        score: chdiResult.score,
        status: chdiResult.status,
        confidence: chdiResult.confidence,
        topFactors: JSON.parse(JSON.stringify(explanation.topFactors)),
      },
    });

    // ── Audit log ─────────────────────────────────────────────
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

    // ── Auto-create VetCase if watch or at-risk ───────────────
    if (chdiResult.status === "watch" || chdiResult.status === "at-risk") {
      // Check for an existing open case to avoid duplicates
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
                topFactors: explanation.topFactors,
                vetSummary: explanation.vetSummary,
                farmerSummary: explanation.farmerSummary,
              })
            ),
          },
        });

        // Audit the auto-case creation
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

    // ── Regional outbreak detection (async, non-blocking) ─────
    if (cattle.region) {
      checkRegionalOutbreak(cattle.region).catch((err) =>
        console.error("[Outbreak check error]", err)
      );
    }
  } catch (err) {
    console.error(`[CHDI Pipeline Error] cattleId=${cattleId}`, err);
    // Don't rethrow — pipeline failures should not block data logging
  }
}

// ─────────────────────────────────────────────────────────────
// Regional outbreak detection
// ─────────────────────────────────────────────────────────────

const OUTBREAK_ANIMAL_THRESHOLD = 3;   // ≥3 animals
const OUTBREAK_FARM_THRESHOLD = 2;     // across ≥2 farms
const OUTBREAK_WINDOW_HOURS = 48;      // within 48 hours
const OUTBREAK_CHDI_DROP = 20;         // score drop ≥20 points

async function checkRegionalOutbreak(region: string): Promise<void> {
  const since = new Date(Date.now() - OUTBREAK_WINDOW_HOURS * 3600000);

  // Find recent at-risk/watch entries in this region
  const recentEntries = await prisma.cHDIEntry.findMany({
    where: {
      timestamp: { gte: since },
      status: { in: ["at-risk", "watch"] },
      cattle: { region },
    },
    include: { cattle: { select: { farmerId: true } } },
  });

  if (recentEntries.length < OUTBREAK_ANIMAL_THRESHOLD) return;

  const uniqueFarms = new Set(recentEntries.map((e) => e.cattle.farmerId));
  if (uniqueFarms.size < OUTBREAK_FARM_THRESHOLD) return;

  // Avoid duplicate alerts for the same region in the same window
  const existingAlert = await prisma.regionAlert.findFirst({
    where: {
      region,
      triggeredAt: { gte: since },
      status: "active",
    },
  });

  if (existingAlert) return;

  // Create regional alert
  await prisma.regionAlert.create({
    data: {
      region,
      affectedFarmIds: [...uniqueFarms],
      severity:
        recentEntries.filter((e) => e.status === "at-risk").length > 2
          ? "critical"
          : "warning",
      metadata: {
        animalCount: recentEntries.length,
        farmCount: uniqueFarms.size,
        windowHours: OUTBREAK_WINDOW_HOURS,
      },
    },
  });

  console.log(`[Outbreak Alert] Region: ${region}, Animals: ${recentEntries.length}, Farms: ${uniqueFarms.size}`);
}
