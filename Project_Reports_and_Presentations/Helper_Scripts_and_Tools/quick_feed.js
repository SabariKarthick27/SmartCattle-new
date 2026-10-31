const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function run() {
  console.log('Inserting batch benchmark logs...');
  const cow = await prisma.cattle.findFirst({ where: { tagId: 'TN-SC-3608' } });
  if (!cow) {
    console.error('Cow TN-SC-3608 not found');
    process.exit(1);
  }

  const base = new Date();
  base.setHours(8, 0, 0, 0);

  const milkData = [];
  const feedData = [];
  const weightData = [];
  const tempData = [];

  for (let d = 14; d >= 1; d--) {
    const timestamp = new Date(base.getTime() - d * 86400000);
    const milk = +(18.0 + Math.sin(d) * 1.2).toFixed(1);
    const feed = +(15.0 + Math.cos(d) * 0.8).toFixed(1);
    const weight = +(425 + (14 - d) * 0.3).toFixed(1);
    const temp = +(38.5 + (Math.sin(d * 2) * 0.2)).toFixed(1);

    milkData.push({ cattleId: cow.id, litres: milk, timestamp, source: 'manual' });
    feedData.push({ cattleId: cow.id, quantity: feed, feedType: 'Concentrate', timestamp, source: 'manual' });
    weightData.push({ cattleId: cow.id, value: weight, timestamp, source: 'manual' });
    tempData.push({ cattleId: cow.id, value: temp, timestamp, source: 'manual' });
  }

  await prisma.milkLog.createMany({ data: milkData });
  await prisma.feedLog.createMany({ data: feedData });
  await prisma.weightLog.createMany({ data: weightData });
  await prisma.temperatureLog.createMany({ data: tempData });

  console.log('✅ Created 14 daily multi-signal records for Cow TN-SC-3608');

  // Create an active Healthy CHDI score
  await prisma.cHDIEntry.create({
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
          farmer_summary: 'Feed consumption within normal limits.',
          vet_summary: 'Feed consumption z-score = +0.24 sigma. Nutritional intake optimal.'
        },
        {
          factor: 'Core Body Temperature',
          label: 'Core Body Temperature',
          contribution_percentage: 26.5,
          direction: 'stable',
          z_score: -0.12,
          farmer_summary: 'Core body temperature normal.',
          vet_summary: 'Body temperature z-score = -0.12 sigma. No fever indicated.'
        }
      ]
    }
  });

  console.log('✅ Created active CHDI score: 84.5 (Healthy) with LOCO factors');

  // Now seed VetFeedback for training
  const primaryVet = await prisma.user.findFirst({ where: { role: 'vet' } });
  const vetId = primaryVet ? primaryVet.id : 'cmu9nsh3x0006gv1d753er3e8';

  const samples = [
    { status: 'healthy', score: 88, outcome: 'healthy' },
    { status: 'healthy', score: 85, outcome: 'healthy' },
    { status: 'healthy', score: 82, outcome: 'healthy' },
    { status: 'healthy', score: 86, outcome: 'healthy' },
    { status: 'watch', score: 68, outcome: 'watch_mild_mastitis' },
    { status: 'watch', score: 64, outcome: 'watch_mild_mastitis' },
    { status: 'watch', score: 71, outcome: 'watch_indigestion' },
    { status: 'watch', score: 62, outcome: 'watch_mild_mastitis' },
    { status: 'at-risk', score: 44, outcome: 'clinical_mastitis' },
    { status: 'at-risk', score: 38, outcome: 'clinical_mastitis' },
    { status: 'at-risk', score: 41, outcome: 'subclinical_ketosis' },
    { status: 'at-risk', score: 35, outcome: 'clinical_mastitis' },
  ];

  for (let i = 0; i < samples.length; i++) {
    const s = samples[i];
    const vCase = await prisma.vetCase.create({
      data: {
        cattleId: cow.id,
        farmerId: cow.farmerId,
        vetId: vetId,
        status: 'resolved',
        urgency: s.status === 'at-risk' ? 'high' : s.status === 'watch' ? 'medium' : 'low',
        symptoms: `Observed health deviation. CHDI Score: ${s.score}`,
        diagnosis: s.outcome.replace(/_/g, ' ').toUpperCase(),
        treatment: 'Supportive electrolyte therapy and daily monitoring.',
        resolvedAt: new Date(Date.now() - (12 - i) * 86400000),
        chdiSnapshot: {
          score: s.score,
          status: s.status,
          confidence: 0.88,
          deviations: {
            milkDeviation: s.status === 'at-risk' ? -2.5 : s.status === 'watch' ? -1.2 : 0.1,
            feedDeviation: s.status === 'at-risk' ? -2.2 : s.status === 'watch' ? -1.0 : 0.2,
            temperatureDeviation: s.status === 'at-risk' ? 1.8 : s.status === 'watch' ? 0.6 : 0.0,
            weightDeviation: s.status === 'at-risk' ? -1.5 : s.status === 'watch' ? -0.5 : 0.1
          }
        }
      }
    });

    await prisma.vetFeedback.create({
      data: {
        cattleId: cow.id,
        vetId: vetId,
        caseId: vCase.id,
        predictedStatus: s.status,
        confirmedOutcome: s.outcome
      }
    });
  }

  console.log('✅ Created 12 verified VetFeedback cases for ML training');
  process.exit(0);
}

run().catch(e => { console.error(e); process.exit(1); });

