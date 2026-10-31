/**
 * SmartCattle — Academic Experiment: Sparse vs. Rich Data Accuracy Comparison
 * scripts/experiment.ts (run with ts-node or compiled)
 *
 * This is the primary evaluation experiment for the IEEE paper.
 * 
 * Compares CHDI Stage 2 accuracy under two conditions:
 *   - Sparse:  manual-entry-only logs (typical smallholder farmer)
 *   - Rich:    sensor-augmented logs (IoT-equipped farm)
 *
 * Methodology:
 * 1. Simulate two cohorts of N animals each
 * 2. For each animal, generate synthetic health events (health dips)
 * 3. Log data under "manual" and "sensor" source types
 * 4. Run computeCHDI() for each condition
 * 5. Compare: abstention rate, detection rate, false alert rate
 * 6. Output CSV report
 */

import { writeFileSync } from "fs";
import { computeCHDI } from "../lib/chdi/anomaly";
import prisma from "../lib/prisma";

// ─────────────────────────────────────────────────────────────
// Experiment parameters
// ─────────────────────────────────────────────────────────────

const N_ANIMALS = 20;           // Animals per cohort
const HISTORY_DAYS = 30;        // Days of history to simulate
const HEALTH_DIP_DAYS = [20, 25, 28]; // Days where health dips occur
const SENSOR_READINGS_PER_DAY = 4;    // Rich condition: 4 readings/day
const MANUAL_READINGS_PER_DAY = 1;    // Sparse condition: 1 reading/day

// ─────────────────────────────────────────────────────────────
// Simulation helpers
// ─────────────────────────────────────────────────────────────

function generateWeight(day: number, isHealthy: boolean, base = 350): number {
  const trend = !isHealthy ? -0.8 : 0.1; // dip if unhealthy
  const noise = (Math.random() - 0.5) * 4;
  return base + day * trend + noise;
}

function generateFeed(day: number, isHealthy: boolean, base = 12): number {
  const dip = !isHealthy ? -2.5 : 0;
  const noise = (Math.random() - 0.5) * 1;
  return Math.max(0, base + dip + noise);
}

function generateActivity(day: number, isHealthy: boolean, base = 65): number {
  const dip = !isHealthy ? -20 : 0;
  const noise = (Math.random() - 0.5) * 8;
  return Math.max(0, Math.min(100, base + dip + noise));
}

// ─────────────────────────────────────────────────────────────
// Core experiment
// ─────────────────────────────────────────────────────────────

interface AnimalResult {
  animalId: string;
  condition: "sparse" | "rich";
  trueStatus: "healthy" | "at-risk";
  predictedStatus: string;
  chdiScore: number;
  confidence: number;
  detectionDelay: number | null; // Days from dip to detection
}

async function runExperiment(): Promise<void> {
  console.log("🔬 SmartCattle — Sparse vs. Rich Data Experiment");
  console.log("=".repeat(50));
  console.log(`Animals per cohort: ${N_ANIMALS}`);
  console.log(`History days: ${HISTORY_DAYS}`);
  console.log(`Health dip days: ${HEALTH_DIP_DAYS.join(", ")}`);
  console.log();

  const results: AnimalResult[] = [];

  // Find or create a test farmer
  let testFarmer = await prisma.user.findFirst({ where: { email: "experiment@test.sc" } });
  if (!testFarmer) {
    testFarmer = await prisma.user.create({
      data: {
        name: "Experiment Bot",
        phone: "+00-0000000000",
        email: "experiment@test.sc",
        passwordHash: "not-used",
        role: "farmer",
        isVerified: true,
      },
    });
  }

  for (const condition of ["sparse", "rich"] as const) {
    const readingsPerDay = condition === "sparse" ? MANUAL_READINGS_PER_DAY : SENSOR_READINGS_PER_DAY;
    const source = condition === "sparse" ? "manual" : "sensor";

    console.log(`\n--- ${condition.toUpperCase()} CONDITION (${readingsPerDay} reading(s)/day, source=${source}) ---`);

    for (let i = 0; i < N_ANIMALS; i++) {
      const isHealthDipAnimal = i < N_ANIMALS / 2; // 50% have health dips
      const trueStatus = isHealthDipAnimal ? "at-risk" : "healthy";
      const tagId = `EXP-${condition.toUpperCase()}-${String(i).padStart(3, "0")}`;

      // Create cattle
      const cattle = await prisma.cattle.create({
        data: {
          farmerId: testFarmer.id,
          tagId: `${tagId}-${Date.now()}`,
          qrToken: `exp-${tagId}-${Date.now()}`,
          breed: "Holstein Friesian",
          dob: new Date(Date.now() - 3 * 365 * 86400000),
        },
      });

      // Log historical data
      const now = Date.now();
      for (let day = 0; day < HISTORY_DAYS; day++) {
        const isHealthy = !(isHealthDipAnimal && HEALTH_DIP_DAYS.includes(day));
        const dayTs = new Date(now - (HISTORY_DAYS - day) * 86400000);

        for (let r = 0; r < readingsPerDay; r++) {
          const readingTs = new Date(dayTs.getTime() + r * (86400000 / readingsPerDay));

          await prisma.weightLog.create({
            data: { cattleId: cattle.id, value: generateWeight(day, isHealthy), timestamp: readingTs, source },
          });
          await prisma.feedLog.create({
            data: { cattleId: cattle.id, quantity: generateFeed(day, isHealthy), feedType: "grass", timestamp: readingTs, source },
          });
          await prisma.activityLog.create({
            data: { cattleId: cattle.id, value: generateActivity(day, isHealthy), timestamp: readingTs, source },
          });
        }
      }

      // Compute baseline and CHDI
      try {
        const latestWeight = await prisma.weightLog.findFirst({ where: { cattleId: cattle.id }, orderBy: { timestamp: "desc" } });
        const latestFeed = await prisma.feedLog.findFirst({ where: { cattleId: cattle.id }, orderBy: { timestamp: "desc" } });
        const latestActivity = await prisma.activityLog.findFirst({ where: { cattleId: cattle.id }, orderBy: { timestamp: "desc" } });

        const deviationVector = {
          weightDeviation: latestWeight ? (latestWeight.value - 350) / 15 : 0,
          feedDeviation: latestFeed ? (latestFeed.quantity - 12) / 1.5 : 0,
          activityDeviation: latestActivity ? (latestActivity.value - 65) / 8 : 0,
        };

        const chdi = await computeCHDI(deviationVector, cattle.id);

        results.push({
          animalId: cattle.id,
          condition,
          trueStatus,
          predictedStatus: chdi.status,
          chdiScore: chdi.score ?? 0,
          confidence: chdi.confidence,
          detectionDelay: null,
        });

        console.log(`  Animal ${String(i + 1).padStart(2)} | True: ${trueStatus.padEnd(8)} | CHDI: ${chdi.status.padEnd(8)} | Score: ${Math.round(chdi.score ?? 0).toString().padStart(3)} | Conf: ${(chdi.confidence * 100).toFixed(0)}%`);
      } catch (e) {
        console.error(`  Animal ${i + 1}: Error — ${(e as Error).message}`);
      }

      // Cleanup
      await prisma.cattle.update({ where: { id: cattle.id }, data: { isActive: false } });
    }
  }

  // ── Compute metrics ───────────────────────────────────────
  console.log("\n" + "=".repeat(50));
  console.log("📊 RESULTS SUMMARY");
  console.log("=".repeat(50));

  for (const condition of ["sparse", "rich"] as const) {
    const condResults = results.filter((r) => r.condition === condition);
    const atRiskAnimals = condResults.filter((r) => r.trueStatus === "at-risk");
    const healthyAnimals = condResults.filter((r) => r.trueStatus === "healthy");

    const truePositives = atRiskAnimals.filter((r) => r.predictedStatus === "at-risk" || r.predictedStatus === "watch").length;
    const falseNegatives = atRiskAnimals.filter((r) => r.predictedStatus === "healthy").length;
    const falsePositives = healthyAnimals.filter((r) => r.predictedStatus === "at-risk" || r.predictedStatus === "watch").length;
    const abstentions = condResults.filter((r) => r.predictedStatus === "abstain").length;

    const detectionRate = atRiskAnimals.length > 0 ? truePositives / atRiskAnimals.length : 0;
    const falseAlertRate = healthyAnimals.length > 0 ? falsePositives / healthyAnimals.length : 0;
    const abstentionRate = condResults.length > 0 ? abstentions / condResults.length : 0;

    console.log(`\n${condition.toUpperCase()}:`);
    console.log(`  Detection rate:    ${(detectionRate * 100).toFixed(1)}%`);
    console.log(`  False alert rate:  ${(falseAlertRate * 100).toFixed(1)}%`);
    console.log(`  Abstention rate:   ${(abstentionRate * 100).toFixed(1)}%`);
    console.log(`  True Positives:    ${truePositives}`);
    console.log(`  False Negatives:   ${falseNegatives}`);
    console.log(`  Abstentions:       ${abstentions}`);
  }

  // ── Export CSV ────────────────────────────────────────────
  const csvHeader = "animalId,condition,trueStatus,predictedStatus,chdiScore,confidence\n";
  const csvRows = results
    .map((r) => `${r.animalId},${r.condition},${r.trueStatus},${r.predictedStatus},${r.chdiScore.toFixed(2)},${r.confidence.toFixed(3)}`)
    .join("\n");

  const csvPath = "./scripts/experiment-results.csv";
  writeFileSync(csvPath, csvHeader + csvRows);
  console.log(`\n✅ Results exported to ${csvPath}`);

  await prisma.$disconnect();
}

runExperiment().catch(console.error);
