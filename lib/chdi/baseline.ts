/**
 * SmartCattle — Stage 1: Baseline Forecasting
 * lib/chdi/baseline.ts
 *
 * Computes per-animal expected trajectories for weight, feed intake, and
 * activity level using a moving-average approach.
 *
 * Design intent:
 * - The function signature `computeBaseline(cattleId)` is kept stable so a
 *   TensorFlow.js LSTM implementation can be swapped in without touching
 *   any calling code.
 * - Fallback: if the animal has fewer than MIN_HISTORY_DAYS of data, we use
 *   the per-breed cluster average as the baseline.
 */

import prisma from "@/lib/prisma";

// ─────────────────────────────────────────────────────────────
// Constants
// ─────────────────────────────────────────────────────────────

const MIN_HISTORY_DAYS = 14; // 2 weeks required for per-animal baseline
const MOVING_AVG_WINDOW = 7; // 7-day rolling window

// ─────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────

export interface SignalBaseline {
  expected: number;
  variance: number;
  sampleCount: number;
  usedFallback: boolean; // true if breed-cluster baseline was used
}

export interface BaselineResult {
  weight: SignalBaseline;
  feedIntake: SignalBaseline;
  activity: SignalBaseline;
  milkYield?: SignalBaseline;
  historyDays: number;
}

// ─────────────────────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────────────────────

function movingAverage(values: number[], window: number): number {
  if (values.length === 0) return 0;
  const slice = values.slice(-window);
  return slice.reduce((a, b) => a + b, 0) / slice.length;
}

function sampleVariance(values: number[], mean: number): number {
  if (values.length < 2) return 1; // default variance if insufficient data
  const squaredDiffs = values.map((v) => Math.pow(v - mean, 2));
  return squaredDiffs.reduce((a, b) => a + b, 0) / (values.length - 1);
}

// ─────────────────────────────────────────────────────────────
// Breed-cluster fallback
// ─────────────────────────────────────────────────────────────

async function getBreedClusterBaseline(
  breed: string,
  signal: "weight" | "feed" | "activity" | "milk"
): Promise<SignalBaseline> {
  // Fetch recent values from all cattle of this breed
  const since = new Date(Date.now() - MIN_HISTORY_DAYS * 86400000);

  if (signal === "weight") {
    const rows = await prisma.weightLog.findMany({
      where: { cattle: { breed }, timestamp: { gte: since } },
      select: { value: true },
    });
    const values = rows.map((r) => r.value);
    const expected = movingAverage(values, values.length);
    return {
      expected,
      variance: sampleVariance(values, expected),
      sampleCount: values.length,
      usedFallback: true,
    };
  }

  if (signal === "feed") {
    const rows = await prisma.feedLog.findMany({
      where: { cattle: { breed }, timestamp: { gte: since } },
      select: { quantity: true },
    });
    const values = rows.map((r) => r.quantity);
    const expected = movingAverage(values, values.length);
    return {
      expected,
      variance: sampleVariance(values, expected),
      sampleCount: values.length,
      usedFallback: true,
    };
  }

  if (signal === "milk") {
    const rows = await prisma.milkLog.findMany({
      where: { cattle: { breed }, timestamp: { gte: since } },
      select: { litres: true },
    });
    const values = rows.map((r) => r.litres);
    const expected = values.length > 0 ? movingAverage(values, values.length) : 12.0;
    return {
      expected,
      variance: sampleVariance(values, expected),
      sampleCount: values.length,
      usedFallback: true,
    };
  }

  // activity
  const rows = await prisma.activityLog.findMany({
    where: { cattle: { breed }, timestamp: { gte: since } },
    select: { value: true },
  });
  const values = rows.map((r) => r.value);
  const expected = movingAverage(values, values.length);
  return {
    expected,
    variance: sampleVariance(values, expected),
    sampleCount: values.length,
    usedFallback: true,
  };
}

// ─────────────────────────────────────────────────────────────
// Main export — stable interface (swap LSTM behind this)
// ─────────────────────────────────────────────────────────────

/**
 * Compute per-animal baseline for weight, feed intake, activity, and milk yield (for dairy).
 * Falls back to breed-cluster averages if the animal has < MIN_HISTORY_DAYS.
 */
export async function computeBaseline(cattleId: string): Promise<BaselineResult> {
  const cattle = await prisma.cattle.findUniqueOrThrow({
    where: { id: cattleId },
    select: { breed: true, purpose: true },
  });

  const oldestCutoff = new Date(Date.now() - MIN_HISTORY_DAYS * 86400000);

  // ── Weight ─────────────────────────────────────────────────
  const weightRows = await prisma.weightLog.findMany({
    where: { cattleId },
    orderBy: { timestamp: "asc" },
    select: { value: true, timestamp: true },
  });

  // ── Feed ───────────────────────────────────────────────────
  const feedRows = await prisma.feedLog.findMany({
    where: { cattleId },
    orderBy: { timestamp: "asc" },
    select: { quantity: true, timestamp: true },
  });

  // ── Activity ───────────────────────────────────────────────
  const activityRows = await prisma.activityLog.findMany({
    where: { cattleId },
    orderBy: { timestamp: "asc" },
    select: { value: true, timestamp: true },
  });

  // ── Milk (Dairy only or if logs exist) ──────────────────────
  const milkRows = await prisma.milkLog.findMany({
    where: { cattleId },
    orderBy: { timestamp: "asc" },
    select: { litres: true, timestamp: true },
  });

  const hasHistory = (rows: { timestamp: Date }[]) =>
    rows.some((r) => r.timestamp <= oldestCutoff);

  const historyDays = Math.max(
    weightRows.length > 0
      ? Math.floor(
          (Date.now() - weightRows[0].timestamp.getTime()) / 86400000
        )
      : 0,
    feedRows.length > 0
      ? Math.floor(
          (Date.now() - feedRows[0].timestamp.getTime()) / 86400000
        )
      : 0,
    milkRows.length > 0
      ? Math.floor(
          (Date.now() - milkRows[0].timestamp.getTime()) / 86400000
        )
      : 0
  );

  // ── Per-animal baselines (or fallback) ─────────────────────
  let weightBaseline: SignalBaseline;
  if (weightRows.length >= 7 && hasHistory(weightRows)) {
    const values = weightRows.map((r) => r.value);
    const expected = movingAverage(values, MOVING_AVG_WINDOW);
    weightBaseline = {
      expected,
      variance: sampleVariance(values, expected),
      sampleCount: values.length,
      usedFallback: false,
    };
  } else {
    weightBaseline = await getBreedClusterBaseline(cattle.breed, "weight");
  }

  let feedBaseline: SignalBaseline;
  if (feedRows.length >= 7 && hasHistory(feedRows)) {
    const values = feedRows.map((r) => r.quantity);
    const expected = movingAverage(values, MOVING_AVG_WINDOW);
    feedBaseline = {
      expected,
      variance: sampleVariance(values, expected),
      sampleCount: values.length,
      usedFallback: false,
    };
  } else {
    feedBaseline = await getBreedClusterBaseline(cattle.breed, "feed");
  }

  let activityBaseline: SignalBaseline;
  if (activityRows.length >= 7 && hasHistory(activityRows)) {
    const values = activityRows.map((r) => r.value);
    const expected = movingAverage(values, MOVING_AVG_WINDOW);
    activityBaseline = {
      expected,
      variance: sampleVariance(values, expected),
      sampleCount: values.length,
      usedFallback: false,
    };
  } else {
    activityBaseline = await getBreedClusterBaseline(cattle.breed, "activity");
  }

  let milkBaseline: SignalBaseline | undefined;
  if (cattle.purpose === "dairy" || milkRows.length > 0) {
    if (milkRows.length >= 7 && hasHistory(milkRows)) {
      const values = milkRows.map((r) => r.litres);
      const expected = movingAverage(values, MOVING_AVG_WINDOW);
      milkBaseline = {
        expected,
        variance: sampleVariance(values, expected),
        sampleCount: values.length,
        usedFallback: false,
      };
    } else {
      milkBaseline = await getBreedClusterBaseline(cattle.breed, "milk");
    }
  }

  return {
    weight: weightBaseline,
    feedIntake: feedBaseline,
    activity: activityBaseline,
    milkYield: milkBaseline,
    historyDays,
  };
}
