# v11 → team footer «صُنّاع دبره» on landing, login and app (addition only; nothing else restyled)
import re
P = '/home/claude/proto/v11.html'
s = open(P, encoding='utf8').read()
assert 'data-team' not in s, 'already patched'

CSS = '''/* v13: فوتر الفريق «صُنّاع دبره» في كل الواجهات */
.teamf{--tf-bg:transparent;--tf-ink:var(--jes);--tf-mut:#BFB4A2;--tf-card:rgba(241,231,214,.05);--tf-line:rgba(241,231,214,.1);--tf-chip:rgba(241,231,214,.08);padding:44px max(5vw,18px) 34px;color:var(--tf-ink);border-top:1px solid var(--tf-line)}
.teamf.lt{--tf-ink:var(--ink);--tf-mut:var(--mut);--tf-card:var(--card);--tf-line:var(--line);--tf-chip:#F3E9DA;margin-top:28px}
.teamf .tf-in{max-width:1180px;margin:0 auto}
.teamf .tf-head{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:8px 24px;margin-bottom:22px}
.teamf .tf-eb{font-size:13px;font-weight:700;letter-spacing:.02em;color:var(--teenL)}
.teamf.lt .tf-eb{color:var(--teenD)}
.teamf h2{font-size:clamp(24px,3vw,32px);margin-top:4px;color:var(--tf-ink)}
.teamf .tf-sub{margin:6px 0 0;color:var(--tf-mut);font-size:15px}
.teamf .tf-grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}
.teamf .tf-m{position:relative;display:flex;flex-direction:column;gap:10px;background:var(--tf-card);border:1px solid var(--tf-line);border-radius:22px;padding:18px 16px 16px;transition:transform .35s var(--ease),border-color .35s,box-shadow .35s}
.teamf.lt .tf-m{box-shadow:var(--sh)}
.teamf .tf-m:hover{transform:translateY(-3px);border-color:var(--teenL)}
.teamf .tf-top{display:flex;align-items:center;gap:12px;min-width:0}
.teamf .tf-av{flex:none;width:46px;height:46px;border-radius:50%;display:grid;place-items:center;font-family:'Kufam','IBM Plex Sans Arabic',sans-serif;font-weight:700;font-size:20px;color:#fff;background:linear-gradient(145deg,var(--teenL),var(--teen) 55%,var(--teenD));box-shadow:inset 0 -3px 0 rgba(0,0,0,.15)}
.teamf .tf-nm{min-width:0}
.teamf .tf-nm b{display:block;font-family:'Kufam','IBM Plex Sans Arabic',sans-serif;font-size:17px;line-height:1.3;color:var(--tf-ink)}
.teamf .tf-lead{display:inline-flex;align-items:center;gap:5px;margin-top:3px;font-size:12px;font-weight:700;color:#4A2C05;background:var(--sand);border-radius:999px;padding:2px 10px}
.teamf .tf-lead svg{width:13px;height:13px}
.teamf .tf-roles{display:flex;flex-wrap:wrap;gap:6px}
.teamf .tf-roles span{font-size:12.5px;font-weight:600;border-radius:999px;padding:3px 10px;background:var(--tf-chip);color:var(--tf-ink)}
.teamf .tf-li{margin-top:auto;display:inline-flex;align-items:center;gap:8px;align-self:flex-start;min-height:40px;padding:0 14px;border-radius:999px;font-size:14px;font-weight:700;text-decoration:none;color:var(--tf-ink);border:1px solid var(--tf-line);transition:background .25s,color .25s,border-color .25s}
.teamf .tf-li svg{width:18px;height:18px;flex:none}
.teamf .tf-li:hover{background:#0A66C2;border-color:#0A66C2;color:#fff}
.teamf .tf-li:focus-visible{outline:3px solid var(--sand);outline-offset:2px}
.teamf .tf-no{margin-top:auto;font-size:13px;color:var(--tf-mut);min-height:40px;display:flex;align-items:center}
.teamf .tf-foot{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;margin-top:22px;padding-top:16px;border-top:1px solid var(--tf-line);font-size:13px;color:var(--tf-mut)}
.teamf .tf-palms{display:inline-flex;gap:4px;vertical-align:middle;margin-inline-start:6px}
.teamf .tf-palms svg{width:14px;height:18px}
@media(max-width:560px){.teamf .tf-grid{grid-template-columns:1fr 1fr}.teamf .tf-m{padding:14px 12px}.teamf .tf-av{width:40px;height:40px;font-size:18px}.teamf .tf-nm b{font-size:15px}}
@media(max-width:380px){.teamf .tf-grid{grid-template-columns:1fr}}
#landing .teamf .tf-foot{display:none}
@media(prefers-reduced-motion:reduce){.teamf .tf-m,.teamf .tf-li{transition:none}.teamf .tf-m:hover{transform:none}}
'''
anchor = '.fld .calsw label:has(input:focus-visible){outline:3px solid var(--sand);outline-offset:2px}\n</style>'
assert anchor in s
s = s.replace(anchor, anchor.replace('</style>', CSS + '</style>'))

# placeholders: landing (above the existing footer line), login (bottom), app (after the demo note)
a = '<footer><span>دبره · مهاراثون 2026'
assert s.count(a) == 1
s = s.replace(a, '<section class="teamf" data-team aria-label="فريق دبره"></section>\n' + a)
b = '  <div class="lwrap" id="lbox"></div>\n</div>'
assert s.count(b) == 1
s = s.replace(b, '  <div class="lwrap" id="lbox"></div>\n  <section class="teamf" data-team aria-label="فريق دبره"></section>\n</div>')
c = '  <p class="demo">بيانات تجريبية · مستودعات الشرق اسم تجريبي</p>\n</div>'
assert s.count(c) == 1
s = s.replace(c, '  <p class="demo">بيانات تجريبية · مستودعات الشرق اسم تجريبي</p>\n  <section class="teamf lt" data-team aria-label="فريق دبره"></section>\n</div>')

JS = r'''/* v13: فريق دبره — يُرسم في فوتر كل الواجهات */
const TEAM=[
 {n:'جنا السعيد',lead:true,r:['التصميم','العرض','البناء'],li:'https://www.linkedin.com/in/'+encodeURIComponent('جنا-السعيـد-jana-alsaeed-b26583340')},
 {n:'لارا الفريح',r:['البحث','نموذج العمل','التصميم'],li:'https://www.linkedin.com/in/laraalfurayh'},
 {n:'عبير السدحان',r:['البحث','العرض التقديمي','البناء'],li:'https://www.linkedin.com/in/alsadhan'},
 {n:'ساره الجريبه',r:['قواعد البيانات والاستضافة','البناء'],li:'https://www.linkedin.com/in/sara-aljuraybah-aa746227a'},
 {n:'ميس السويكت',r:['البحث','نموذج العمل','البناء'],li:''}
];
(function(){
 const LI='<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="1.5" y="1.5" width="21" height="21" rx="5" fill="#0A66C2"/><path fill="#fff" d="M6.6 9.6h2.6v8H6.6zM7.9 5.7a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3zM10.9 9.6h2.5v1.1c.4-.7 1.3-1.3 2.6-1.3 2.7 0 3.2 1.7 3.2 4v4.2h-2.6v-3.7c0-.9 0-2-1.3-2s-1.5 1-1.5 2v3.7h-2.6z"/></svg>';
 const CROWN='<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#7E4626" d="M3 7l4.5 4L12 4l4.5 7L21 7l-2 11H5z"/></svg>';
 const PALM='<svg viewBox="0 0 14 18" aria-hidden="true"><path d="M7 7v11" stroke="#7E4626" stroke-width="1.6"/><path fill="#4C8A5E" d="M7 7C5 3 2 3 0 4c3 0 5 1 7 3zm0 0c2-4 5-4 7-3-3 0-5 1-7 3zM7 7C6 4 7 1 7 0c0 1 1 4 0 7z"/></svg>';
 const first=n=>n.trim().charAt(0);
 const html=`<div class="tf-in"><div class="tf-head"><div><div class="tf-eb">فريق دبره · مهاراثون 2026</div><h2>صُنّاع دبره</h2><p class="tf-sub">خمسة أشخاص، وكل وحدة فيهم دبره في مجالها.</p></div></div>
 <ul class="tf-grid">${TEAM.map(m=>`<li class="tf-m"><div class="tf-top"><span class="tf-av" aria-hidden="true">${first(m.n)}</span><div class="tf-nm"><b>${m.n}</b>${m.lead?`<span class="tf-lead">${CROWN}قائدة الفريق</span>`:''}</div></div>
 <div class="tf-roles">${m.r.map(x=>`<span>${x}</span>`).join('')}</div>
 ${m.li?`<a class="tf-li" href="${m.li}" target="_blank" rel="noopener noreferrer" aria-label="حساب ${m.n} في لينكدإن (يفتح في نافذة جديدة)">${LI}لينكدإن</a>`:''}</li>`).join('')}</ul>
 <div class="tf-foot"><span>دبره · المسار الأول: الكفاءات الوطنية ومستقبل العمل · السؤال 1.2 «مسيرة للمستقبل»<span class="tf-palms" aria-hidden="true">${PALM}${PALM}${PALM}</span></span><span>© 2026 فريق دبره</span></div></div>`;
 document.querySelectorAll('[data-team]').forEach(el=>{el.innerHTML=html});
})();
'''
d = 'window.DABRAH={S,API,ACT,readyOf,loadOf,CONFIG};'
assert s.count(d) == 1
s = s.replace(d, JS + d)
open(P, 'w', encoding='utf8').write(s)
print('ok', len(s))
