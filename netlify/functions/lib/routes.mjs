// دبره · منطق نقاط الربط (API). مستقل عن Netlify وعن مشغّل قاعدة البيانات:
// يستقبل db فيه query(text, params) → {rows}، عشان نقدر نختبره محليًا.
// كل نقطة هنا تقابل دالة في طبقة الـ API داخل المنصة (site/index.html).

const LV = ['مبتدئ', 'شاطر', 'ذيب', 'سنع', 'دبره'];
const DEMO_EMPLOYEE_ID = 1; // عبدالله الشمري في البيانات التجريبية. استبدله بهوية المستخدم بعد ربط الدخول.

const json = (status, body) => ({ status, body });
const bad = (msg) => json(400, { error: msg });
const intParam = (v) => (/^\d+$/.test(String(v)) ? Number(v) : null);

async function one(db, text, params) { const r = await db.query(text, params); return r.rows[0]; }
async function log(db, who, item, decision, ok) {
  await db.query('INSERT INTO approvals_log (employee_name, item, decision, approved, when_text) VALUES ($1,$2,$3,$4,$5)', [who, item, decision, ok, 'اليوم']);
}
async function audit(db, actor, action) {
  await db.query('INSERT INTO audit_log (actor, action, when_text) VALUES ($1,$2,$3)', [actor, action, 'اليوم']);
}
async function empName(db, id) { return (await one(db, 'SELECT full_name FROM employees WHERE id=$1', [id]))?.full_name || ''; }
async function getLevel(db, emp, skill) { return (await one(db, 'SELECT level FROM employee_skills WHERE employee_id=$1 AND skill_code=$2', [emp, skill]))?.level || 1; }
async function setLevel(db, emp, skill, level) {
  await db.query(`INSERT INTO employee_skills (employee_id, skill_code, level) VALUES ($1,$2,$3)
    ON CONFLICT (employee_id, skill_code) DO UPDATE SET level=GREATEST(employee_skills.level, EXCLUDED.level), updated_at=now(), last_used_at=now()`, [emp, skill, level]);
}
async function addFronds(db, emp, n) { await db.query('UPDATE employees SET fronds=fronds+$2 WHERE id=$1', [emp, n]); }

// ---------- GET /bootstrap: كل اللي تحتاجه الواجهة عند الفتح ----------
async function bootstrap(db) {
  const emps = (await db.query(`
    SELECT e.id, e.full_name n, e.gender g, CASE WHEN e.is_saudi THEN 'sa' ELSE e.nationality END nat, e.department_id - 1 d,
           e.fronds fr, COALESCE(MAX(s.level) FILTER (WHERE s.skill_code='cap'),1) cap, COALESCE(MAX(s.level) FILTER (WHERE s.skill_code='ai'),1) ai,
           COALESCE(MAX(s.level) FILTER (WHERE s.skill_code='inv'),1) inv, COALESCE(MAX(s.level) FILTER (WHERE s.skill_code='lead'),1) lead,
           CASE WHEN e.excel_health='green' THEN 'g' ELSE 'y' END xl, e.score_360::float b360, e.performance perf, e.potential pot, e.weekly_hours hrs, e.on_leave
    FROM employees e LEFT JOIN employee_skills s ON s.employee_id=e.id GROUP BY e.id ORDER BY e.id`)).rows;
  const weights = Object.fromEntries((await db.query(`SELECT skill_code, weight FROM job_profile_weights WHERE job_code='ops-planner'`)).rows.map(r => [r.skill_code, r.weight]));
  const plans = (await db.query(`
    SELECT p.id, p.skill_code k, p.net_cost::float net, p.hadaf_support::float hadaf, p.status st,
           COALESCE(json_agg(m.employee_id - 1 ORDER BY m.employee_id) FILTER (WHERE m.employee_id IS NOT NULL), '[]') sel
    FROM development_plans p LEFT JOIN plan_members m ON m.plan_id=p.id GROUP BY p.id ORDER BY p.id`)).rows.map(p => ({ ...p, open: false }));
  const auditRows = (await db.query('SELECT actor who, action what, COALESCE(when_text, to_char(created_at, \'YYYY-MM-DD\')) "when" FROM audit_log ORDER BY created_at DESC, id DESC LIMIT 50')).rows;
  const history = (await db.query('SELECT employee_name who, item what, decision dec, COALESCE(when_text, \'اليوم\') "when", CASE WHEN approved THEN 1 ELSE 0 END ok FROM approvals_log ORDER BY created_at DESC, id DESC LIMIT 20')).rows;
  return json(200, { employees: emps.map(({ id, on_leave, ...e }) => e), weights, plans, audit: auditRows, history });
}

// ---------- الراوتر ----------
export async function handle(db, method, path, body = {}) {
  const p = path.replace(/\/+$/, '').split('/').filter(Boolean); // ['submissions'] …
  const me = intParam(body.employeeId) || DEMO_EMPLOYEE_ID;
  const role = body.role || 'emp';
  const R = (m, pattern) => {
    if (m !== method) return null;
    const parts = pattern.split('/').filter(Boolean);
    if (parts.length !== p.length) return null;
    const out = {};
    for (let i = 0; i < parts.length; i++) { if (parts[i].startsWith(':')) out[parts[i].slice(1)] = decodeURIComponent(p[i]); else if (parts[i] !== p[i]) return null; }
    return out;
  };
  let m;

  if ((m = R('GET', '/health'))) return json(200, { ok: true });
  if ((m = R('GET', '/bootstrap'))) return bootstrap(db);

  // POST /auth/login — تجريبي: يرجّع الدور. اربطه بمزوّد هوية حقيقي قبل البيانات الفعلية.
  if ((m = R('POST', '/auth/login'))) {
    if (!['emp', 'mgr', 'haya', 'top'].includes(body.role)) return bad('دور غير معروف');
    return json(200, { ok: true, role: body.role, demo: true });
  }

  // POST /submissions — تقرير تحدي، أو شهادة خارجية تُصحّح على الخادم
  if ((m = R('POST', '/submissions'))) {
    if (body.type === 'report') {
      const score = intParam(body.score);
      if (score === null || score > 8) return bad('درجة التقرير غير صالحة');
      const prev = await getLevel(db, me, 'ai');
      const approved = score >= 7;
      const lv = approved ? Math.max(prev, 3) : Math.max(prev, 2);
      await setLevel(db, me, 'ai', lv);
      const fr = approved ? 3 + (prev < 3 ? 5 : 0) : 1;
      await addFronds(db, me, fr);
      await db.query('INSERT INTO submissions (employee_id, skill_code, type, payload, score, level_awarded, status) VALUES ($1,$2,$3,$4,$5,$6,$7)',
        [me, 'ai', 'report', JSON.stringify({ text: body.text || '', verify: body.verify || '', fileName: body.fileName || '' }), score, lv, approved ? 'approved' : 'recorded']);
      await log(db, await empName(db, me), 'تقرير الأداء الأسبوعي', approved ? `اعتماد تلقائي «ذيب» (${score} من 8)` : `سُجّل تلقائيًا «شاطر» (${score} من 8)`, approved);
      return json(201, { level: lv, fronds: fr, approved });
    }
    if (body.type === 'certificate') {
      const k = String(body.skillId || '');
      const qs = (await db.query('SELECT correct_index FROM certificate_questions WHERE skill_code=$1 ORDER BY position', [k])).rows;
      if (!qs.length) return bad('ما فيه أسئلة لهذي المهارة');
      const ans = Array.isArray(body.answers) ? body.answers : [];
      const score = qs.filter((q, i) => Number(ans[i]) === q.correct_index).length; // التصحيح على الخادم، مو من المتصفح
      const prev = await getLevel(db, me, k);
      const req = (await one(db, 'SELECT required_level FROM skills WHERE code=$1', [k]))?.required_level || 3;
      let lv = prev, status = 'theory', fr = 0;
      if (score > 2) {
        lv = Math.max(prev, k === 'inv' ? (score === 4 ? 4 : 3) : (score === 4 ? 3 : 2));
        await setLevel(db, me, k, lv);
        fr = 3 + (lv >= req && prev < req ? 5 : 0);
        await addFronds(db, me, fr);
        status = 'approved';
      }
      await db.query('INSERT INTO submissions (employee_id, skill_code, type, payload, score, level_awarded, status) VALUES ($1,$2,$3,$4,$5,$6,$7)',
        [me, k, 'certificate', JSON.stringify({ title: body.title, issuer: body.issuer, date: body.date, cal: body.cal, fileName: body.fileName, answers: ans }), score, lv, status]);
      const sk = (await one(db, 'SELECT name FROM skills WHERE code=$1', [k]))?.name || k;
      await log(db, await empName(db, me), 'شهادة خارجية · ' + sk, score > 2 ? `اعتماد تلقائي «${LV[lv - 1]}» (${score} من 4)` : `سُجّلت نظرية تلقائيًا (${score} من 4)`, score > 2);
      return json(201, { score, level: lv, fronds: fr, approved: score > 2 });
    }
    return bad('نوع غير معروف');
  }

  // POST /skills/:id/renewals — تجديد عمر المهارة
  if ((m = R('POST', '/skills/:id/renewals'))) {
    const score = intParam(body.score) ?? 0; const passed = score >= 2;
    await db.query('INSERT INTO renewals (employee_id, skill_code, score, passed) VALUES ($1,$2,$3,$4)', [me, m.id, score, passed]);
    if (passed) {
      await db.query('UPDATE employee_skills SET last_used_at=now() WHERE employee_id=$1 AND skill_code=$2', [me, m.id]);
      if (m.id === 'xl') await db.query(`UPDATE employees SET excel_health='green' WHERE id=$1`, [me]);
      await addFronds(db, me, 1);
    }
    return json(201, { passed });
  }

  if ((m = R('PATCH', '/employees/:id/leave'))) {
    const id = intParam(m.id); if (!id) return bad('معرّف غير صالح');
    await db.query('UPDATE employees SET on_leave=$2 WHERE id=$1', [id, !!body.onLeave]); return json(200, { ok: true });
  }

  if ((m = R('POST', '/mentorship/sessions'))) {
    const mentor = await one(db, 'SELECT employee_id, slot FROM mentors LIMIT 1');
    if (!mentor) return bad('ما فيه مرشد متاح');
    const r = await one(db, 'INSERT INTO mentorship_sessions (mentee_id, mentor_id, slot) VALUES ($1,$2,$3) RETURNING id', [me, mentor.employee_id, mentor.slot]);
    return json(201, r);
  }
  if ((m = R('DELETE', '/mentorship/sessions/mine'))) {
    await db.query(`UPDATE mentorship_sessions SET status='cancelled' WHERE mentee_id=$1 AND status='booked'`, [me]); return json(200, { ok: true });
  }

  for (const [kind, table, col] of [['workshops', 'workshop_registrations', 'workshop_code'], ['courses', 'course_registrations', 'course_code']]) {
    if ((m = R('POST', `/${kind}/:id/registrations`))) {
      await db.query(`INSERT INTO ${table} (${col}, employee_id) VALUES ($1,$2) ON CONFLICT DO NOTHING`, [m.id, me]); return json(201, { ok: true });
    }
    if ((m = R('DELETE', `/${kind}/:id/registrations/me`))) {
      await db.query(`DELETE FROM ${table} WHERE ${col}=$1 AND employee_id=$2`, [m.id, me]); return json(200, { ok: true });
    }
  }

  if ((m = R('PATCH', '/content/:id/progress'))) {
    if (body.status === null || body.status === undefined || body.status === '') {
      await db.query('DELETE FROM content_progress WHERE content_code=$1 AND employee_id=$2', [m.id, me]);
    } else {
      if (!['saved', 'done'].includes(body.status)) return bad('حالة غير صالحة');
      await db.query(`INSERT INTO content_progress (content_code, employee_id, status) VALUES ($1,$2,$3)
        ON CONFLICT (content_code, employee_id) DO UPDATE SET status=EXCLUDED.status, updated_at=now()`, [m.id, me, body.status]);
    }
    return json(200, { ok: true });
  }

  if ((m = R('POST', '/internal-jobs/:id/applications'))) {
    await db.query('INSERT INTO job_applications (job_code, employee_id) VALUES ($1,$2) ON CONFLICT DO NOTHING', [m.id, me]); return json(201, { ok: true });
  }

  // ملف الترقية: المقابلة، ثم مراجعة الإدارة العليا عند الرفض
  if ((m = R('PATCH', '/promotions/:id'))) {
    const id = intParam(m.id); const pass = body.interview === 'pass'; const reason = String(body.reason || '').trim();
    if (!pass && reason.length < 10) return bad('الرفض يحتاج سبب (10 أحرف على الأقل)');
    const r = await one(db, `UPDATE promotion_files SET interview=$2, reason=$3, status=$4, updated_at=now() WHERE id=$1 RETURNING employee_id`, [id, pass ? 'pass' : 'fail', pass ? null : reason, pass ? 'sent' : 'esc']);
    if (!r) return json(404, { error: 'الملف غير موجود' });
    await log(db, await empName(db, r.employee_id), pass ? 'ملف ترقية · مخطط عمليات' : 'مقابلة ترقية', pass ? 'اكتمل الملف وانتقل للجنة تلقائيًا' : 'رفض المدير بسبب، وتحوّل للإدارة العليا', pass);
    return json(200, { ok: true });
  }
  if ((m = R('PATCH', '/promotions/:id/escalation'))) {
    const id = intParam(m.id); const uphold = body.decision === 'uphold';
    if (!['uphold', 'overturn'].includes(body.decision)) return bad('قرار غير صالح');
    const r = await one(db, `UPDATE promotion_files SET escalation_decision=$2, status=$3, updated_at=now() WHERE id=$1 AND status='esc' RETURNING employee_id`, [id, body.decision, uphold ? 'retry' : 'sent']);
    if (!r) return json(409, { error: 'الملف مو محوّل للإدارة العليا' });
    await log(db, await empName(db, r.employee_id), 'مراجعة الإدارة العليا', uphold ? 'أيّدت الرفض: تحدي إضافي ثم مقابلة ثانية' : 'ألغت الرفض، وانتقل الملف للجنة', !uphold);
    return json(200, { ok: true });
  }

  if ((m = R('POST', '/rotations/:id/approval'))) {
    const r = await one(db, 'UPDATE rotations SET approved=true, approved_at=now() WHERE code=$1 RETURNING code', [m.id]); return r ? json(200, { ok: true }) : json(404, { error: 'غير موجود' });
  }
  if ((m = R('DELETE', '/rotations/:id/approval'))) {
    await db.query('UPDATE rotations SET approved=false, approved_at=NULL WHERE code=$1', [m.id]); return json(200, { ok: true });
  }

  if ((m = R('POST', '/shadowing'))) {
    const learners = { wms: 'خالد المطيري', cold: 'سلطان العتيبي', cap: 'عبدالله الشمري' };
    const r = await one(db, 'INSERT INTO shadowing (skill_code, learner_name, weeks) VALUES ($1,$2,6) RETURNING id', [String(body.skillId || ''), learners[body.skillId] || null]);
    return json(201, r);
  }

  if ((m = R('POST', '/promotions/exceptional/:id/votes'))) {
    const id = intParam(m.id);
    await db.query('INSERT INTO exceptional_votes (promotion_id, approver_role) VALUES ($1,$2) ON CONFLICT DO NOTHING', [id, String(body.approverRole || role)]);
    const c = await one(db, 'SELECT count(*)::int n, (SELECT votes_needed FROM exceptional_promotions WHERE id=$1) need FROM exceptional_votes WHERE promotion_id=$1', [id]);
    if (c.n >= c.need) {
      const r = await one(db, `UPDATE exceptional_promotions SET status='ok' WHERE id=$1 AND status<>'ok' RETURNING employee_id, to_title`, [id]);
      if (r) await audit(db, 'اللجنة', `ترقية استثنائية: ${await empName(db, r.employee_id)} إلى ${r.to_title}`);
    }
    return json(201, { votes: c.n });
  }

  if ((m = R('PATCH', '/positions/:id'))) {
    await db.query('UPDATE positions SET decision=$2, decided_at=now() WHERE code=$1', [m.id, String(body.decision || '')]); return json(200, { ok: true });
  }

  // أوزان الجدارات: طلب تعديل، ثم قرار لجنة
  if ((m = R('POST', '/competency-profiles/:job/change-requests'))) {
    const w = body.weights || {}; const total = Object.values(w).reduce((a, b) => a + Number(b || 0), 0);
    if (total !== 100) return bad('مجموع الأوزان لازم يكون 100%');
    const r = await one(db, 'INSERT INTO weight_change_requests (job_code, weights, requested_by) VALUES ($1,$2,$3) RETURNING id', [m.job, JSON.stringify(w), 'هيا']);
    await audit(db, 'هيا', 'طلبت تعديل أوزان «مخطط عمليات»');
    return json(201, r);
  }
  if ((m = R('PATCH', '/competency-profiles/:job/change-requests/latest'))) {
    const req = await one(db, `SELECT id, weights FROM weight_change_requests WHERE job_code=$1 AND status='pending' ORDER BY id DESC LIMIT 1`, [m.job]);
    if (!req) return json(404, { error: 'ما فيه طلب معلّق' });
    const ok = body.decision === 'approve';
    await db.query('UPDATE weight_change_requests SET status=$2, decided_by=$3, decided_at=now() WHERE id=$1', [req.id, ok ? 'approved' : 'rejected', 'لجنة الموارد البشرية']);
    if (ok) for (const [k, v] of Object.entries(req.weights)) {
      await db.query(`INSERT INTO job_profile_weights (job_code, skill_code, weight) VALUES ($1,$2,$3) ON CONFLICT (job_code, skill_code) DO UPDATE SET weight=EXCLUDED.weight`, [m.job, k, v]);
    }
    await audit(db, 'لجنة الموارد البشرية', ok ? 'اعتمدت أوزان «مخطط عمليات» الجديدة' : 'رفضت تعديل الأوزان');
    return json(200, { ok: true });
  }

  // خطط التطوير: التكلفة تُحسب على الخادم من جدول البرامج
  if ((m = R('POST', '/development-plans'))) {
    const k = String(body.skillId || ''); const ids = (Array.isArray(body.employeeIds) ? body.employeeIds : []).map(intParam).filter(Boolean);
    const prog = await one(db, 'SELECT cost_per_employee::float cost, hadaf_support::float hadaf FROM programs WHERE skill_code=$1', [k]);
    if (!prog) return bad('برنامج غير معروف');
    if (!ids.length) return bad('اختاري موظف واحد على الأقل');
    await db.query(`DELETE FROM development_plans WHERE skill_code=$1 AND status='rej'`, [k]);
    const money = (x) => Math.round(x * 100) / 100;
    const net = money(ids.length * prog.cost * (1 - prog.hadaf)), hadaf = money(ids.length * prog.cost * prog.hadaf);
    const r = await one(db, 'INSERT INTO development_plans (skill_code, net_cost, hadaf_support, created_by) VALUES ($1,$2,$3,$4) RETURNING id', [k, net, hadaf, 'هيا']);
    for (const e of ids) await db.query('INSERT INTO plan_members (plan_id, employee_id) VALUES ($1,$2) ON CONFLICT DO NOTHING', [r.id, e]);
    return json(201, { id: r.id, net, hadaf });
  }
  if ((m = R('PATCH', '/development-plans/by-skill/:k'))) {
    if (!['ok', 'rej', 'wait'].includes(body.status)) return bad('حالة غير صالحة');
    const r = await one(db, `UPDATE development_plans SET status=$2 WHERE id=(SELECT id FROM development_plans WHERE skill_code=$1 ORDER BY id DESC LIMIT 1) RETURNING id`, [m.k, body.status]);
    if (r && body.status !== 'wait') await audit(db, 'فيصل', body.status === 'ok' ? 'اعتمد خطة تطوير' : 'رفض خطة تطوير');
    return r ? json(200, { ok: true }) : json(404, { error: 'الخطة غير موجودة' });
  }

  if ((m = R('PATCH', '/notifications/:key'))) {
    await db.query('INSERT INTO notification_reads (key, role) VALUES ($1,$2) ON CONFLICT DO NOTHING', [m.key, role]); return json(200, { ok: true });
  }

  return json(404, { error: 'نقطة غير معروفة', method, path });
}
