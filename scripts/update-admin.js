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

// Override DATABASE_URL with DIRECT_URL for direct connection
if (process.env.DIRECT_URL) {
  process.env.DATABASE_URL = process.env.DIRECT_URL;
}

const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcryptjs');

async function main() {
  const prisma = new PrismaClient();
  try {
    const passwordHash = await bcrypt.hash('admin2005', 12);
    
    // 1. Create or update primary admin: admin.smartcattle@gmail.com
    const admin = await prisma.user.upsert({
      where: { email: 'admin.smartcattle@gmail.com' },
      update: {
        passwordHash,
        role: 'admin',
        isVerified: true,
        isActive: true,
      },
      create: {
        name: 'SmartCattle Primary Admin',
        phone: '+91-9876543210',
        email: 'admin.smartcattle@gmail.com',
        passwordHash,
        role: 'admin',
        isVerified: true,
        isActive: true,
      },
    });

    console.log(`✅ Primary Admin created/updated: ${admin.email}`);

    // 2. Find and delete all other admins
    const otherAdmins = await prisma.user.findMany({
      where: {
        role: 'admin',
        NOT: { email: 'admin.smartcattle@gmail.com' },
      },
    });

    for (const oldAdmin of otherAdmins) {
      await prisma.auditLog.deleteMany({ where: { actorId: oldAdmin.id } });
      await prisma.passwordResetToken.deleteMany({ where: { userId: oldAdmin.id } });
      await prisma.user.delete({ where: { id: oldAdmin.id } });
      console.log(`❌ Removed old admin: ${oldAdmin.email}`);
    }

    console.log('\n🎉 Successfully updated primary admin and removed all other admin logins.');

  } catch (err) {
    console.error('Error updating admin:', err);
  } finally {
    await prisma.$disconnect();
  }
}

main();
