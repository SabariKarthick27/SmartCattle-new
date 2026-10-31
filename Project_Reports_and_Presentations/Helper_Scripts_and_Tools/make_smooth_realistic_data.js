const { PrismaClient } = require('@prisma/client');
const p = new PrismaClient();

async function makeSmoothRealisticData() {
  console.log('Generating organic daily biological curves with smooth transitions...');

  // 1. Ganga (TN-SC-4717) - Watch Status (Gradual incubation drop over 5 days)
  const cowWatch = await p.cattle.findFirst({ where: { tagId: 'TN-SC-4717' } });
  if (cowWatch) {
    await p.milkLog.deleteMany({ where: { cattleId: cowWatch.id } });
    await p.feedLog.deleteMany({ where: { cattleId: cowWatch.id } });
    await p.weightLog.deleteMany({ where: { cattleId: cowWatch.id } });
    await p.temperatureLog.deleteMany({ where: { cattleId: cowWatch.id } });

    // Realistic curve: Normal (16.2 to 15.5 kg) -> Gentle gradual decline starting 5 days ago:
    // 15.8 -> 15.2 -> 14.6 -> 13.7 -> 12.8 -> 12.1 -> 11.4 kg
    const gangaDaily = [
      // Day 14 (16 Oct) to Day 6 (24 Oct) - Healthy organic fluctuation around ~15.5-16.2 kg feed, ~16-17 L milk
      { day: 14, feed: 15.8, milk: 16.4, weight: 412.5, temp: 38.5 },
      { day: 13, feed: 16.1, milk: 16.8, weight: 412.8, temp: 38.6 },
      { day: 12, feed: 15.6, milk: 16.2, weight: 413.0, temp: 38.4 },
      { day: 11, feed: 16.3, milk: 17.1, weight: 413.5, temp: 38.5 },
      { day: 10, feed: 15.9, milk: 16.5, weight: 413.2, temp: 38.6 },
      { day: 9,  feed: 15.7, milk: 16.3, weight: 413.0, temp: 38.5 },
      { day: 8,  feed: 16.0, milk: 16.6, weight: 413.4, temp: 38.6 },
      { day: 7,  feed: 15.4, milk: 16.0, weight: 412.9, temp: 38.7 },
      // Day 6 to Day 1 (25 Oct - 29 Oct) - Realistic smooth progressive decline
      { day: 6,  feed: 14.8, milk: 15.3, weight: 412.5, temp: 38.8 },
      { day: 5,  feed: 14.2, milk: 14.7, weight: 411.8, temp: 38.9 },
      { day: 4,  feed: 13.5, milk: 14.1, weight: 411.2, temp: 39.0 },
      { day: 3,  feed: 12.8, milk: 13.4, weight: 410.5, temp: 39.1 },
      { day: 2,  feed: 12.1, milk: 12.8, weight: 409.8, temp: 39.2 },
      { day: 1,  feed: 11.4, milk: 12.3, weight: 409.0, temp: 39.3 },
    ];

    const base = new Date();
    base.setHours(7, 30, 0, 0);

    for (const item of gangaDaily) {
      const timestamp = new Date(base.getTime() - item.day * 86400000);
      await p.milkLog.create({ data: { cattleId: cowWatch.id, litres: item.milk, timestamp, source: 'manual' } });
      await p.feedLog.create({ data: { cattleId: cowWatch.id, quantity: item.feed, feedType: 'Concentrate', timestamp, source: 'manual' } });
      await p.weightLog.create({ data: { cattleId: cowWatch.id, value: item.weight, timestamp, source: 'manual' } });
      await p.temperatureLog.create({ data: { cattleId: cowWatch.id, value: item.temp, timestamp, source: 'manual' } });
    }
    console.log('✅ Ganga (Watch) updated with natural smooth 5-day disease curve!');
  }

  // 2. Kamadhenu (TN-SC-1042) - At-Risk Status (Natural acute mastitis curve over 6 days)
  const cowAtRisk = await p.cattle.findFirst({ where: { tagId: 'TN-SC-1042' } });
  if (cowAtRisk) {
    await p.milkLog.deleteMany({ where: { cattleId: cowAtRisk.id } });
    await p.feedLog.deleteMany({ where: { cattleId: cowAtRisk.id } });
    await p.weightLog.deleteMany({ where: { cattleId: cowAtRisk.id } });
    await p.temperatureLog.deleteMany({ where: { cattleId: cowAtRisk.id } });

    // Healthy baseline (16-17 kg feed, 21-23 L milk) with realistic daily micro-variations
    // Followed by clinical disease curve: 16.2 -> 15.1 -> 13.6 -> 11.2 -> 8.7 -> 6.8 kg
    const kamaDaily = [
      { day: 14, feed: 16.4, milk: 21.8, weight: 446.2, temp: 38.5 },
      { day: 13, feed: 16.8, milk: 22.4, weight: 446.5, temp: 38.6 },
      { day: 12, feed: 16.1, milk: 21.5, weight: 446.0, temp: 38.4 },
      { day: 11, feed: 17.0, milk: 22.8, weight: 447.1, temp: 38.5 },
      { day: 10, feed: 16.5, milk: 22.0, weight: 446.8, temp: 38.6 },
      { day: 9,  feed: 16.2, milk: 21.6, weight: 446.4, temp: 38.5 },
      { day: 8,  feed: 16.7, milk: 22.2, weight: 447.0, temp: 38.6 },
      { day: 7,  feed: 16.0, milk: 21.2, weight: 446.1, temp: 38.7 },
      // Disease onset: Mastitis incubation to acute fever
      { day: 6,  feed: 15.1, milk: 19.8, weight: 445.2, temp: 38.9 },
      { day: 5,  feed: 13.8, milk: 17.6, weight: 443.8, temp: 39.3 },
      { day: 4,  feed: 12.2, milk: 15.1, weight: 441.5, temp: 39.7 },
      { day: 3,  feed: 10.4, milk: 12.4, weight: 439.0, temp: 40.0 },
      { day: 2,  feed: 8.5,  milk: 9.6,  weight: 436.5, temp: 40.2 },
      { day: 1,  feed: 6.8,  milk: 7.4,  weight: 434.0, temp: 40.3 },
    ];

    const base = new Date();
    base.setHours(7, 30, 0, 0);

    for (const item of kamaDaily) {
      const timestamp = new Date(base.getTime() - item.day * 86400000);
      await p.milkLog.create({ data: { cattleId: cowAtRisk.id, litres: item.milk, timestamp, source: 'manual' } });
      await p.feedLog.create({ data: { cattleId: cowAtRisk.id, quantity: item.feed, feedType: 'Concentrate', timestamp, source: 'manual' } });
      await p.weightLog.create({ data: { cattleId: cowAtRisk.id, value: item.weight, timestamp, source: 'manual' } });
      await p.temperatureLog.create({ data: { cattleId: cowAtRisk.id, value: item.temp, timestamp, source: 'manual' } });
    }
    console.log('✅ Kamadhenu (At-Risk) updated with clinical progressive mastitis curve!');
  }

  // 3. Lakshmi (TN-SC-3608) - Healthy Status (Natural biological day-to-day fluctuations)
  const cowHealthy = await p.cattle.findFirst({ where: { tagId: 'TN-SC-3608' } });
  if (cowHealthy) {
    await p.milkLog.deleteMany({ where: { cattleId: cowHealthy.id } });
    await p.feedLog.deleteMany({ where: { cattleId: cowHealthy.id } });
    await p.weightLog.deleteMany({ where: { cattleId: cowHealthy.id } });
    await p.temperatureLog.deleteMany({ where: { cattleId: cowHealthy.id } });

    const lakshmiDaily = [
      { day: 14, feed: 15.2, milk: 18.2, weight: 428.0, temp: 38.5 },
      { day: 13, feed: 15.6, milk: 18.7, weight: 428.4, temp: 38.6 },
      { day: 12, feed: 14.9, milk: 17.8, weight: 428.1, temp: 38.4 },
      { day: 11, feed: 15.8, milk: 19.1, weight: 428.9, temp: 38.5 },
      { day: 10, feed: 15.3, milk: 18.4, weight: 428.6, temp: 38.6 },
      { day: 9,  feed: 15.0, milk: 18.0, weight: 428.2, temp: 38.5 },
      { day: 8,  feed: 15.7, milk: 18.9, weight: 429.0, temp: 38.6 },
      { day: 7,  feed: 15.1, milk: 18.1, weight: 428.7, temp: 38.5 },
      { day: 6,  feed: 15.5, milk: 18.6, weight: 429.2, temp: 38.6 },
      { day: 5,  feed: 14.8, milk: 17.9, weight: 428.8, temp: 38.4 },
      { day: 4,  feed: 15.6, milk: 18.8, weight: 429.4, temp: 38.5 },
      { day: 3,  feed: 15.4, milk: 18.5, weight: 429.1, temp: 38.6 },
      { day: 2,  feed: 15.2, milk: 18.3, weight: 429.0, temp: 38.5 },
      { day: 1,  feed: 15.5, milk: 18.7, weight: 429.3, temp: 38.6 },
    ];

    const base = new Date();
    base.setHours(7, 30, 0, 0);

    for (const item of lakshmiDaily) {
      const timestamp = new Date(base.getTime() - item.day * 86400000);
      await p.milkLog.create({ data: { cattleId: cowHealthy.id, litres: item.milk, timestamp, source: 'manual' } });
      await p.feedLog.create({ data: { cattleId: cowHealthy.id, quantity: item.feed, feedType: 'Concentrate', timestamp, source: 'manual' } });
      await p.weightLog.create({ data: { cattleId: cowHealthy.id, value: item.weight, timestamp, source: 'manual' } });
      await p.temperatureLog.create({ data: { cattleId: cowHealthy.id, value: item.temp, timestamp, source: 'manual' } });
    }
    console.log('✅ Lakshmi (Healthy) updated with natural daily biological variations!');
  }

  console.log('\n🎉 ALL DONE! Tables and graphs now show realistic, progressive changes.');
  process.exit(0);
}

makeSmoothRealisticData().catch(e => { console.error(e); process.exit(1); });

