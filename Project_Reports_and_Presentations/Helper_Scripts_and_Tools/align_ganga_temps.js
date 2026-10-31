const { PrismaClient } = require('@prisma/client');
const p = new PrismaClient();

async function alignGangaWatchTemps() {
  console.log('Aligning Ganga temperatures to match her 24-29 Oct Watch status...');
  const cow = await p.cattle.findFirst({ where: { tagId: 'TN-SC-4717' } });
  if (!cow) return;

  await p.temperatureLog.deleteMany({ where: { cattleId: cow.id } });

  // 14 days matching 16 Oct to 29 Oct
  // Healthy days (16-24 Oct): 38.4 to 38.7 C
  // Watch subclinical days (25-29 Oct): 38.8 -> 38.9 -> 39.0 -> 39.1 -> 39.2 C
  const gangaTemps = [
    { day: 14, temp: 38.5 },
    { day: 13, temp: 38.6 },
    { day: 12, temp: 38.4 },
    { day: 11, temp: 38.6 },
    { day: 10, temp: 38.5 },
    { day: 9,  temp: 38.4 },
    { day: 8,  temp: 38.6 },
    { day: 7,  temp: 38.5 },
    { day: 6,  temp: 38.7 },
    // Mild subclinical elevation starts
    { day: 5,  temp: 38.9 },
    { day: 4,  temp: 39.0 },
    { day: 3,  temp: 39.1 },
    { day: 2,  temp: 39.1 },
    { day: 1,  temp: 39.2 }
  ];

  const base = new Date();
  base.setHours(7, 30, 0, 0);

  const batch = [];
  for (const item of gangaTemps) {
    const timestamp = new Date(base.getTime() - item.day * 86400000);
    batch.push({ cattleId: cow.id, value: item.temp, timestamp, source: 'manual' });
  }

  await p.temperatureLog.createMany({ data: batch });
  console.log('✅ Ganga temperatures aligned with her Watch status (38.5 -> 39.2 C)!');
  process.exit(0);
}

alignGangaWatchTemps().catch(e => { console.error(e); process.exit(1); });

