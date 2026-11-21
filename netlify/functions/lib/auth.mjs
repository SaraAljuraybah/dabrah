// دبره · الحسابات والجلسات
// كلمات المرور تتخزن مُجزّأة (scrypt + ملح عشوائي)، والجلسة رمز عشوائي في كوكي HttpOnly،
// ونخزّن في القاعدة بصمة الرمز (sha256) بس، عشان لو انسرقت القاعدة ما تنسرق الجلسات.
import { scrypt as _scrypt, randomBytes, timingSafeEqual, createHash } from 'node:crypto';
import { promisify } from 'node:util';
const scrypt = promisify(_scrypt);

export const COOKIE = 'dabrah_session';
export const SESSION_DAYS = 7;
const N = 16384, r = 8, p = 1, KEYLEN = 64;

export async function hashPassword(pw) {
  const salt = randomBytes(16);
  const key = await scrypt(pw, salt, KEYLEN, { N, r, p });
  return `scrypt$${N}$${r}$${p}$${salt.toString('base64')}$${key.toString('base64')}`;
}
export async function verifyPassword(pw, stored) {
  try {
    const [alg, n, rr, pp, s, k] = String(stored || '').split('$');
    if (alg !== 'scrypt') return false;
    const want = Buffer.from(k, 'base64');
    const got = await scrypt(pw, Buffer.from(s, 'base64'), want.length, { N: +n, r: +rr, p: +pp });
    return want.length === got.length && timingSafeEqual(want, got);
  } catch { return false; }
}
export const newToken = () => randomBytes(32).toString('base64url');
export const tokenHash = (t) => createHash('sha256').update(String(t)).digest('hex');

export function readCookie(header, name = COOKIE) {
  for (const part of String(header || '').split(';')) {
    const i = part.indexOf('=');
    if (i > 0 && part.slice(0, i).trim() === name) return decodeURIComponent(part.slice(i + 1).trim());
  }
  return null;
}
export const sessionCookie = (token, secure = true) =>
  `${COOKIE}=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${SESSION_DAYS * 86400}${secure ? '; Secure' : ''}`;
export const clearCookie = (secure = true) => `${COOKIE}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0${secure ? '; Secure' : ''}`;

// ---------- التحقق من الحقول (نفس قواعد الواجهة، والخادم هو الحكم) ----------
const normD = (v) => String(v ?? '').replace(/[٠-٩]/g, (d) => '٠١٢٣٤٥٦٧٨٩'.indexOf(d));
const clean = (v) => String(v ?? '').replace(/\s+/g, ' ').trim();
export const V = {
  name: (v) => !v ? 'اكتب اسمك' : /[0-9٠-٩]/.test(v) ? 'الاسم ما يكون فيه أرقام' : !/^[ء-يـa-zA-Z\s'-]+$/.test(v) ? 'الاسم يكون حروف بس، بدون رموز'
    : v.split(' ').length < 2 ? 'اكتب اسمك الأول واسم العائلة' : v.split(' ').some((w) => w.length < 2) ? 'كل جزء من الاسم لازم يكون حرفين أو أكثر' : v.length > 50 ? 'الاسم أطول من 50 حرف' : '',
  id: (v) => !v ? 'اكتب رقمك الوظيفي' : !/^\d+$/.test(v) ? 'الرقم الوظيفي أرقام بس' : v.length < 4 || v.length > 8 ? 'الرقم الوظيفي من 4 إلى 8 أرقام' : '',
  email: (v) => !v ? 'اكتب بريدك الإلكتروني' : /\s/.test(v) ? 'البريد ما يكون فيه مسافات' : v.length > 80 || !/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/.test(v) ? 'اكتب بريد صحيح، مثل name@company.sa' : '',
  text: (v) => !v ? 'اكتب مسماك الوظيفي' : /[0-9٠-٩]/.test(v) ? 'المسمى يكون كلام، بدون أرقام' : !/^[ء-يـa-zA-Z\s()\-]+$/.test(v) ? 'المسمى فيه رموز غير مقبولة' : v.length < 3 ? 'المسمى قصير' : v.length > 40 ? 'المسمى أطول من 40 حرف' : '',
  org: (v) => !v ? 'اكتب اسم المنشأة' : !/[ء-يa-zA-Z]{2}/.test(v) ? 'اسم المنشأة لازم يكون فيه حروف' : !/^[ء-يـa-zA-Z0-9\s&.()\-]+$/.test(v) ? 'اسم المنشأة فيه رموز غير مقبولة' : v.length > 60 ? 'الاسم أطول من 60 حرف' : '',
  dept: (v) => !['0', '1', '2'].includes(String(v)) ? 'اختر الإدارة' : '',
  gender: (v) => !['m', 'f'].includes(v) ? 'اختر الجنس' : '',
  nat: (v) => !['sa', 'other'].includes(v) ? 'اختر الجنسية' : '',
  num: (v, mn, mx) => !v ? 'اكتب الرقم' : !/^\d+$/.test(v) ? 'اكتب رقم صحيح بس، بدون حروف أو كسور' : +v < mn || +v > mx ? `الرقم لازم يكون بين ${mn} و${mx.toLocaleString('en-US')}` : '',
  password: (v) => !v ? 'اكتب كلمة المرور' : v.length < 8 ? 'كلمة المرور 8 أحرف أو أكثر' : v.length > 64 ? 'كلمة المرور أطول من 64 حرف' : !/[A-Za-zء-ي]/.test(v) || !/\d/.test(v) ? 'كلمة المرور لازم يكون فيها حروف وأرقام' : '',
};
// الحقول المطلوبة لكل دور: [المفتاح في الطلب، نوع التحقق، حد أدنى، حد أعلى]
export const ROLE_FIELDS = {
  emp: [['name', 'name'], ['eid', 'id'], ['email', 'email'], ['gender', 'gender'], ['nat', 'nat'], ['title', 'text'], ['dept', 'dept']],
  mgr: [['name', 'name'], ['eid', 'id'], ['email', 'email'], ['dept', 'dept'], ['team', 'num', 1, 200]],
  top: [['name', 'name'], ['eid', 'id'], ['email', 'email'], ['title', 'text']],
  haya: [['name', 'name'], ['eid', 'id'], ['email', 'email'], ['org', 'org'], ['count', 'num', 1, 100000]],
};
export function validateSignup(body) {
  const role = body.role;
  if (!ROLE_FIELDS[role]) return { errors: { role: 'اختر دورك' } };
  const out = { role }, errors = {};
  for (const [k, kind, mn, mx] of ROLE_FIELDS[role]) {
    let v = body[k];
    v = kind === 'id' || kind === 'num' ? normD(clean(v)) : kind === 'dept' || kind === 'gender' || kind === 'nat' ? String(v ?? '') : clean(v);
    if (kind === 'email') v = v.toLowerCase();
    const e = V[kind](v, mn, mx);
    if (e) errors[k] = e; else out[k] = v;
  }
  const pw = String(body.password ?? '');
  const pe = V.password(pw); if (pe) errors.password = pe;
  if (String(body.confirm ?? '') !== pw) errors.confirm = 'كلمتا المرور مو متطابقتين';
  out.password = pw;
  return Object.keys(errors).length ? { errors } : { data: out };
}
