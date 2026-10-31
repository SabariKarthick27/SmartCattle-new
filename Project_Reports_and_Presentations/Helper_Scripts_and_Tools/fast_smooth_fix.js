const { PrismaClient } = require('@prisma/client');
const p = new PrismaClient();

async function runFast() {
  console.log('Fast batch replace...');
  const cow = await p.cattle.findFirst({ where: { tagId: 'TN-SC-1042' } });
  if (!cow) return;

  await p.milkLog.deleteMany({ where: { cattleId: cow.id } });
  await p.feedLog.deleteMany({ where: { cattleId: cow.id } });
  await p.weightLog.deleteMany({ where: { cattleId: cow.id } });
  await p.temperatureLog.deleteMany({ where: { cattleId: cow.id } });

  const kamaDaily = [
    { day: 14, feed: 16.4, milk: 21.8, weight: 446.2, temp: 38.5 },
    { day: 13, feed: 16.8, milk: 22.4, weight: 446.5, temp: 38.6 },
    { day: 12, feed: 16.1, milk: 21.5, weight: 446.0, temp: 38.4 },
    { day: 11, feed: 17.0, milk: 22.8, weight: 447.1, temp: 38.5 },
    { day: 10, feed: 16.5, milk: 22.0, weight: 446.8, temp: 38.6 },
    { day: 9,  feed: 16.2, milk: 21.6, weight: 446.4, temp: 38.5 },
    { day: 8,  feed: 16.7, milk: 22.2, weight: 447.0, temp: 38.6 },
    { day: 7,  feed: 16.0, milk: 21.2, weight: 446.1, temp: 38.7 },
    { day: 6,  feed: 15.1, milk: 19.8, weight: 445.2, temp: 38.9 },
    { day: 5,  feed: 13.8, milk: 17.6, weight: 443.8, temp: 39.3 },
    { day: 4,  feed: 12.2, milk: 15.1, weight: 441.5, temp: 39.7 },
    { day: 3,  feed: 10.4, milk: 12.4, weight: 439.0, temp: 40.0 },
    { day: 2,  feed: 8.5,  milk: 9.6,  weight: 436.5, temp: 40.2 },
    { day: 1,  feed: 6.8,  milk: 7.4,  weight: 434.0, temp: 40.3 },
  ];

  const base = new Date();
  base.setHours(7, 30, 0, 0);

  const milkBatch = [];
  const feedBatch = [];
  const weightBatch = [];
  const tempBatch = [];

  for (const item of kamaDaily) {
    const timestamp = new Date(base.getTime() - item.day * 86400000);
    milkBatch.push({ cattleId: cow.id, litres: item.milk, timestamp, source: 'manual' });
    feedBatch.push({ cattleId: cow.id, quantity: item.feed, feedType: 'Concentrate', timestamp, source: 'manual' });
    weightBatch.push({ cattleId: cow.id, value: item.weight, timestamp, source: 'manual' });
    tempBatch.push({ cattleId: cow.id, value: item.temp, timestamp, source: 'manual' });
  }

  await p.milkLog.createMany({ data: milkBatch });
  await p.feedLog.createMany({ data: feedBatch });
  await p.weightLog.createMany({ data: weightBatch });
  await p.temperatureLog.createMany({ data: tempBatch });

  console.log('✅ Kamadhenu (TN-SC-1042) now has a smooth, natural gradual decline!');
  process.exit(0);
}

runFast().catch(e => { console.error(e); process.exit(1); });

