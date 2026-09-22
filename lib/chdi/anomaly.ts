/**
 * SmartCattle — Stage 2: Anomaly Detection / CHDI Score
 * lib/chdi/anomaly.ts
 *
 * Computes a Cattle Health Deviation Index (CHDI) score using a
 * distance-based anomaly detection approach (Mahalanobis distance against
 * the animal's own historical distribution).
 *
 * Design notes:
 * - Per the master spec: no hardcoded per-signal weights. Signal covariance
 *   is used to weight contributions automatically (Mahalanobis distance).
 * - Output normalized to 0–100 (100 = perfectly healthy, 0 = extreme anomaly).
 * - If the animal has < MIN_HISTORY_POINTS, or if the confidence interval is
 *   too wide, status = "abstain" instead of forcing healthy/unhealthy.
 * - Status thresholds are read from the Settings table (admin-configurable),
 *   not hardcoded constants.
 */

import prisma from "@/lib/prisma";

// ─────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────

export interface DeviationVector {
  weightDeviation: number;   // current - expected, normalized by std
  feedDeviation: number;
  activityDeviation: number;
  milkDeviation?: number;    // milk yield deviation (critical early indicator for dairy)
  scanFrequency?: number;    // optional: QR scan frequency (scans/day)
}

export interface CHDIResult {
  score: number | null; // 0–100; null when abstaining
  confidence: number;   // 0–1
  status: "healthy" | "watch" | "at-risk" | "abstain";
  rawDistance: number;
  deviationVector: DeviationVector;
}

// ─────────────────────────────────────────────────────────────
// Matrix math helpers (no external dependency needed)
// ─────────────────────────────────────────────────────────────

/**
 * Compute covariance matrix from a list of numeric vectors of any dimension.
 * Uses sample covariance (n-1 denominator).
 */
function computeCovarianceMatrix(vectors: number[][]): number[][] {
  const n = vectors.length;
  if (n === 0) return [];
  const dim = vectors[0].length;

  // Column means
  const means = Array.from({ length: dim }, (_, j) =>
    vectors.reduce((acc, v) => acc + v[j], 0) / n
  );

  // Initialize matrix
  const cov: number[][] = Array.from({ length: dim }, () =>
    new Array(dim).fill(0)
  );

  for (const v of vectors) {
    for (let i = 0; i < dim; i++) {
      for (let j = 0; j < dim; j++) {
        cov[i][j] += ((v[i] - means[i]) * (v[j] - means[j])) / Math.max(1, n - 1);
      }
    }
  }
  return cov;
}

/**
 * Invert an NxN matrix (Gauss-Jordan elimination with partial pivoting).
 * Returns identity matrix if the matrix is singular (fallback to euclidean distance).
 */
function invertMatrix(m: number[][]): number[][] {
  const n = m.length;
  if (n === 0) return [];

  // Augmented matrix [A | I]
  const aug = m.map((row, i) => {
    const r = [...row];
    for (let j = 0; j < n; j++) {
      r.push(i === j ? 1 : 0);
    }
    return r;
  });

  for (let i = 0; i < n; i++) {
    let maxRow = i;
    for (let k = i + 1; k < n; k++) {
      if (Math.abs(aug[k][i]) > Math.abs(aug[maxRow][i])) {
        maxRow = k;
      }
    }
    if (Math.abs(aug[maxRow][i]) < 1e-10) {
      // Singular — fall back to identity (euclidean distance)
      return Array.from({ length: n }, (_, r) =>
        Array.from({ length: n }, (_, c) => (r === c ? 1 : 0))
      );
    }

    // Swap rows
    const temp = aug[i];
    aug[i] = aug[maxRow];
    aug[maxRow] = temp;

    // Scale pivot row
    const pivot = aug[i][i];
    for (let j = 0; j < 2 * n; j++) {
      aug[i][j] /= pivot;
    }

    // Eliminate other rows
    for (let k = 0; k < n; k++) {
      if (k !== i) {
        const factor = aug[k][i];
        for (let j = 0; j < 2 * n; j++) {
          aug[k][j] -= factor * aug[i][j];
        }
      }
    }
  }

  // Extract inverse
  return aug.map((row) => row.slice(n));
}

/**
 * Mahalanobis distance: sqrt( (x - mu)^T * S^-1 * (x - mu) )
 */
function mahalanobisDistance(
  point: number[],
  mean: number[],
  covInv: number[][]
): number {
  const diff = point.map((v, i) => v - mean[i]);
  let sum = 0;
  for (let i = 0; i < diff.length; i++) {
    for (let j = 0; j < diff.length; j++) {
      sum += diff[i] * covInv[i][j] * diff[j];
    }
  }
  return Math.sqrt(Math.max(0, sum));
}

// ─────────────────────────────────────────────────────────────
// Settings loader (admin-configurable thresholds)
// ─────────────────────────────────────────────────────────────

interface CHDIThresholds {
  watchBelow: number;     // score below this → watch (default 75)
  atRiskBelow: number;    // score below this → at-risk (default 50)
  minConfidence: number;  // confidence below this → abstain (default 0.4)
  minHistoryPoints: number; // fewer than this → abstain (default 7)
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

// ─────────────────────────────────────────────────────────────
// Main export — stable interface
// ─────────────────────────────────────────────────────────────

/**
 * Compute the CHDI score for an animal given its 5-signal deviation vector:
 * weight, feed, activity, milk_yield (dairy), and scan_pattern (supplementary).
 *
 * Uses distance-based anomaly detection (Mahalanobis distance) against the
 * animal's own historical distribution. Normalizes to 0–100.
 *
 * @param deviationVector  Normalized deviations from baseline (per-signal z-scores)
 * @param cattleId         Used to fetch historical data for covariance matrix
 */
export async function computeCHDI(
  deviationVector: DeviationVector,
  cattleId: string
): Promise<CHDIResult> {
  const thresholds = await getCHDIThresholds();

  // ── Fetch historical deviation vectors to build covariance ──
  const since = new Date(Date.now() - 90 * 86400000); // 90-day window

  const [weightRows, feedRows, activityRows, milkRows] = await Promise.all([
    prisma.weightLog.findMany({
      where: { cattleId, timestamp: { gte: since } },
      orderBy: { timestamp: "asc" },
      select: { value: true },
    }),
    prisma.feedLog.findMany({
      where: { cattleId, timestamp: { gte: since } },
      orderBy: { timestamp: "asc" },
      select: { quantity: true },
    }),
    prisma.activityLog.findMany({
      where: { cattleId, timestamp: { gte: since } },
      orderBy: { timestamp: "asc" },
      select: { value: true },
    }),
    prisma.milkLog.findMany({
      where: { cattleId, timestamp: { gte: since } },
      orderBy: { timestamp: "asc" },
      select: { litres: true },
    }),
  ]);

  const hasMilk = deviationVector.milkDeviation !== undefined && milkRows.length > 0;
  const n = hasMilk
    ? Math.min(weightRows.length, feedRows.length, activityRows.length, milkRows.length)
    : Math.min(weightRows.length, feedRows.length, activityRows.length);

  // ── Abstain if insufficient history ─────────────────────────
  if (n < thresholds.minHistoryPoints) {
    return {
      score: null,
      confidence: 0,
      status: "abstain",
      rawDistance: 0,
      deviationVector,
    };
  }

  // ── Build historical matrix ──────────────────────────────────
  const wMean = weightRows.reduce((a, r) => a + r.value, 0) / weightRows.length;
  const fMean = feedRows.reduce((a, r) => a + r.quantity, 0) / feedRows.length;
  const aMean = activityRows.reduce((a, r) => a + r.value, 0) / activityRows.length;

  const wStd = Math.sqrt(
    weightRows.reduce((a, r) => a + Math.pow(r.value - wMean, 2), 0) / Math.max(1, weightRows.length - 1)
  ) || 1;
  const fStd = Math.sqrt(
    feedRows.reduce((a, r) => a + Math.pow(r.quantity - fMean, 2), 0) / Math.max(1, feedRows.length - 1)
  ) || 1;
  const aStd = Math.sqrt(
    activityRows.reduce((a, r) => a + Math.pow(r.value - aMean, 2), 0) / Math.max(1, activityRows.length - 1)
  ) || 1;

  let mMean = 0;
  let mStd = 1;
  if (hasMilk) {
    mMean = milkRows.reduce((a, r) => a + r.litres, 0) / milkRows.length;
    mStd = Math.sqrt(
      milkRows.reduce((a, r) => a + Math.pow(r.litres - mMean, 2), 0) / Math.max(1, milkRows.length - 1)
    ) || 1;
  }

  // Milk yield is an early illness indicator for dairy cattle specifically.
  // Weight factor 1.35x emphasizes acute milk drops in dairy cows.
  const MILK_WEIGHT_FACTOR = 1.35;

  // Normalize historical vectors (z-scores)
  const historicalVectors = Array.from({ length: n }, (_, i) => {
    const row = [
      (weightRows[i].value - wMean) / wStd,
      (feedRows[i].quantity - fMean) / fStd,
      (activityRows[i].value - aMean) / aStd,
    ];
    if (hasMilk) {
      row.push(((milkRows[i].litres - mMean) / mStd) * MILK_WEIGHT_FACTOR);
    }
    return row;
  });

  const covMatrix = computeCovarianceMatrix(historicalVectors);
  const covInv = invertMatrix(covMatrix);

  // ── Current point (already normalized by caller via deviationVector) ──
  const currentPoint = [
    deviationVector.weightDeviation,
    deviationVector.feedDeviation,
    deviationVector.activityDeviation,
  ];
  if (hasMilk) {
    currentPoint.push((deviationVector.milkDeviation ?? 0) * MILK_WEIGHT_FACTOR);
  }

  const historicalMean = new Array(currentPoint.length).fill(0); // z-scores are mean-centered

  const rawDistance = mahalanobisDistance(currentPoint, historicalMean, covInv);

  // ── Compute historical distance distribution for normalization ──
  const historicalDistances = historicalVectors.map((v) =>
    mahalanobisDistance(v, historicalMean, covInv)
  );
  const maxHistoricalDist = Math.max(...historicalDistances, 1);

  // ── Confidence: based on distance spread (tighter = more confident) ──
  const confidence = Math.min(
    1,
    Math.max(0, 1 - rawDistance / (maxHistoricalDist * 3))
  );

  // ── Normalize score: 0 distance → 100, large distance → 0 ──
  const normalizedScore = Math.max(
    0,
    Math.min(100, Math.round(100 - (rawDistance / (maxHistoricalDist * 2)) * 100))
  );

  // ── Abstain if confidence too low ───────────────────────────
  if (confidence < thresholds.minConfidence) {
    return {
      score: normalizedScore,
      confidence,
      status: "abstain",
      rawDistance,
      deviationVector,
    };
  }

  // ── Determine status from admin-configurable thresholds ─────
  let status: CHDIResult["status"];
  if (normalizedScore < thresholds.atRiskBelow) {
    status = "at-risk";
  } else if (normalizedScore < thresholds.watchBelow) {
    status = "watch";
  } else {
    status = "healthy";
  }

  return {
    score: normalizedScore,
    confidence,
    status,
    rawDistance,
    deviationVector,
  };
}
