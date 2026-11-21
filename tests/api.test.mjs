// يختبر كل نقاط الـ API على PostgreSQL محلي فيه schema.sql + seed.sql
// التشغيل: PGURI="host=/tmp port=5544 user=postgres dbname=dabrah_test" node tests/api.test.mjs
// (يستخدم psql من سطر الأوامر، فما يحتاج أي مكتبة)
import { execFileSync } from 'node:child_process';
import { handle } from '../netlify/functions/lib/routes.mjs';
import assert from 'node:assert/strict';

const uri = process.env.PGURI || 'host=/tmp port=5544 user=postgres dbname=dabrah_test';
const lit = (v) => v === null || v === undefined ? 'NULL' : typeof v === 'number' || typeof v === 'boolean' ? String(v) : "'" + String(v).replace(/'/g, "''") + "'";
const db = { async query(text, params = []) {
  const sql = text.replace(/\$(\d+)/g, (_, i) => lit(params[i - 1]));
  const isRead = /^\s*SELECT/i.test(sql) || /RETURNING/i.test(sql);
  const wrapped = isRead ? `WITH t AS (${sql}) SELECT COALESCE(json_agg(t),'[]') FROM t` : sql;
  const out = execFileSync('psql', [uri, '-v', 'ON_ERROR_STOP=1', '-Atq', '-c', wrapped], { encoding: 'utf8' }).trim();
  return { rows: isRead ? JSON.parse(out || '[]') : [] };
} };

const call = (m, p, b) => handle(db, m, p, b);
let n = 0; const ok = (name) => { n++; console.log('✓', name); };

let r = await call('GET', '/bootstrap'); assert.equal(r.status, 200); assert.equal(r.body.employees.length, 21); assert.equal(r.body.employees[0].n, 'عبدالله الشمري');
assert.equal(Object.values(r.body.weights).reduce((a, b) => a + b, 0), 100); ok('bootstrap');
r = await call('POST', '/submissions', { type: 'report', score: 8, text: 'تقرير' }); assert.equal(r.status, 201); assert.equal(r.body.level, 3); assert.equal(r.body.fronds, 8); ok('report → ذيب + 8 سعفات');
r = await call('POST', '/submissions', { type: 'certificate', skillId: 'inv', answers: [1, 1, 0, 1] }); assert.equal(r.body.score, 4); assert.equal(r.body.level, 4); ok('certificate graded on server → سنع');
r = await call('POST', '/submissions', { type: 'certificate', skillId: 'cap', answers: [0, 0, 0, 0] }); assert.equal(r.body.approved, false); ok('weak certificate → theory');
r = await call('POST', '/skills/xl/renewals', { score: 3 }); assert.equal(r.body.passed, true); ok('renewal');
for (const [m, p, b] of [['POST', '/mentorship/sessions'], ['DELETE', '/mentorship/sessions/mine'], ['POST', '/workshops/wms/registrations'], ['DELETE', '/workshops/wms/registrations/me'], ['POST', '/courses/k1/registrations'], ['PATCH', '/content/c1/progress', { status: 'saved' }], ['PATCH', '/content/c1/progress', { status: 'done' }], ['POST', '/internal-jobs/p1/applications'], ['PATCH', '/employees/1/leave', { onLeave: true }], ['POST', '/rotations/r1/approval'], ['DELETE', '/rotations/r1/approval'], ['POST', '/shadowing', { skillId: 'wms' }], ['PATCH', '/positions/p3', { decision: 'إغلاق' }], ['PATCH', '/notifications/ready', { role: 'haya' }], ['POST', '/auth/login', { role: 'mgr' }]]) {
  r = await call(m, p, b || {}); assert.ok(r.status < 300, `${m} ${p} → ${r.status} ${JSON.stringify(r.body)}`);
} ok('learning, jobs, leave, rotations, shadowing, positions, notifications, login');
r = await call('PATCH', '/promotions/1', { interview: 'fail', reason: 'قصير' }); assert.equal(r.status, 400); ok('rejection without reason is refused');
r = await call('PATCH', '/promotions/1', { interview: 'fail', reason: 'ما قدر يشرح خطوات حل تحدي الجرد بنفسه' }); assert.equal(r.status, 200);
r = await call('PATCH', '/promotions/1/escalation', { decision: 'overturn' }); assert.equal(r.status, 200); ok('reject with reason → escalation → overturn');
for (const role of ['top', 'haya', 'committee']) r = await call('POST', '/promotions/exceptional/1/votes', { approverRole: role });
assert.equal(r.body.votes, 3); ok('exceptional promotion: 3 votes');
r = await call('POST', '/competency-profiles/ops-planner/change-requests', { weights: { cap: 50, inv: 40 } }); assert.equal(r.status, 400); ok('weights must total 100');
const w = (await call('GET', '/bootstrap')).body.weights; w.cap += 5; w.inv -= 5;
r = await call('POST', '/competency-profiles/ops-planner/change-requests', { weights: w }); assert.equal(r.status, 201);
r = await call('PATCH', '/competency-profiles/ops-planner/change-requests/latest', { decision: 'approve' }); assert.equal(r.status, 200); ok('weights change request → approved');
r = await call('POST', '/development-plans', { skillId: 'cap', employeeIds: [1, 3, 4] }); assert.equal(r.status, 201); assert.equal(r.body.net, 3 * 3200 * 0.3); ok('plan cost computed on server (هدف 70%)');
r = await call('PATCH', '/development-plans/by-skill/cap', { status: 'ok' }); assert.equal(r.status, 200); ok('plan approved');
r = await call('GET', '/bootstrap'); assert.equal(r.body.plans.length, 1); assert.deepEqual(r.body.plans[0].sel, [0, 2, 3]); assert.equal(r.body.employees[0].ai, 3); assert.equal(r.body.employees[0].inv, 4); assert.equal(r.body.weights.cap, 20); ok('bootstrap reflects all writes');
r = await call('GET', '/nope'); assert.equal(r.status, 404); ok('unknown route → 404');
console.log(`\n${n} اختبار نجحت`);
