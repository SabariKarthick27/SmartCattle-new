/**
 * SmartCattle — Stage 2: Explainability Layer
 * lib/chdi/explain.ts
 *
 * Permutation-importance based explanation of CHDI scores.
 * Ranks which signal contributed most to the deviation from baseline.
 *
 * Two display levels per the spec:
 *  - "farmer": plain-language single top factor
 *  - "vet": full ranked breakdown with contribution percentages
 *
 * This is a SHAP substitute — no external explainability library required.
 */

import type { DeviationVector } from "./anomaly";

// ─────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────

export interface FactorContribution {
  factor: string;
  contribution: number;     // 0–1, relative contribution
  direction: "up" | "down"; // "down" = worse than baseline
  plainLabel: string;        // Human-readable label
  farmerExplanation: string; // Simple, actionable text
  vetExplanation: string;    // Technical description
}

export interface ExplainResult {
  topFactors: FactorContribution[];
  farmerSummary: string;   // Single sentence for farmer
  vetSummary: string;      // Full ranked breakdown text
}

// ─────────────────────────────────────────────────────────────
// Factor metadata
// ─────────────────────────────────────────────────────────────

const FACTOR_META: Record<
  string,
  { label: string; farmerTemplate: (dir: string, pct: number) => string; vetTemplate: (dev: number) => string }
> = {
  weightDeviation: {
    label: "Body Weight",
    farmerTemplate: (dir, pct) =>
      dir === "down"
        ? `Your animal's weight has dropped more than usual (${pct}% impact on the health score).`
        : `Your animal gained weight faster than expected (${pct}% impact on the health score).`,
    vetTemplate: (dev) =>
      `Weight z-score deviation: ${dev.toFixed(3)} σ from 7-day moving average.`,
  },
  feedDeviation: {
    label: "Feed Intake",
    farmerTemplate: (dir, pct) =>
      dir === "down"
        ? `The animal is eating less than normal (${pct}% impact). Check for illness or feed quality issues.`
        : `The animal is eating significantly more than normal (${pct}% impact).`,
    vetTemplate: (dev) =>
      `Feed intake z-score deviation: ${dev.toFixed(3)} σ from rolling baseline.`,
  },
  activityDeviation: {
    label: "Activity Level",
    farmerTemplate: (dir, pct) =>
      dir === "down"
        ? `Activity has dropped significantly (${pct}% impact). The animal may be lethargic.`
        : `Activity is unusually high (${pct}% impact). May indicate agitation or heat.`,
    vetTemplate: (dev) =>
      `Activity z-score deviation: ${dev.toFixed(3)} σ from historical mean.`,
  },
  milkDeviation: {
    label: "Milk Production",
    farmerTemplate: (dir, pct) =>
      dir === "down"
        ? `Daily milk yield dropped noticeably (${pct}% impact). Early warning for mastitis, acidosis, or systemic illness.`
        : `Daily milk yield increased (${pct}% impact on production baseline).`,
    vetTemplate: (dev) =>
      `Milk yield z-score deviation: ${dev.toFixed(3)} σ from rolling baseline (early illness biomarker).`,
  },
  scanFrequency: {
    label: "QR Scan Frequency",
    farmerTemplate: (dir, pct) =>
      dir === "down"
        ? `This animal is being checked less frequently (${pct}% impact). Try to scan daily.`
        : `Unusually frequent scans detected (${pct}% impact). This may indicate concern.`,
    vetTemplate: (dev) =>
      `QR scan frequency deviation: ${dev.toFixed(3)} σ from expected rate.`,
  },
};

// ─────────────────────────────────────────────────────────────
// Permutation importance (stable interface — SHAP substitute)
// ─────────────────────────────────────────────────────────────

/**
 * Rank each signal's contribution to the CHDI deviation score.
 *
 * Method: permutation importance via leave-one-out analysis.
 * For each signal, compute how much the Euclidean distance drops when
 * that signal is zeroed out (permuted to baseline). Larger drop = more important.
 *
 * @param deviationVector  Normalized z-score deviations per signal
 * @returns ExplainResult with ranked factors, farmer summary, and vet summary
 */
export function explainScore(deviationVector: DeviationVector): ExplainResult {
  const signals: { key: keyof DeviationVector; value: number }[] = [
    { key: "weightDeviation", value: deviationVector.weightDeviation },
    { key: "feedDeviation", value: deviationVector.feedDeviation },
    { key: "activityDeviation", value: deviationVector.activityDeviation },
  ];

  if (deviationVector.milkDeviation !== undefined) {
    // Weight factor for milk yield explanation in dairy
    signals.push({ key: "milkDeviation", value: deviationVector.milkDeviation * 1.35 });
  }

  if (deviationVector.scanFrequency !== undefined) {
    signals.push({ key: "scanFrequency", value: deviationVector.scanFrequency });
  }

  // Baseline Euclidean distance (all signals present)
  const baselineDistance = Math.sqrt(
    signals.reduce((acc, s) => acc + s.value * s.value, 0)
  );

  // Permutation: zero out each signal and measure distance reduction
  const contributions = signals.map((s) => {
    const withoutThisSignal = signals.filter((x) => x.key !== s.key);
    const distWithout = Math.sqrt(
      withoutThisSignal.reduce((acc, x) => acc + x.value * x.value, 0)
    );
    const marginalContribution = Math.max(
      0,
      baselineDistance - distWithout
    );
    return {
      key: s.key,
      value: s.value,
      marginalContribution,
    };
  });

  // Normalize contributions to sum to 1
  const totalContribution = contributions.reduce(
    (a, c) => a + c.marginalContribution,
    0
  ) || 1;

  const ranked = contributions
    .map((c) => {
      const meta = FACTOR_META[c.key as string];
      const relativePct = Math.round((c.marginalContribution / totalContribution) * 100);
      const direction: "up" | "down" = c.value < 0 ? "down" : "up";

      return {
        factor: c.key as string,
        contribution: c.marginalContribution / totalContribution,
        direction,
        plainLabel: meta?.label ?? c.key,
        farmerExplanation:
          meta?.farmerTemplate(direction, relativePct) ??
          `${c.key} is ${direction === "down" ? "below" : "above"} normal (${relativePct}% of score).`,
        vetExplanation:
          meta?.vetTemplate(c.value) ?? `${c.key}: deviation = ${c.value.toFixed(3)}`,
      } satisfies FactorContribution;
    })
    .sort((a, b) => b.contribution - a.contribution);

  // ── Farmer summary (top factor only) ──────────────────────
  const top = ranked[0];
  const farmerSummary =
    top?.farmerExplanation ??
    "Your animal's health indicators are within normal range.";

  // ── Vet summary (full breakdown) ───────────────────────────
  const vetSummary = ranked
    .map(
      (f, i) =>
        `${i + 1}. ${f.plainLabel} (${Math.round(f.contribution * 100)}%): ${f.vetExplanation}`
    )
    .join("\n");

  return {
    topFactors: ranked,
    farmerSummary,
    vetSummary,
  };
}
