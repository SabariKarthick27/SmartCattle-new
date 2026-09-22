const { PrismaClient } = require('@prisma/client');

async function checkTables() {
  const p = new PrismaClient({
    datasources: { db: { url: process.env.DATABASE_URL } }
  });
  try {
    const tables = await p.$queryRaw`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public' 
      ORDER BY table_name
    `;
    console.log('Tables in public schema:');
    tables.forEach(t => console.log(' -', t.table_name));

    const types = await p.$queryRaw`
      SELECT typname FROM pg_type WHERE typtype = 'e' AND typnamespace = (
        SELECT oid FROM pg_namespace WHERE nspname = 'public'
      )
    `;
    console.log('\nEnum types:');
    types.forEach(t => console.log(' -', t.typname));
  } catch(e) {
    console.error('Check error:', e.message);
  } finally {
    await p.$disconnect();
  }
}

checkTables();
