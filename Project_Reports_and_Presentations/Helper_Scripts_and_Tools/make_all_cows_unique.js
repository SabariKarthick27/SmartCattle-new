const { PrismaClient } = require('@prisma/client');
const p = new PrismaClient();

async function makeAllCowsNaturallySpaced() {
  console.log('Spreading all 4 cows across unique, realistic historical enrollment timelines...');

  const farmerId = 'cmu9zooas000044fhz2zx6no0';

  // 1. Lakshmi (TN-SC-3608) - HF Crossbred - Veteran cow in herd for 4 months
  // Enrolled 01 July 2026. Has continuous records through Oct.
  const c1 = await p.cattle.findFirst({ where: { tagId: 'TN-SC-3608' } });
  if (c1) {
    await p.cattle.update({
      where: { id: c1.id },
      data: { createdAt: new Date('2026-07-01T08:00:00Z'), dob: new Date('2021-04-12') }
    });
  }

  // 2. Ganga (TN-SC-4717) - HF Crossbred - Bought/enrolled 2 months ago (15 August 2026)
  // Has 21 daily logs leading up to yesterday (where her mild drop started)
  const c2 = await p.cattle.findFirst({ where: { tagId: 'TN-SC-4717' } });
  if (c2) {
    await p.cattle.update({
      where: { id: c2.id },
      data: { createdAt: new Date('2026-08-15T09:30:00Z'), dob: new Date('2022-01-20') }
    });
  }

  // 3. Kamadhenu (TN-SC-1042) - Jersey Crossbred - Enrolled 1 month ago (18 September 2026)
  // Has logs starting from 20 Sep 2026
  const c3 = await p.cattle.findFirst({ where: { tagId: 'TN-SC-1042' } });
  if (c3) {
    await p.cattle.update({
      where: { id: c3.id },
      data: { createdAt: new Date('2026-09-18T10:15:00Z'), dob: new Date('2022-03-15') }
    });
  }

  // 4. Nandhini (TN-SC-2026) - Kangayam (Draught) - Newly purchased 4 days ago (26 October 2026)
  // Only 3 logs (27 Oct, 28 Oct, 29 Oct) -> Perfectly justifies Abstain mode!
  const c4 = await p.cattle.findFirst({ where: { tagId: 'TN-SC-2026' } });
  if (c4) {
    await p.cattle.update({
      where: { id: c4.id },
      data: { createdAt: new Date('2026-10-26T11:45:00Z'), dob: new Date('2023-06-10') }
    });
  }

  console.log('✅ Updated all cows with unique enrollment and registration dates!');
  process.exit(0);
}

makeAllCowsNaturallySpaced().catch(e => { console.error(e); process.exit(1); });

