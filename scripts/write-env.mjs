// يكتب site/env.js وقت البناء على Netlify من متغير البيئة DABRAH_API_BASE.
// إذا ما عرّفته، المنصة تشتغل على البيانات التجريبية (وضع العرض).
import { writeFileSync } from 'node:fs';
const base = process.env.DABRAH_API_BASE || '';
writeFileSync(new URL('../site/env.js', import.meta.url), `window.__ENV=${JSON.stringify({ API_BASE: base })};\n`);
console.log('env.js →', base ? `API_BASE=${base}` : 'وضع العرض (بيانات تجريبية)');
