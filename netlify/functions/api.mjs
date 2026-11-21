// دبره · دالة Netlify وحدة تخدم كل نقاط /api/*
// تحتاج متغير البيئة DATABASE_URL (PostgreSQL: Neon أو Supabase أو غيرها، مع ?sslmode=require)
import pg from 'pg';
import { handle } from './lib/routes.mjs';

let pool;
const db = () => (pool ??= new pg.Pool({ connectionString: process.env.DATABASE_URL, max: 3 }));

export default async (req) => {
  const url = new URL(req.url);
  const path = url.pathname.replace(/^\/(\.netlify\/functions\/api|api)/, '') || '/';
  if (req.method === 'OPTIONS') return new Response(null, { status: 204 });
  if (!process.env.DATABASE_URL) return Response.json({ error: 'DATABASE_URL غير معرّف في إعدادات Netlify' }, { status: 500 });
  let body = {};
  if (!['GET', 'HEAD'].includes(req.method)) { try { body = await req.json(); } catch { body = {}; } }
  body.role = body.role || req.headers.get('x-dabrah-role') || 'emp';
  const client = await db().connect();
  try {
    await client.query('BEGIN');
    const out = await handle(client, req.method, path, body);
    await client.query(out.status < 400 ? 'COMMIT' : 'ROLLBACK');
    return Response.json(out.body, { status: out.status, headers: { 'Cache-Control': 'no-store' } });
  } catch (e) {
    await client.query('ROLLBACK').catch(() => {});
    console.error(e);
    return Response.json({ error: 'خطأ في الخادم' }, { status: 500 });
  } finally { client.release(); }
};

// المسار /api/* يتحوّل لهذي الدالة من netlify.toml
