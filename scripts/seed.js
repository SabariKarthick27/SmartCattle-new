const path = require('path');
const fs = require('fs');

// Load .env.local environment variables if present
const envPath = path.resolve(__dirname, '../.env.local');
if (fs.existsSync(envPath)) {
  const envConfig = fs.readFileSync(envPath, 'utf8');
  envConfig.split('\n').forEach((line) => {
    const match = line.match(/^\s*([\w.-]+)\s*=\s*["']?([^"'\r\n]+)["']?\s*$/);
    if (match && !process.env[match[1]]) {
      process.env[match[1]] = match[2];
    }
  });
}

const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcryptjs');

async function seed() {
  const p = new PrismaClient();

  try {
    // ── Primary Admin user ───────────────────────────────────
    const adminPasswordHash = await bcrypt.hash('admin2005', 12);
    await p.user.upsert({
      where: { email: 'admin.smartcattle@gmail.com' },
      update: {
        passwordHash: adminPasswordHash,
        role: 'admin',
        isVerified: true,
        isActive: true,
      },
      create: {
        name: 'SmartCattle Admin',
        phone: '+91-9876543210',
        email: 'admin.smartcattle@gmail.com',
        passwordHash: adminPasswordHash,
        role: 'admin',
        isVerified: true,
        isActive: true,
      },
    });
    console.log('✅ Primary Admin set: admin.smartcattle@gmail.com / admin2005');

    // Remove any legacy admin accounts
    const legacyAdmins = await p.user.findMany({
      where: {
        role: 'admin',
        NOT: { email: 'admin.smartcattle@gmail.com' },
      },
    });
    for (const old of legacyAdmins) {
      await p.auditLog.deleteMany({ where: { actorId: old.id } });
      await p.passwordResetToken.deleteMany({ where: { userId: old.id } });
      await p.user.delete({ where: { id: old.id } });
      console.log('❌ Removed old admin:', old.email);
    }

    // ── Default CHDI thresholds ────────────────────────────────
    const defaults = [
      { key: 'chdi_watch_below', value: '75', description: 'CHDI score below this → Watch status' },
      { key: 'chdi_at_risk_below', value: '50', description: 'CHDI score below this → At-Risk status' },
      { key: 'chdi_min_confidence', value: '0.4', description: 'Confidence below this → Abstain' },
      { key: 'chdi_min_history_points', value: '10', description: 'Fewer logs than this → Abstain' },
    ];

    for (const s of defaults) {
      await p.settings.upsert({
        where: { key: s.key },
        create: s,
        update: {},
      });
    }
    console.log('✅ CHDI default settings seeded');

    // ── Demo farmer ────────────────────────────────────────────
    const existingFarmer = await p.user.findUnique({ where: { email: 'farmer@demo.com' } });
    if (!existingFarmer) {
      const ph = await bcrypt.hash('demo1234', 12);
      await p.user.create({
        data: {
          name: 'Ramesh Kumar',
          phone: '+91-9876543210',
          email: 'farmer@demo.com',
          passwordHash: ph,
          role: 'farmer',
          farmId: 'DEMO-FARM-01',
          assignedRegion: 'Tamil Nadu',
          isVerified: true,
          isActive: true,
        }
      });
      console.log('✅ Demo farmer created: farmer@demo.com / demo1234');
    }

    // ── Demo vet ────────────────────────────────────────────────
    const existingVet = await p.user.findUnique({ where: { email: 'vet@demo.com' } });
    if (!existingVet) {
      const ph = await bcrypt.hash('demo1234', 12);
      await p.user.create({
        data: {
          name: 'Dr. Priya Sharma',
          phone: '+91-9123456789',
          email: 'vet@demo.com',
          passwordHash: ph,
          role: 'vet',
          assignedRegion: 'Tamil Nadu',
          isVerified: true,
          isActive: true,
        }
      });
      console.log('✅ Demo vet created: vet@demo.com / demo1234');
    }

    console.log('\n✅ Seed complete!');
    console.log('   admin.smartcattle@gmail.com / admin2005');
    console.log('   farmer@demo.com / demo1234');
    console.log('   vet@demo.com / demo1234');

  } catch (e) {
    console.error('Seed error:', e.message);
  } finally {
    await p.$disconnect();
  }
}

seed();
