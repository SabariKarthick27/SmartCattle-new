const { PrismaClient } = require('@prisma/client');
const p = new PrismaClient();

async function run() {
  const types = [
    'Green Fodder (Co-4 / Napier)',
    'Concentrate Feed Mix',
    'Dry Paddy Straw',
    'Mixed Rations (TMR)',
    'Silage & Bran'
  ];

  const logs = await p.feedLog.findMany({ select: { id: true } });
  console.log(`Updating ${logs.length} feed logs...`);

  const updates = logs.map((l, idx) => 
    p.feedLog.update({
      where: { id: l.id },
      data: { feedType: types[idx % types.length] }
    })
  );

  await p.$transaction(updates);
  console.log('✅ Updated all feed logs with authentic, diverse feed types in transaction!');
  process.exit(0);
}

run().catch(e => { console.error(e); process.exit(1); });

