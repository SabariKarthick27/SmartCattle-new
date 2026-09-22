/**
 * SmartCattle — Stage 3: Vet-Feedback Classifier
 * lib/chdi/feedback-classifier.ts
 *
 * Once VetFeedback accumulates enough labeled rows, trains an ml-random-forest
 * model on (feature vector → confirmedOutcome).
 *
 * Initially stubbed — wires to real training once data exists.
 * Precision/recall/F1 are tracked and exposed on the admin dashboard.
 */

import prisma from "@/lib/prisma";

// ─────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────

export interface ClassifierMetrics {
  precision: number;
  recall: number;
  f1Score: number;
  accuracy: number;
  sampleCount: number;
  trainedAt: Date | null;
}

export interface ClassifierResult {
  predictedOutcome: string;
  confidence: number;
}

// Minimum number of VetFeedback rows before real training runs
const MIN_FEEDBACK_ROWS = 30;

// Label encoding for outcomes
const OUTCOME_LABELS = ["healthy", "recovered", "diagnosed", "hospitalized", "deceased"];

// ─────────────────────────────────────────────────────────────
// Feature extraction
// ─────────────────────────────────────────────────────────────

/**
 * Convert a CHDI snapshot + feedback row into a numeric feature vector.
 * Must stay consistent between training and inference.
 */
function extractFeatures(chdiSnapshot: Record<string, unknown>): number[] {
  return [
    typeof chdiSnapshot.score === "number" ? chdiSnapshot.score : 50,
    typeof chdiSnapshot.confidence === "number" ? chdiSnapshot.confidence : 0,
    typeof chdiSnapshot.weightDeviation === "number" ? chdiSnapshot.weightDeviation : 0,
    typeof chdiSnapshot.feedDeviation === "number" ? chdiSnapshot.feedDeviation : 0,
    typeof chdiSnapshot.activityDeviation === "number" ? chdiSnapshot.activityDeviation : 0,
  ];
}

// ─────────────────────────────────────────────────────────────
// Classifier state (in-memory, reset on cold start)
// ─────────────────────────────────────────────────────────────

// eslint-disable-next-line @typescript-eslint/no-explicit-any
let trainedModel: any = null;
let lastMetrics: ClassifierMetrics = {
  precision: 0,
  recall: 0,
  f1Score: 0,
  accuracy: 0,
  sampleCount: 0,
  trainedAt: null,
};

// ─────────────────────────────────────────────────────────────
// Training job
// ─────────────────────────────────────────────────────────────

/**
 * Retrain the Stage 3 classifier using all available VetFeedback rows.
 * Stubbed if fewer than MIN_FEEDBACK_ROWS are present.
 *
 * This function is callable as a manual trigger from the admin dashboard
 * or as a scheduled cron job.
 */
export async function retrainClassifier(): Promise<ClassifierMetrics> {
  const feedbackRows = await prisma.vetFeedback.findMany({
    include: { case: true },
  });

  if (feedbackRows.length < MIN_FEEDBACK_ROWS) {
    console.log(
      `[Stage 3] Insufficient data (${feedbackRows.length}/${MIN_FEEDBACK_ROWS}). Skipping real training.`
    );
    return lastMetrics;
  }

  // Dynamic import to avoid SSR issues with ml-random-forest
  const { RandomForestClassifier } = await import("ml-random-forest");

  // Build training data
  const features: number[][] = [];
  const labels: number[] = [];

  for (const row of feedbackRows) {
    const snapshot = row.case.chdiSnapshot as Record<string, unknown>;
    const feature = extractFeatures(snapshot);
    const labelIdx = OUTCOME_LABELS.indexOf(row.confirmedOutcome);
    if (labelIdx === -1) continue; // Skip unknown labels
    features.push(feature);
    labels.push(labelIdx);
  }

  if (features.length < MIN_FEEDBACK_ROWS) {
    return lastMetrics;
  }

  // Train / test split (80/20)
  const splitIdx = Math.floor(features.length * 0.8);
  const trainX = features.slice(0, splitIdx);
  const trainY = labels.slice(0, splitIdx);
  const testX = features.slice(splitIdx);
  const testY = labels.slice(splitIdx);

  const classifier = new RandomForestClassifier({ nEstimators: 50 });
  classifier.train(trainX, trainY);
  trainedModel = classifier;

  // ── Evaluate on test set ──────────────────────────────────
  const predictions: number[] = testX.map((x: number[]) => classifier.predict([x])[0]);

  let correct = 0;
  const tp: Record<number, number> = {};
  const fp: Record<number, number> = {};
  const fn: Record<number, number> = {};

  for (let i = 0; i < testY.length; i++) {
    if (predictions[i] === testY[i]) correct++;
    tp[testY[i]] = (tp[testY[i]] ?? 0) + (predictions[i] === testY[i] ? 1 : 0);
    fp[predictions[i]] = (fp[predictions[i]] ?? 0) + (predictions[i] !== testY[i] ? 1 : 0);
    fn[testY[i]] = (fn[testY[i]] ?? 0) + (predictions[i] !== testY[i] ? 1 : 0);
  }

  const uniqueLabels = [...new Set(testY)];
  const macroP =
    uniqueLabels.reduce((a, l) => {
      const p = tp[l] ?? 0;
      const denom = (p + (fp[l] ?? 0)) || 1;
      return a + p / denom;
    }, 0) / uniqueLabels.length;

  const macroR =
    uniqueLabels.reduce((a, l) => {
      const p = tp[l] ?? 0;
      const denom = (p + (fn[l] ?? 0)) || 1;
      return a + p / denom;
    }, 0) / uniqueLabels.length;

  const f1 = macroP + macroR > 0 ? (2 * macroP * macroR) / (macroP + macroR) : 0;
  const accuracy = testY.length > 0 ? correct / testY.length : 0;

  lastMetrics = {
    precision: macroP,
    recall: macroR,
    f1Score: f1,
    accuracy,
    sampleCount: features.length,
    trainedAt: new Date(),
  };

  // Persist version to DB
  await prisma.modelVersion.create({
    data: {
      stage: 3,
      version: new Date().toISOString(),
      precision: macroP,
      recall: macroR,
      f1Score: f1,
      isActive: true,
      metadata: { sampleCount: features.length, testSize: testY.length },
    },
  });

  // Deactivate previous versions
  await prisma.modelVersion.updateMany({
    where: { stage: 3, trainedAt: { lt: lastMetrics.trainedAt! } },
    data: { isActive: false },
  });

  console.log(
    `[Stage 3] Retrained. P=${macroP.toFixed(3)} R=${macroR.toFixed(3)} F1=${f1.toFixed(3)}`
  );
  return lastMetrics;
}

// ─────────────────────────────────────────────────────────────
// Inference
// ─────────────────────────────────────────────────────────────

/**
 * Predict the likely outcome for a given CHDI snapshot.
 * Returns null if the classifier has not been trained yet.
 */
export function classifyOutcome(
  chdiSnapshot: Record<string, unknown>
): ClassifierResult | null {
  if (!trainedModel) return null;

  const feature = extractFeatures(chdiSnapshot);
  const prediction = trainedModel.predict([feature])[0];
  const label = OUTCOME_LABELS[prediction] ?? "unknown";

  // Estimate confidence from vote distribution (if available)
  const confidence = 0.7; // placeholder; replace with oob_score when available

  return { predictedOutcome: label, confidence };
}

/**
 * Get the latest classifier performance metrics.
 */
export function getClassifierMetrics(): ClassifierMetrics {
  return lastMetrics;
}
