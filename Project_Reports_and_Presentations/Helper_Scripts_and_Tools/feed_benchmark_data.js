const path = require('path');
const fs = require('fs');

// Load environment variables from .env / .env.local
for (const envFile of ['.env.local', '.env']) {
  const p = path.resolve(__dirname, '..', envFile);
  if (fs.existsSync(p)) {
    const lines = fs.readFileSync(p, 'utf8').split('\n');
    for (const line of lines) {
      const match = line.match(/^\s*([\w.-]+)\s*=\s*["']?([^"'\r\n]+)["']?\s*$/);
      if (match && !process.env[match[1]]) {
        process.env[match[1]] = match[2];
      }
    }
  }
}

const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function feedBenchmarkData() {
  console.log('🚀 Starting Benchmark Dataset Feed...');

  try {
    const cattleList = await prisma.cattle.findMany({
      where: {
        tagId: { in: ['TN-SC-3608', 'TEST-REG-7851'] }
      }
    });

    if (cattleList.length === 0) {
      console.log('❌ Target cattle not found.');
      return;
    }

    const primaryVet = await prisma.user.findFirst({
      where: { role: 'vet' }
    });

    for (const cow of cattleList) {
      console.log(`\n📌 Seeding 14-day longitudinal data for Cow ${cow.tagId} (${cow.name})...`);

      // 14 days of realistic synchronized baseline data
      // Baseline averages: Milk ~ 18.5 L, Feed ~ 15.0 kg, Weight ~ 430 kg, Temp ~ 38.6 C
      const baseDate = new Date();
      baseDate.setHours(8, 0, 0, 0);

      const logsToCreate = [];

      for (let day = 14; day >= 1; day--) {
        const logDate = new Date(baseDate.getTime() - day * 24 * 60 * 60 * 1000);
        
        // Add subtle daily biological variance
        const milk = +(18.0 + Math.sin(day) * 1.2 + (day < 3 ? -1.0 : 0.4)).toFixed(1);
        const feed = +(15.0 + Math.cos(day) * 0.8).toFixed(1);
        const weight = +(430 + (14 - day) * 0.2 + (Math.random() - 0.5) * 2).toFixed(1);
        const temp = +(38.5 + (Math.sin(day * 2) * 0.2)).toFixed(1);

        logsToCreate.push({ date: logDate, milk, feed, weight, temp });
      }

      // Insert milk logs
      for (const item of logsToCreate) {
        await prisma.milkLog.create({
          data: {
            cattleId: cow.id,
            litres: item.milk,
            timestamp: item.date,
            source: 'manual'
          }
        });

        await prisma.feedLog.create({
          data: {
            cattleId: cow.id,
            quantity: item.feed,
            feedType: 'Concentrate & Dry Fodder',
            timestamp: item.date,
            source: 'manual'
          }
        });

        await prisma.weightLog.create({
          data: {
            cattleId: cow.id,
            value: item.weight,
            timestamp: item.date,
            source: 'manual'
          }
        });

        await prisma.temperatureLog.create({
          data: {
            cattleId: cow.id,
            value: item.temp,
            timestamp: item.date,
            source: 'manual'
          }
        });
      }

      console.log(`✅ Inserted 14 daily multi-signal logs (Milk, Feed, Weight, Temp)`);

      // Create an active Healthy CHDI score
      const latestChdi = await prisma.cHDIEntry.create({
        data: {
          cattleId: cow.id,
          score: 84.5,
          status: 'healthy',
          confidence: 0.92,
          timestamp: new Date(),
          topFactors: [
            {
              factor: 'Daily Milk Yield',
              label: 'Daily Milk Yield',
              contribution_percentage: 42.1,
              direction: 'stable',
              z_score: 0.18,
              farmer_summary: 'Milk production is stable and consistent with 14-day baseline.',
              vet_summary: 'Milk yield z-score = +0.18 sigma. Within expected physiological variance.'
            },
            {
              factor: 'Feed Intake',
              label: 'Feed Intake',
              contribution_percentage: 31.4,
              direction: 'stable',
              z_score: 0.24,
              farmer_summary: 'Dry matter and concentrate intake within normal limits.',
              vet_summary: 'Feed consumption z-score = +0.24 sigma. Nutritional intake optimal.'
            },
            {
              factor: 'Core Body Temperature',
              label: 'Core Body Temperature',
              contribution_percentage: 26.5,
              direction: 'stable',
              z_score: -0.12,
              farmer_summary: 'Core body temperature normal.',
              vet_summary: 'Body temperature z-score = -0.12 sigma. No pyrexia indicated.'
            }
          ]
        }
      });

      console.log(`✅ Generated active CHDI score: 84.5 (Healthy) with LOCO explainability`);
    }

    // Now populate 12 verified VetFeedback samples to train the Random Forest Classifier
    console.log('\n📌 Populating verified clinical vet feedback samples for ML Retraining...');

    const sampleOutcomes = [
      { status: 'healthy', score: 88, milkDev: 0.1, feedDev: 0.2, tempDev: 0.0, weightDev: 0.1, outcome: 'healthy' },
      { status: 'healthy', score: 85, milkDev: -0.2, feedDev: 0.1, tempDev: 0.1, weightDev: 0.0, outcome: 'healthy' },
      { status: 'healthy', score: 82, milkDev: -0.3, feedDev: -0.2, tempDev: 0.2, weightDev: 0.1, outcome: 'healthy' },
      { status: 'healthy', score: 86, milkDev: 0.2, feedDev: 0.3, tempDev: -0.1, weightDev: 0.2, outcome: 'healthy' },
      { status: 'watch', score: 68, milkDev: -1.2, feedDev: -0.8, tempDev: 0.6, weightDev: -0.4, outcome: 'watch_mild_mastitis' },
      { status: 'watch', score: 64, milkDev: -1.4, feedDev: -1.1, tempDev: 0.8, weightDev: -0.5, outcome: 'watch_mild_mastitis' },
      { status: 'watch', score: 71, milkDev: -0.9, feedDev: -1.2, tempDev: 0.3, weightDev: -0.3, outcome: 'watch_indigestion' },
      { status: 'watch', score: 62, milkDev: -1.5, feedDev: -1.0, tempDev: 0.7, weightDev: -0.6, outcome: 'watch_mild_mastitis' },
      { status: 'at-risk', score: 44, milkDev: -2.4, feedDev: -2.1, tempDev: 1.8, weightDev: -1.2, outcome: 'clinical_mastitis' },
      { status: 'at-risk', score: 38, milkDev: -2.8, feedDev: -2.5, tempDev: 2.1, weightDev: -1.5, outcome: 'clinical_mastitis' },
      { status: 'at-risk', score: 41, milkDev: -2.2, feedDev: -2.7, tempDev: 1.2, weightDev: -1.8, outcome: 'subclinical_ketosis' },
      { status: 'at-risk', score: 35, milkDev: -3.0, feedDev: -2.8, tempDev: 2.4, weightDev: -2.0, outcome: 'clinical_mastitis' },
    ];

    const targetCow = cattleList[0];
    const vetId = primaryVet ? primaryVet.id : 'cmu9nsh3x0006gv1d753er3e8';

    for (let i = 0; i < sampleOutcomes.length; i++) {
      const s = sampleOutcomes[i];
      
      // Create a closed vet case for feedback
      const vCase = await prisma.vetCase.create({
        data: {
          cattleId: targetCow.id,
          farmerId: targetCow.farmerId,
          vetId: vetId,
          status: 'resolved',
          urgency: s.status === 'at-risk' ? 'high' : s.status === 'watch' ? 'medium' : 'low',
          symptoms: `Observed departure in production. CHDI Score: ${s.score}`,
          diagnosis: s.outcome.replace(/_/g, ' ').toUpperCase(),
          treatment: 'Administered supportive electrolytes and verified clinical progress.',
          resolvedAt: new Date(Date.now() - (12 - i) * 86400000),
          chdiSnapshot: {
            score: s.score,
            status: s.status,
            confidence: 0.88,
            deviations: {
              milkDeviation: s.milkDev,
              feedDeviation: s.feedDev,
              temperatureDeviation: s.tempDev,
              weightDeviation: s.weightDev,
              activityDeviation: 0.0,
              ruminationDeviation: 0.0
            }
          }
        }
      });

      await prisma.vetFeedback.create({
        data: {
          cattleId: targetCow.id,
          vetId: vetId,
          caseId: vCase.id,
          predictedStatus: s.status,
          confirmedOutcome: s.outcome
        }
      });
    }

    console.log(`✅ Seeded 12 verified clinical VetFeedback training cases.`);

    console.log('\n🎉 SUCCESS! Benchmark dataset successfully fed into your live database.');
  } catch (error) {
    console.error('❌ Error feeding benchmark data:', error);
  } finally {
    await prisma.$disconnect();
  }
}

feedBenchmarkData();

