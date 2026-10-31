/**
 * SmartCattle — Stage 2: CHDI Machine Learning Client
 * lib/chdi/anomaly.ts
 *
 * Dispatches cattle health scoring requests directly to the dedicated
 * Python FastAPI Machine Learning Microservice (port 8000), which executes:
 *   - Stage 1: Rolling Baseline (NumPy)
 *   - Stage 2: Regularized Mahalanobis Distance & CHDI Normalization (SciPy)
 *   - Stage 3: LOCO Feature Attribution (Scikit-learn)
 */

import prisma from "@/lib/prisma";

export interface DeviationVector {
  weightDeviation: number;
  feedDeviation: number;
  activityDeviation?: number;
  milkDeviation?: number;
  temperatureDeviation?: number;
  ruminationDeviation?: number;
  scanFrequency?: number;
}

export interface FactorAttribution {
  factor: string;
  label: string;
  contribution_percentage: number;
  direction: string;
  z_score: number;
  farmer_summary: string;
  vet_summary: string;
}

export interface CHDIResult {
  score: number | null; // 0–100; null when abstaining
  confidence: number;   // 0–1
  status: "healthy" | "watch" | "at-risk" | "abstain";
  rawDistance: number;
  deviationVector: DeviationVector;
  topFactors?: FactorAttribution[];
  farmerText?: string;
  vetText?: string;
}

interface CHDIThresholds {
  watchBelow: number;
  atRiskBelow: number;
  minConfidence: number;
  minHistoryPoints: number;
}

async function getCHDIThresholds(): Promise<CHDIThresholds> {
  const settings = await prisma.settings.findMany({
    where: {
      key: {
        in: [
          "chdi_watch_below",
          "chdi_at_risk_below",
          "chdi_min_confidence",
          "chdi_min_history_points",
        ],
      },
    },
  });

  const get = (key: string, def: number) =>
    parseFloat(settings.find((s) => s.key === key)?.value ?? String(def));

  return {
    watchBelow: get("chdi_watch_below", 75),
    atRiskBelow: get("chdi_at_risk_below", 50),
    minConfidence: get("chdi_min_confidence", 0.4),
    minHistoryPoints: get("chdi_min_history_points", 7),
  };
}

/**
 * Compute CHDI via the dedicated Python FastAPI Machine Learning Microservice.
 */
export async function computeCHDI(
  deviationVector: DeviationVector,
  cattleId: string
): Promise<CHDIResult> {
  const thresholds = await getCHDIThresholds();
  const since = new Date(Date.now() - 90 * 86400000); // 90-day window

  // Fetch all historical signal logs from PostgreSQL
  const [weightRows, feedRows, activityRows, milkRows, tempRows, rumRows] = await Promise.all([
    prisma.weightLog.findMany({
      where: { cattleId, timestamp: { gte: since } },
      orderBy: { timestamp: "asc" },
      select: { value: true, timestamp: true },
    }),
    prisma.feedLog.findMany({
      where: { cattleId, timestamp: { gte: since } },
      orderBy: { timestamp: "asc" },
      select: { quantity: true, timestamp: true },
    }),
    prisma.activityLog.findMany({
      where: { cattleId, timestamp: { gte: since } },
      orderBy: { timestamp: "asc" },
      select: { value: true, timestamp: true },
    }),
    prisma.milkLog.findMany({
      where: { cattleId, timestamp: { gte: since } },
      orderBy: { timestamp: "asc" },
      select: { litres: true, timestamp: true },
    }),
    (prisma as any).temperatureLog?.findMany({
      where: { cattleId, timestamp: { gte: since } },
      orderBy: { timestamp: "asc" },
      select: { value: true, timestamp: true },
    }) || Promise.resolve([]),
    (prisma as any).ruminationLog?.findMany({
      where: { cattleId, timestamp: { gte: since } },
      orderBy: { timestamp: "asc" },
      select: { minutes: true, timestamp: true },
    }) || Promise.resolve([]),
  ]);

  const historicalPayload = [];
  const maxLen = Math.max(
    weightRows.length,
    feedRows.length,
    activityRows.length,
    milkRows.length,
    tempRows.length,
    rumRows.length
  );

  for (let i = 0; i < maxLen; i++) {
    historicalPayload.push({
      timestamp: (weightRows[i]?.timestamp || new Date()).toISOString(),
      milk: milkRows[i]?.litres ?? null,
      rumination: rumRows[i]?.minutes ?? null,
      temperature: tempRows[i]?.value ?? null,
      activity: activityRows[i]?.value ?? null,
      feed: feedRows[i]?.quantity ?? null,
      weight: weightRows[i]?.value ?? null,
    });
  }

  const pyRes = await fetch("http://127.0.0.1:8000/api/v1/chdi/compute", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      cattle_id: cattleId,
      current_observation: {
        milk: deviationVector.milkDeviation !== undefined ? 25.0 + deviationVector.milkDeviation * 3.0 : null,
        rumination: deviationVector.ruminationDeviation !== undefined ? 500.0 + deviationVector.ruminationDeviation * 40.0 : null,
        activity: deviationVector.activityDeviation !== undefined ? 65.0 + deviationVector.activityDeviation * 8.0 : null,
        feed: 12.0 + deviationVector.feedDeviation * 1.5,
        weight: 350.0 + deviationVector.weightDeviation * 15.0,
      },
      historical_observations: historicalPayload,
      min_confidence: thresholds.minConfidence,
      min_history_days: thresholds.minHistoryPoints,
      watch_below: thresholds.watchBelow,
      at_risk_below: thresholds.atRiskBelow,
    }),
  });

  if (!pyRes.ok) {
    throw new Error(`Python ML microservice error: ${pyRes.statusText}`);
  }

  const pyData = await pyRes.json();

  return {
    score: pyData.score,
    confidence: pyData.confidence,
    status: pyData.status,
    rawDistance: pyData.raw_distance,
    deviationVector,
    topFactors: pyData.top_factors,
    farmerText: pyData.farmer_text,
    vetText: pyData.vet_text,
  };
}
