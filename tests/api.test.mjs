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

// جلسات حقيقية لحسابات العرض: الموظف (عبدالله) للمسارات الشخصية، والمدير لمسارات الإدارة
const login = async (email) => (await handle(db, 'POST', '/auth/login', { email, password: 'Dabrah2026' }, { secure: false })).cookie.match(/dabrah_session=([^;]+)/)[1];
const EMP_T = await login('abdullah.alshammari@sharq.sa'), MGR_T = await login('mohammed.alanazi@sharq.sa');
const PERSONAL = /^\/(bootstrap|submissions|skills|employees|mentorship|workshops|courses|content|internal-jobs|notifications)/;
const call = (m, p, b, t) => handle(db, m, p, b, { token: t ?? (PERSONAL.test(p) ? EMP_T : MGR_T), secure: false });
let n = 0; const ok = (name) => { n++; console.log('✓', name); };

let r = await call('GET', '/bootstrap'); assert.equal(r.status, 200); assert.equal(r.body.employees.length, 21); assert.equal(r.body.employees[0].n, 'عبدالله الشمري');
assert.equal(Object.values(r.body.weights).reduce((a, b) => a + b, 0), 100); ok('bootstrap');
r = await call('POST', '/submissions', { type: 'report', score: 8, text: 'تقرير' }); assert.equal(r.status, 201); assert.equal(r.body.level, 3); assert.equal(r.body.fronds, 8); ok('report → ذيب + 8 سعفات');
r = await call('POST', '/submissions', { type: 'certificate', skillId: 'inv', answers: [1, 1, 0, 1] }); assert.equal(r.body.score, 4); assert.equal(r.body.level, 4); ok('certificate graded on server → سنع');
r = await call('POST', '/submissions', { type: 'certificate', skillId: 'cap', answers: [0, 0, 0, 0] }); assert.equal(r.body.approved, false); ok('weak certificate → theory');
r = await call('POST', '/skills/xl/renewals', { score: 3 }); assert.equal(r.body.passed, true); ok('renewal');
for (const [m, p, b] of [['POST', '/mentorship/sessions'], ['DELETE', '/mentorship/sessions/mine'], ['POST', '/workshops/wms/registrations'], ['DELETE', '/workshops/wms/registrations/me'], ['POST', '/courses/k1/registrations'], ['PATCH', '/content/c1/progress', { status: 'saved' }], ['PATCH', '/content/c1/progress', { status: 'done' }], ['POST', '/internal-jobs/p1/applications'], ['PATCH', '/employees/1/leave', { onLeave: true }], ['POST', '/rotations/r1/approval'], ['DELETE', '/rotations/r1/approval'], ['POST', '/shadowing', { skillId: 'wms' }], ['PATCH', '/positions/p3', { decision: 'إغلاق' }], ['PATCH', '/notifications/ready', {}]]) {
  r = await call(m, p, b || {}); assert.ok(r.status < 300, `${m} ${p} → ${r.status} ${JSON.stringify(r.body)}`);
} ok('learning, jobs, leave, rotations, shadowing, positions, notifications');
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
r = await call('GET', '/bootstrap'); assert.equal(r.body.plans.length, 1); assert.deepEqual(r.body.plans[0].sel, [1, 3, 4]); assert.equal(r.body.employees[0].ai, 3); assert.equal(r.body.employees[0].inv, 4); assert.equal(r.body.weights.cap, 20); ok('bootstrap reflects all writes');
r = await call('GET', '/nope'); assert.equal(r.status, 404); ok('unknown route → 404');

// ---------- الحسابات ----------
const raw = (m, p, b, t) => handle(db, m, p, b || {}, { token: t, secure: false });
const tok = (r) => r.cookie.match(/dabrah_session=([^;]+)/)[1];
r = await raw('GET', '/bootstrap'); assert.equal(r.status, 401); ok('no session → 401');
r = await raw('POST', '/auth/login', { email: 'abdullah.alshammari@sharq.sa', password: 'wrong123' }); assert.equal(r.status, 401); assert.equal(r.body.error, 'البريد أو كلمة المرور غلط'); ok('wrong password refused');
r = await raw('POST', '/auth/login', { email: 'ABDULLAH.alshammari@sharq.sa ', password: 'Dabrah2026' }); assert.equal(r.status, 200); assert.match(r.cookie, /HttpOnly/); assert.equal(r.body.user.employeeId, 1); ok('demo login (email case-insensitive) + HttpOnly cookie');
r = await raw('POST', '/auth/signup', { role: 'emp' }); assert.equal(r.status, 400); for (const k of ['name', 'eid', 'email', 'gender', 'nat', 'title', 'dept', 'password']) assert.ok(r.body.fields[k], 'missing error for ' + k); ok('empty signup → every required field flagged');
const good = { role: 'emp', name: 'ليان الحربي', eid: '٥٥٥١٢', email: 'Layan@Test.sa', gender: 'f', nat: 'sa', title: 'منسقة مخزون', dept: '1', password: 'Layan2026', confirm: 'Layan2026' };
r = await raw('POST', '/auth/signup', { ...good, password: 'short', confirm: 'short' }); assert.equal(r.status, 400); assert.ok(r.body.fields.password); ok('weak password refused');
r = await raw('POST', '/auth/signup', { ...good, confirm: 'Other2026' }); assert.equal(r.status, 400); assert.ok(r.body.fields.confirm); ok('password confirmation must match');
r = await raw('POST', '/auth/signup', { ...good, email: 'abdullah.alshammari@sharq.sa' }); assert.equal(r.status, 409); assert.ok(r.body.fields.email); ok('duplicate email refused');
r = await raw('POST', '/auth/signup', { ...good, eid: '10482' }); assert.equal(r.status, 409); assert.ok(r.body.fields.eid); ok('duplicate employee number refused');
r = await raw('POST', '/auth/signup', good); assert.equal(r.status, 201); const NEW_T = tok(r); assert.equal(r.body.user.email, 'layan@test.sa'); ok('new employee signs up, no email confirmation, logged in at once');
r = await raw('GET', '/bootstrap', null, NEW_T); const nb = r.body;
assert.equal(nb.employees[0].n, 'ليان الحربي'); assert.equal(nb.employees[0].fresh, true); assert.equal(nb.employees[0].fr, 0);
assert.deepEqual([nb.employees[0].cap, nb.employees[0].ai, nb.employees[0].inv, nb.employees[0].lead], [1, 1, 1, 1]); assert.equal(nb.employees[0].d, 1);
assert.deepEqual([nb.me.ws, nb.me.courses, nb.me.content, nb.me.applied, nb.me.mentorBook], [{}, {}, {}, {}, false]); ok('new account starts empty (level 1, 0 fronds, no registrations)');
r = await call('GET', '/bootstrap', null, MGR_T); assert.equal(r.body.employees.length, 21); assert.ok(!r.body.employees.some((e) => e.n === 'ليان الحربي')); ok('new sign-up not in manager team lists');
r = await raw('POST', '/workshops/ai/registrations', {}, NEW_T); assert.equal(r.status, 201);
r = await raw('GET', '/bootstrap', null, NEW_T); assert.deepEqual(r.body.me.ws, { ai: 1 });
r = await raw('GET', '/bootstrap', null, EMP_T); assert.ok(!r.body.me.ws.ai || r.body.me.employeeId === 1); assert.equal(r.body.employees[0].n, 'عبدالله الشمري'); ok('each account saves to its own record');
r = await raw('PATCH', '/employees/1/leave', { onLeave: true }, NEW_T); assert.equal(r.status, 403); ok("can't change someone else's leave");
r = await raw('POST', '/rotations/r1/approval', {}, NEW_T); assert.equal(r.status, 403); ok('employee blocked from manager actions');
r = await raw('POST', '/submissions', { type: 'report', score: 8 }, MGR_T); assert.equal(r.status, 403); ok('manager has no personal employee record');
r = await raw('POST', '/auth/signup', { role: 'haya', name: 'نوف السالم', eid: '7788', email: 'nouf@test.sa', org: 'منشأة تجربة', count: '30', password: 'Nouf2026x', confirm: 'Nouf2026x' }); assert.equal(r.status, 201); assert.equal(r.body.user.employeeId, null); ok('non-employee roles sign up without an employee record');
r = await raw('POST', '/auth/logout', {}, NEW_T); assert.match(r.cookie, /Max-Age=0/);
r = await raw('GET', '/auth/me', null, NEW_T); assert.equal(r.body.user, null); r = await raw('GET', '/bootstrap', null, NEW_T); assert.equal(r.status, 401); ok('logout ends the session');

// ---------- مساعد دبره (Gemini وهمي محلي يسجّل الطلبات) ----------
import http from 'node:http';
const seen = []; let mode = 'ok', orMode = 'ok';
const fake = http.createServer(async (req, res) => {
  let b = ''; for await (const c of req) b += c; const j = JSON.parse(b || '{}');
  seen.push({ url: req.url, key: req.headers['x-goog-api-key'], auth: req.headers.authorization, body: j });
  if (req.url.startsWith('/api/v1/chat/completions')) {
    if (orMode === 'credits') { res.writeHead(402, { 'content-type': 'application/json' }); return res.end(JSON.stringify({ error: { code: 402, message: 'Insufficient credits' } })); }
    res.writeHead(200, { 'content-type': 'application/json' }); return res.end(JSON.stringify({ model: j.model, choices: [{ message: { role: 'assistant', content: '<think>x</think>أبشر، هذا رد Qwen.' } }] }));
  }
  const send = (st, o) => { res.writeHead(st, { 'content-type': 'application/json' }); res.end(JSON.stringify(o)); };
  if (mode === '404first' && req.url.includes('gemini-flash-latest')) return send(404, { error: { message: 'not found' } });
  if (mode === '429') return send(429, { error: { message: 'quota' } });
  if (mode === '503first' && req.url.includes('gemini-flash-latest')) return send(503, { error: { code: 503, message: 'This model is currently experiencing high demand.', status: 'UNAVAILABLE' } });
  if (mode === '503all') return send(503, { error: { code: 503, status: 'UNAVAILABLE' } });
  if (mode === 'badkey') return send(400, { error: { message: 'API key not valid' } });
  send(200, { candidates: [{ content: { parts: [{ text: 'هلا والله! أول خطوة: ابدأ تحدي التقرير الأسبوعي.' }] } }] });
}).listen(0);
await new Promise((r) => fake.once('listening', r));
process.env.GEMINI_BASE_URL = 'http://127.0.0.1:' + fake.address().port;
const SARA = tok(await raw('POST', '/auth/signup', { role: 'emp', name: 'ساره الجريبه', eid: '12345678', email: 'sara@x.sa', gender: 'f', nat: 'sa', title: 'مشرفة', dept: '0', password: 'Sara2026x', confirm: 'Sara2026x' }));
const ask = (t, extra = {}) => raw('POST', '/chat', { messages: [{ role: 'user', text: 'وش أسوي عشان أترقى؟' }], snapshot: { ready: 0, fronds: 0, newAccount: true, skills: [{ n: 'إدارة المخزون', t: 'فنية', lv: 'مبتدئ', req: 'سنع', w: 12, proven: false }] }, ...extra }, t);
r = await raw('POST', '/chat', { messages: [{ role: 'user', text: 'هلا' }] }); assert.equal(r.status, 401); ok('chat needs a session');
delete process.env.GEMINI_API_KEY; r = await ask(SARA); assert.equal(r.status, 503); assert.equal(r.body.code, 'no_key'); ok('no API key → clear "not enabled" message');
process.env.GEMINI_API_KEY = 'test-key-123';
r = await ask(SARA); assert.equal(r.status, 200); assert.match(r.body.reply, /هلا والله/); assert.equal(r.body.left, 39); ok('reply returned, daily counter shown');
const sent = seen.at(-1); const sys = sent.body.systemInstruction.parts[0].text;
assert.equal(sent.key, 'test-key-123'); assert.ok(sent.url.includes('gemini-flash-latest:generateContent')); ok('key sent only server-side in header, default model');
assert.ok(sys.includes('ساره الجريبه') && sys.includes('لهجة سعودية') && sys.includes('المؤنث')); ok('Saudi persona, her name, feminine address');
assert.ok(sys.includes('إدارة المخزون') && sys.includes('"حساب_جديد": true')); ok('her own skills and new-account status in context');
// أسماء مقدّمي الورش والمرشد معلومات عامة يشوفها كل موظف في «التعلّم»؛ الممنوع بيانات أداء أي موظف ثاني
assert.ok(!sys.includes('فهد الدوسري') && !sys.includes('عبدالله الشمري') && !sys.includes('سارة الزهراني') && !/score_360|performance|b360|"perf"|4\.4|3\.6/.test(sys)); ok("no other employee's personal or performance data sent to Gemini");
assert.deepEqual(sent.body.contents, [{ role: 'user', parts: [{ text: 'وش أسوي عشان أترقى؟' }] }]); ok('message passed as-is');
r = await raw('POST', '/chat', { messages: [{ role: 'user', text: 'س' }], snapshot: { ready: 75 } }, EMP_T); const sysA = seen.at(-1).body.systemInstruction.parts[0].text;
assert.ok(sysA.includes('عبدالله الشمري') && sysA.includes('المذكر') && sysA.includes('ورش')); ok("Abdullah's chat gets his own context, masculine address");
r = await raw('POST', '/chat', { messages: [{ role: 'user', text: 'كيف أوزّع العبء؟' }] }, MGR_T); assert.equal(r.status, 200); assert.ok(!seen.at(-1).body.systemInstruction.parts[0].text.includes('تسجيلاتي')); ok('manager chat works without personal employee data');
r = await raw('POST', '/chat', { messages: [{ role: 'user', text: 'x'.repeat(5000) }] }, SARA); assert.equal(seen.at(-1).body.contents[0].parts[0].text.length, 600); ok('long messages clipped to 600 chars');
r = await raw('POST', '/chat', { messages: [] }, SARA); assert.equal(r.status, 400);
r = await raw('POST', '/chat', { messages: [{ role: 'user', text: 'a' }, { role: 'model', text: 'b' }] }, SARA); assert.equal(r.status, 400); ok('empty / malformed conversation refused');
mode = '404first'; r = await ask(SARA); assert.equal(r.status, 200); assert.ok(seen.at(-1).url.includes('gemini-3.8-flash')); ok('retired model (404) → next Gemini model (3.8-flash)');
mode = '503first'; r = await ask(SARA); assert.equal(r.status, 200); assert.ok(seen.at(-1).url.includes('gemini-3.8-flash')); ok('model overloaded (503, what happened live) → next model answers');
mode = '503all'; r = await ask(SARA); assert.equal(r.status, 503); assert.equal(r.body.code, 'busy'); ok('all models overloaded → clear "busy, try in a minute"');
mode = '429'; r = await ask(SARA); assert.equal(r.status, 429); assert.equal(r.body.code, 'rate'); ok('Gemini busy → friendly retry message');
mode = 'badkey'; r = await ask(SARA); assert.equal(r.status, 502); assert.equal(r.body.code, 'key'); assert.ok(!JSON.stringify(r.body).includes('test-key')); ok('bad key → generic message, key never echoed');
mode = 'ok';
const sid = (await raw('GET', '/auth/me', null, SARA)).body.user.id;
await db.query('UPDATE chat_usage SET n=40 WHERE user_id=$1', [sid]);
r = await ask(SARA); assert.equal(r.status, 429); assert.equal(r.body.code, 'daily'); ok('daily limit of 40 messages per account');
r = await raw('GET', '/chat/status', null, SARA); assert.deepEqual([r.body.enabled, r.body.limit], [true, 40]); ok('status endpoint');

// ---------- Qwen احتياط عبر OpenRouter ----------
await db.query('DELETE FROM chat_usage WHERE user_id=$1', [sid]); // حد اليوم انستهلك في الاختبار اللي قبل
process.env.OPENROUTER_API_KEY = 'sk-or-test'; process.env.OPENROUTER_BASE_URL = process.env.GEMINI_BASE_URL;
mode = 'ok'; r = await ask(SARA); assert.equal(r.body.provider, 'gemini'); ok('Gemini answers first when available');
mode = '503all'; r = await ask(SARA); const q = seen.at(-1);
assert.equal(r.status, 200); assert.equal(r.body.provider, 'qwen'); assert.equal(r.body.reply, 'أبشر، هذا رد Qwen.'); ok('all Gemini models busy → Qwen answers (thinking tags stripped)');
assert.equal(q.auth, 'Bearer sk-or-test'); assert.equal(q.body.model, 'qwen/qwen3-next-80b-a3b-instruct'); assert.equal(q.body.models.length, 3); ok('Qwen called with Bearer key and 3 Qwen fallbacks');
assert.equal(q.body.messages[0].role, 'system'); assert.ok(q.body.messages[0].content.includes('ساره الجريبه') && q.body.messages[0].content.includes('لهجة سعودية')); ok('Qwen gets the same Saudi persona and her context');
orMode = 'credits'; r = await ask(SARA); assert.equal(r.status, 503); assert.equal(r.body.code, 'busy'); ok('Gemini busy + Qwen out of credits → friendly busy message');
orMode = 'ok'; delete process.env.GEMINI_API_KEY; mode = 'ok'; r = await ask(SARA); assert.equal(r.body.provider, 'qwen'); ok('works with Qwen alone if the Gemini key is removed');
delete process.env.OPENROUTER_API_KEY; r = await ask(SARA); assert.equal(r.body.code, 'no_key'); ok('no keys at all → "not enabled"');
fake.close();

// ---------- عالمين: العرض والحقيقي ----------
const REAL_MGR = tok(await raw('POST', '/auth/signup', { role: 'mgr', name: 'ساره الجريبه', eid: '22222222', email: 'rm@x.sa', dept: '0', team: '5', password: 'Sara2026x', confirm: 'Sara2026x' }));
const REAL_EMP = tok(await raw('POST', '/auth/signup', { role: 'emp', name: 'ريما العتيبي', eid: '33333333', email: 're@x.sa', gender: 'f', nat: 'sa', title: 'مشرفة', dept: '0', password: 'Rima2026x', confirm: 'Rima2026x' }));
const REAL_HR = tok(await raw('POST', '/auth/signup', { role: 'haya', name: 'نوف السالم', eid: '44444444', email: 'rh@x.sa', org: 'منشأة', count: '30', password: 'Nouf2026x', confirm: 'Nouf2026x' }));
const REAL_TOP = tok(await raw('POST', '/auth/signup', { role: 'top', name: 'فهد الحربي', eid: '55555555', email: 'rt@x.sa', title: 'مدير عام', password: 'Fahd2026x', confirm: 'Fahd2026x' }));
r = await raw('GET', '/bootstrap', null, REAL_MGR); const names = r.body.employees.map((e) => e.n);
assert.ok(names.includes('ريما العتيبي') && !names.includes('عبدالله الشمري') && !names.includes('ماجد القحطاني')); ok('real manager sees real employees only, no sample staff');
assert.equal(r.body.me.demo, false); assert.ok(r.body.history.every((h) => !['ماجد القحطاني', 'نورة السبيعي'].includes(h.who))); assert.ok(r.body.audit.every((a) => a.who !== 'هيا')); ok('real world: no sample approvals or governance log');
r = await raw('GET', '/bootstrap', null, MGR_T); assert.equal(r.body.employees.length, 21); assert.ok(!r.body.employees.some((e) => e.n === 'ريما العتيبي')); assert.equal(r.body.me.demo, true); ok('demo manager still sees exactly the 21 sample staff');
await raw('POST', '/submissions', { type: 'report', score: 8 }, REAL_EMP);
r = await raw('GET', '/bootstrap', null, REAL_MGR); assert.equal(r.body.history[0].who, 'ريما العتيبي');
r = await raw('GET', '/bootstrap', null, MGR_T); assert.ok(!r.body.history.some((h) => h.who === 'ريما العتيبي')); ok("real employee's approval shows in the real world only");
for (const [m, p, b] of [['PATCH', '/promotions/1', { interview: 'pass' }], ['POST', '/rotations/r1/approval'], ['PATCH', '/positions/p1', { decision: 'x' }], ['POST', '/shadowing', { skillId: 'wms' }], ['POST', '/competency-profiles/ops-planner/change-requests', { weights: {} }]]) {
  r = await raw(m, p, b || {}, REAL_MGR); assert.equal(r.status, 403, p);
} ok('real accounts cannot change demo-only items (Majed file, rotations, positions, weights)');
const rimaId = (await raw('GET', '/auth/me', null, REAL_EMP)).body.user.employeeId;
r = await raw('POST', '/development-plans', { skillId: 'cap', employeeIds: [rimaId, 1, 2] }, REAL_HR); assert.equal(r.status, 201); assert.equal(r.body.net, 1 * 3200 * 0.3); ok('real HR plan only includes real employees (sample ids dropped)');
r = await raw('GET', '/bootstrap', null, REAL_TOP); assert.equal(r.body.plans.length, 1); assert.deepEqual(r.body.plans[0].sel, [rimaId]); assert.deepEqual(r.body.applicants, []);
r = await raw('GET', '/bootstrap', null, MGR_T); assert.ok(!r.body.plans.some((p) => p.sel.includes(rimaId))); ok('plans are separated by world');
r = await raw('PATCH', '/development-plans/by-skill/cap', { status: 'ok' }, REAL_TOP); assert.equal(r.status, 200);
r = await raw('GET', '/bootstrap', null, REAL_HR); assert.equal(r.body.plans[0].st, 'ok'); r = await raw('GET', '/bootstrap', null, MGR_T); assert.equal(r.body.plans.find((p) => p.k === 'cap').st, 'ok'); ok('top approval affects the real plan only (demo plan untouched)');
await raw('POST', '/internal-jobs/p1/applications', {}, REAL_EMP); r = await raw('GET', '/bootstrap', null, REAL_HR); assert.deepEqual(r.body.applicants.map((a) => [a.who, a.job]), [['ريما العتيبي', 'منسّق تخطيط عمليات']]); ok('real HR sees real internal-job applicants');
console.log(`\n${n} اختبار نجحت`);
