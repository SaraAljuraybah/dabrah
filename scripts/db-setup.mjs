// ينشئ الجداول ويعبّي البيانات التجريبية في قاعدة DATABASE_URL.
// التشغيل: DATABASE_URL=... node scripts/db-setup.mjs        (أضف --no-seed لتخطي البيانات التجريبية)
import pg from 'pg';
import { readFileSync } from 'node:fs';
const url = process.env.DATABASE_URL;
if (!url) { console.error('عرّف DATABASE_URL أول'); process.exit(1); }
const u = new URL(url); const local = ['localhost','127.0.0.1'].includes(u.hostname); u.searchParams.delete('sslmode');
const client = new pg.Client({ connectionString: u.toString(), ssl: local ? false : { rejectUnauthorized: false } });
await client.connect();
const run = async (f) => { await client.query(readFileSync(new URL(`../database/${f}`, import.meta.url), 'utf8')); console.log('✓', f); };
try {
  await run('schema.sql');
  if (!process.argv.includes('--no-seed')) await run('seed.sql');
  await run('security.sql');
} catch (e) { console.error('✗', e.message); process.exitCode = 1; }
finally { await client.end(); }
