const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function populateAllStatuses() {
  console.log('Setting up full spectrum status demo for Farmer...');

  // Cow 2: Ganga (TN-SC-4717) -> Set as WATCH / NEEDS ATTENTION (Score ~64)
  const cowWatch = await prisma.cattle.findFirst({ where: { tagId: 'TN-SC-4717' } });
  
  // Cow 3: Kamadhenu (TN-SC-1042) -> Set as AT-RISK / CRITICAL SICK (Score ~38)
  const cowAtRisk = await prisma.cattle.findFirst({ where: { tagId: 'TN-SC-1042' } });

  const base = new Date();
  base.setHours(8, 0, 0, 0);

  // 1. Seed logs for Ganga (Watch: mild milk & feed drop in last 3 days)
  if (cowWatch) {
    console.log('Seeding Watch case for Ganga (TN-SC-4717)...');
    const milkData = [];
    const feedData = [];
    const weightData = [];
    const tempData = [];

    for (let d = 14; d >= 1; d--) {
      const timestamp = new Date(base.getTime() - d * 86400000);
      // Last 3 days: drop from 16 L to 12.5 L, feed drop from 14 kg to 11 kg
      const isDropping = d <= 3;
      const milk = +(isDropping ? 12.5 + Math.random() * 0.5 : 16.0 + Math.random() * 0.8).toFixed(1);
      const feed = +(isDropping ? 11.0 + Math.random() * 0.4 : 14.5 + Math.random() * 0.6).toFixed(1);
      const weight = +(410 - (isDropping ? 3 : 0) + Math.random()).toFixed(1);
      const temp = +(isDropping ? 39.2 : 38.6).toFixed(1);

      milkData.push({ cattleId: cowWatch.id, litres: milk, timestamp, source: 'manual' });
      feedData.push({ cattleId: cowWatch.id, quantity: feed, feedType: 'Concentrate', timestamp, source: 'manual' });
      weightData.push({ cattleId: cowWatch.id, value: weight, timestamp, source: 'manual' });
      tempData.push({ cattleId: cowWatch.id, value: temp, timestamp, source: 'manual' });
    }

    await prisma.milkLog.createMany({ data: milkData });
    await prisma.feedLog.createMany({ data: feedData });
    await prisma.weightLog.createMany({ data: weightData });
    await prisma.temperatureLog.createMany({ data: tempData });

    await prisma.cHDIEntry.create({
      data: {
        cattleId: cowWatch.id,
        score: 64.2,
        status: 'watch',
        confidence: 0.89,
        timestamp: new Date(),
        topFactors: [
          {
            factor: 'Daily Milk Yield',
            label: 'Daily Milk Yield',
            contribution_percentage: 55.4,
            direction: 'down',
            z_score: -1.48,
            farmer_summary: 'Warning: 22% drop in milk yield compared to 14-day baseline.',
            vet_summary: 'Sub-acute milk yield reduction z = -1.48 sigma. Early mastitis suspect.'
          },
          {
            factor: 'Feed Intake',
            label: 'Feed Intake',
            contribution_percentage: 28.1,
            direction: 'down',
            z_score: -1.12,
            farmer_summary: 'Feed intake reduced by 3.5 kg over last 48 hours.',
            vet_summary: 'Anorexia departure z = -1.12 sigma.'
          },
          {
            factor: 'Core Body Temperature',
            label: 'Core Body Temperature',
            contribution_percentage: 16.5,
            direction: 'up',
            z_score: 1.05,
            farmer_summary: 'Mild body temperature elevation (39.2 °C).',
            vet_summary: 'Low-grade pyrexia departure z = +1.05 sigma.'
          }
        ]
      }
    });

    // Create an open VetCase for Ganga
    await prisma.vetCase.create({
      data: {
        cattleId: cowWatch.id,
        farmerId: cowWatch.farmerId,
        status: 'open',
        urgency: 'medium',
        symptoms: 'Mild milk reduction (12.5 L) and warm rear udder quarter.',
        diagnosis: 'Suspected Early Subclinical Mastitis',
        treatment: 'Scheduled for veterinary CMT (California Mastitis Test) checkup.',
        chdiSnapshot: {
          score: 64.2,
          status: 'watch',
          confidence: 0.89,
          topFactors: ['Daily Milk Yield (-1.48 sigma)', 'Feed Intake (-1.12 sigma)']
        }
      }
    });

    console.log('✅ Created WATCH status (64.2) & Open Vet Case for Ganga');
  }

  // 2. Seed logs for Kamadhenu (At-Risk: severe drop to 7 L, fever 40.1 C)
  if (cowAtRisk) {
    console.log('Seeding At-Risk case for Kamadhenu (TN-SC-1042)...');
    const milkData = [];
    const feedData = [];
    const weightData = [];
    const tempData = [];

    for (let d = 14; d >= 1; d--) {
      const timestamp = new Date(base.getTime() - d * 86400000);
      const isSevere = d <= 2;
      const milk = +(isSevere ? 7.2 : 21.0 - (14 - d) * 0.2).toFixed(1);
      const feed = +(isSevere ? 6.5 : 16.0).toFixed(1);
      const weight = +(445 - (isSevere ? 12 : 0)).toFixed(1);
      const temp = +(isSevere ? 40.2 : 38.6).toFixed(1);

      milkData.push({ cattleId: cowAtRisk.id, litres: milk, timestamp, source: 'manual' });
      feedData.push({ cattleId: cowAtRisk.id, quantity: feed, feedType: 'Concentrate', timestamp, source: 'manual' });
      weightData.push({ cattleId: cowAtRisk.id, value: weight, timestamp, source: 'manual' });
      tempData.push({ cattleId: cowAtRisk.id, value: temp, timestamp, source: 'manual' });
    }

    await prisma.milkLog.createMany({ data: milkData });
    await prisma.feedLog.createMany({ data: feedData });
    await prisma.weightLog.createMany({ data: weightData });
    await prisma.temperatureLog.createMany({ data: tempData });

    await prisma.cHDIEntry.create({
      data: {
        cattleId: cowAtRisk.id,
        score: 38.0,
        status: 'at-risk',
        confidence: 0.94,
        timestamp: new Date(),
        topFactors: [
          {
            factor: 'Daily Milk Yield',
            label: 'Daily Milk Yield',
            contribution_percentage: 52.8,
            direction: 'down',
            z_score: -2.85,
            farmer_summary: 'CRITICAL: Acute 65% drop in milk yield. Immediate vet attention needed.',
            vet_summary: 'Severe milk drop departure z = -2.85 sigma. Acute clinical mastitis.'
          },
          {
            factor: 'Core Body Temperature',
            label: 'Core Body Temperature',
            contribution_percentage: 29.4,
            direction: 'up',
            z_score: 2.45,
            farmer_summary: 'High fever detected (40.2 °C).',
            vet_summary: 'High pyrexia departure z = +2.45 sigma.'
          },
          {
            factor: 'Feed Intake',
            label: 'Feed Intake',
            contribution_percentage: 17.8,
            direction: 'down',
            z_score: -2.10,
            farmer_summary: 'Severe loss of appetite.',
            vet_summary: 'Severe anorexia z = -2.10 sigma.'
          }
        ]
      }
    });

    // Create an urgent VetCase for Kamadhenu
    await prisma.vetCase.create({
      data: {
        cattleId: cowAtRisk.id,
        farmerId: cowAtRisk.farmerId,
        status: 'open',
        urgency: 'critical',
        symptoms: 'High fever 40.2 C, severe milk drop to 7.2 L, swollen left quarter.',
        diagnosis: 'Acute Clinical Mastitis with High Pyrexia',
        treatment: 'Urgent veterinary attention required. Administer anti-inflammatory & antibiotic therapy.',
        chdiSnapshot: {
          score: 38.0,
          status: 'at-risk',
          confidence: 0.94,
          topFactors: ['Daily Milk Yield (-2.85 sigma)', 'Core Body Temperature (+2.45 sigma)']
        }
      }
    });

    console.log('✅ Created AT-RISK status (38.0) & Critical Vet Case for Kamadhenu');
  }

  console.log('\n🎉 DONE! All 3 cows now have distinct, realistic statuses:');
  console.log('1. Lakshmi   (TN-SC-3608) -> HEALTHY (Score: 84.5)');
  console.log('2. Ganga     (TN-SC-4717) -> WATCH   (Score: 64.2)');
  console.log('3. Kamadhenu (TN-SC-1042) -> AT-RISK (Score: 38.0)');
  process.exit(0);
}

populateAllStatuses().catch(e => { console.error(e); process.exit(1); });

