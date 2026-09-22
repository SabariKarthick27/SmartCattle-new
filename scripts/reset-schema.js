const { PrismaClient } = require('@prisma/client');

async function deepReset() {
  // Use the NON-pooled direct connection for DDL operations
  const p = new PrismaClient({
    datasources: { db: { url: process.env.DIRECT_URL } }
  });

  try {
    // Check what exists
    const types = await p.$queryRaw`
      SELECT typname, nspname FROM pg_type 
      JOIN pg_namespace ON pg_namespace.oid = pg_type.typnamespace 
      WHERE typtype = 'e'
    `;
    console.log('Existing enum types:');
    types.forEach(t => console.log(` - ${t.nspname}.${t.typname}`));

    const schemas = await p.$queryRaw`SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('information_schema', 'pg_catalog', 'pg_toast')`;
    console.log('\nSchemas:', schemas.map(s => s.schema_name));

    // Drop ALL non-system schemas and recreate public
    for (const s of schemas) {
      if (s.schema_name === 'public') {
        await p.$executeRawUnsafe(`DROP SCHEMA IF EXISTS public CASCADE`);
        console.log('Dropped public schema');
      } else if (!s.schema_name.startsWith('pg_')) {
        await p.$executeRawUnsafe(`DROP SCHEMA IF EXISTS "${s.schema_name}" CASCADE`);
        console.log(`Dropped schema: ${s.schema_name}`);
      }
    }

    await p.$executeRawUnsafe('CREATE SCHEMA public');
    await p.$executeRawUnsafe('GRANT ALL ON SCHEMA public TO neondb_owner');
    await p.$executeRawUnsafe('GRANT ALL ON SCHEMA public TO PUBLIC');
    console.log('\nCreated fresh public schema');

    // Verify clean
    const remaining = await p.$queryRaw`
      SELECT typname FROM pg_type 
      WHERE typtype = 'e' 
      AND typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')
    `;
    console.log('Remaining types:', remaining.length === 0 ? 'none ✅' : remaining.map(t => t.typname));

  } catch (e) {
    console.error('Deep reset error:', e.message);
  } finally {
    await p.$disconnect();
  }
}

deepReset();
