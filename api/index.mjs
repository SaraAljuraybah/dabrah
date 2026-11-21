// دبره · دالة Vercel وحدة تخدم كل نقاط /api/*
// تحتاج متغير البيئة DATABASE_URL (رابط Supabase Pooler، المنفذ 6543)
// vercel.json يحوّل /api/<المسار> إلى /api/index?__path=<المسار>
import pg from 'pg';
import { handle } from '../netlify/functions/lib/routes.mjs';

let pool;
function db() {
  if (pool) return pool;
  let url;
  try { url = new URL(process.env.DATABASE_URL); }
  catch { throw Object.assign(new Error('DATABASE_URL مو رابط صحيح'), { code: 'BAD_URL' }); }
  const local = ['localhost', '127.0.0.1'].includes(url.hostname) || url.searchParams.get('sslmode') === 'disable';
  url.searchParams.delete('sslmode');
  pool = new pg.Pool({
    connectionString: url.toString(),
    max: 3,
    ssl: local ? false : { rejectUnauthorized: false }, // Supabase يستخدم شهادة من جهة إصدار خاصة فيه
  });
  return pool;
}

function apiPath(req) {
  const url = new URL(req.url, 'http://localhost');
  const p = url.searchParams.get('__path');
  if (p !== null) return '/' + p.replace(/^\/+/, '');
  return url.pathname.replace(/^\/api(\/index)?/, '') || '/';
}

async function main(req) {
  if (req.method === 'OPTIONS') return new Response(null, { status: 204 });
  if (!process.env.DATABASE_URL) return Response.json({ error: 'DATABASE_URL غير معرّف في إعدادات Vercel' }, { status: 500 });
  const path = apiPath(req);
  let body = {};
  if (!['GET', 'HEAD'].includes(req.method)) { try { body = await req.json(); } catch { body = {}; } }
  body.role = body.role || req.headers.get('x-dabrah-role') || 'emp';
  let client;
  try { client = await db().connect(); }
  catch (e) {
    console.error('DB connect failed:', e.code, e.message);
    const msg = e.code === '28P01' ? 'كلمة مرور قاعدة البيانات غلط في DATABASE_URL' : 'ما قدرنا نتصل بقاعدة البيانات';
    return Response.json({ error: msg }, { status: 503, headers: { 'Cache-Control': 'no-store' } });
  }
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
}

export const GET = main, POST = main, PUT = main, PATCH = main, DELETE = main, OPTIONS = main;
