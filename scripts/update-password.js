const path = require('path');
const fs = require('fs');

// Load .env.local
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

async function updatePassword() {
  const p = new PrismaClient();
  try {
    const email = 'theofflsabari@gmail.com';
    const newPassword = 'sabari2005';

    const user = await p.user.findUnique({ where: { email } });
    if (!user) {
      console.log(`❌ No user found with email: ${email}`);
      return;
    }

    const passwordHash = await bcrypt.hash(newPassword, 12);
    await p.user.update({
      where: { email },
      data: { passwordHash },
    });

    console.log(`✅ Password updated for ${email}`);
    console.log(`   Name: ${user.name}`);
    console.log(`   Role: ${user.role}`);
  } catch (e) {
    console.error('Error:', e.message);
  } finally {
    await p.$disconnect();
  }
}

updatePassword();
