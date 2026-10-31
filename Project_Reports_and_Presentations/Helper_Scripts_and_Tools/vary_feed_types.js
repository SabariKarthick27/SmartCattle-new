const { PrismaClient } = require('@prisma/client');
const p = new PrismaClient();

async function varyAllFeedTypes() {
  console.log('Distributing realistic, alternating dairy feed types across all cows...');

  const options = [
    'Green Fodder (Co-4 / Napier)',
    'Concentrate Feed Mix',
    'Dry Paddy Straw',
    'Mixed Rations (TMR)',
    'Silage & Bran',
    'Green Fodder (Co-4 / Napier)',
    'Concentrate Feed Mix',
    'Oil Cake & Husk Mix',
    'Mixed Rations (TMR)',
    'Dry Paddy Straw',
    'Green Fodder (Co-4 / Napier)',
    'Concentrate Feed Mix',
    'Silage & Bran',
    'Mixed Rations (TMR)'
  ];

  // Update feed logs for all cows
  const allFeedLogs = await p.feedLog.findMany({
    orderBy: { timestamp: 'desc' }
  });

  console.log(`Found ${allFeedLogs.length} total feed logs across all cows.`);

  for (let i = 0; i < allFeedLogs.length; i++) {
    const feedType = options[i % options.length];
    await p.feedLog.update({
      where: { id: allFeedLogs[i].id },
      data: { feedType }
    });
  }

  console.log('✅ Successfully updated all feed logs with realistic, diverse feed types!');
  process.exit(0);
}

varyAllFeedTypes().catch(e => { console.error(e); process.exit(1); });

