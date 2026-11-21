import re
s=open('v3.html',encoding='utf8').read()
def rep(a,b,cnt=1):
    global s
    assert a in s, 'MISSING: '+a[:70]
    s=s.replace(a,b) if cnt==0 else s.replace(a,b,cnt)

# ---------- CSS ----------
css=r'''
/* rail */
.rail{position:fixed;inset-inline-end:18px;top:50%;transform:translateY(-50%);z-index:19;display:flex;flex-direction:column;gap:6px;padding:10px 8px;border-radius:999px;background:rgba(14,26,23,.55);backdrop-filter:blur(8px);box-shadow:0 8px 24px -10px rgba(0,0,0,.5)}
.rail a{position:relative;display:grid;place-items:center;width:28px;height:28px;border-radius:50%;text-decoration:none}
.rail a i{width:9px;height:9px;border-radius:50%;background:rgba(241,231,214,.45);transition:all .4s var(--ease)}
.rail a.on i{width:13px;height:13px;background:var(--sand);box-shadow:0 0 0 4px rgba(227,196,143,.25)}
.rail a span{position:absolute;inset-inline-end:38px;white-space:nowrap;background:var(--night);color:var(--jes);font-size:14px;padding:6px 12px;border-radius:999px;opacity:0;transform:translateX(-8px);pointer-events:none;transition:all .35s var(--ease);box-shadow:var(--shD)}
.rail a:hover span,.rail a:focus-visible span{opacity:1;transform:none}
.rail .bar{position:absolute;inset-inline-end:21px;top:16px;bottom:16px;width:2px;background:rgba(241,231,214,.12);z-index:-1;border-radius:2px}
.rail .bar b{display:block;width:100%;background:var(--sand);border-radius:2px;height:0;transition:height .3s}
@media(max-width:760px){.rail{inset-inline-end:6px;padding:8px 4px}.rail a{width:22px;height:22px}}
/* compare card */
.withd{background:linear-gradient(160deg,var(--night3),var(--night) 70%);color:var(--jes);border-radius:28px;padding:28px;box-shadow:var(--shD)}
.withd .it{display:flex;gap:14px;align-items:flex-start;padding:14px 0;border-top:1px solid rgba(241,231,214,.1)}
.withd .it:first-of-type{border-top:0}
.withd .ok{flex:none;width:34px;height:34px;border-radius:12px;background:var(--palm);display:grid;place-items:center}
.withd b{display:block;color:var(--sand)}
.withd span{color:#D9CFBE}
/* stairs */
.stairs{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;align-items:end;margin-top:50px}
.sc{display:flex;flex-direction:column}
.sc .step{min-height:168px;display:flex;flex-direction:column;border-radius:22px 22px 6px 6px}
.sc .base{background:var(--teen);border-radius:0 0 14px 14px;position:relative;transition:background .5s}
.sc .base::before{content:"";position:absolute;top:-1px;inset-inline:10%;height:10px;background:var(--teenD);clip-path:polygon(0 100%,0 60%,16% 60%,16% 30%,33% 30%,33% 0,67% 0,67% 30%,84% 30%,84% 60%,100% 60%,100% 100%);opacity:.5}
.sc.on .base{background:var(--teenD)}
@media(max-width:900px){.stairs{grid-template-columns:1fr;gap:10px}.sc .base{display:none}.sc .step{min-height:0;border-radius:22px}}
/* house levels */
.levels{display:flex;gap:10px;align-items:flex-end;justify-content:space-between;height:210px;margin:20px 0 12px}
.lv svg{overflow:visible}
.lv svg *{transition:fill .6s var(--ease),opacity .6s}
/* faq palm */
.qa summary::after{content:none}
.qa .pi{flex:none;width:34px;height:34px;transition:transform .5s var(--ease)}
.qa details[open] .pi{transform:scale(1.25) rotate(-8deg)}
.qa details[open] summary{color:var(--teenD)}
/* glow */
.glow{color:var(--sand);text-shadow:0 0 18px rgba(227,196,143,.55),0 0 46px rgba(227,196,143,.35),0 0 90px rgba(164,100,60,.35);animation:pulse 3.2s ease-in-out infinite}
@keyframes pulse{0%,100%{text-shadow:0 0 14px rgba(227,196,143,.45),0 0 36px rgba(227,196,143,.25),0 0 70px rgba(164,100,60,.25)}50%{text-shadow:0 0 22px rgba(227,196,143,.8),0 0 60px rgba(227,196,143,.5),0 0 110px rgba(164,100,60,.45)}}
.meaning{white-space:pre-line}
/* login */
#login{min-height:100vh;background:radial-gradient(120% 80% at 50% 0%,var(--night3),var(--night) 60%);color:var(--jes)}
.lwrap{max-width:900px;margin:0 auto;padding:40px max(4vw,16px) 60px}
.lroles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:28px}
@media(max-width:760px){.lroles{grid-template-columns:1fr}}
.lrole{background:var(--night2);border:1.5px solid rgba(241,231,214,.1);border-radius:26px;padding:24px 20px;text-align:start;color:var(--jes);box-shadow:var(--shD);transition:transform .45s var(--ease),border-color .4s,background .4s;display:flex;flex-direction:column;gap:10px;min-height:190px}
.lrole:hover,.lrole:focus-visible{transform:translateY(-6px);border-color:var(--sand);background:#1A3027}
.lrole .ri{width:54px;height:54px;border-radius:18px;background:var(--teen);display:grid;place-items:center}
.lrole b{font:800 21px 'Kufam'}
.lrole span{color:#C3B8A6;font-size:15px}
.lform{background:var(--card);color:var(--ink);border-radius:28px;padding:clamp(20px,3vw,32px);margin-top:26px;box-shadow:var(--shD)}
.fgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px 18px}
@media(max-width:640px){.fgrid{grid-template-columns:1fr}}
.fld label{display:block;font-weight:700;margin:12px 0 6px}
.fld input,.fld select{width:100%;min-height:50px;border:1.5px solid var(--line);border-radius:14px;padding:0 14px;font-size:16px;background:#fff;color:var(--ink)}
.fld input:focus,.fld select:focus{outline:none;border-color:var(--teen);box-shadow:0 0 0 4px rgba(164,100,60,.15)}
.fld .err{color:#A33A16;font-size:13.5px;min-height:20px;display:block}
.fld.bad input{border-color:#C0502A}
'''
rep('</style>',css+'</style>')

# ---------- logo ----------
rep('__LOGO_J__','__LOGO3__',0)

# ---------- nav + hero CTAs ----------
rep('<a class="btn" href="#app" style="min-height:44px;padding:0 20px">جرّب دبره</a>','<a class="btn" href="#login" style="min-height:44px;padding:0 20px">تسجيل الدخول</a>')
rep('<a class="btn" href="#app">جرّب البروتوتايب</a>','<a class="btn" href="#login">تسجيل الدخول</a>')
rep('<a href="#story">المشكلة</a><a href="#how">كيف تشتغل</a><a href="#palm">نخلتك</a><a href="#impact">الأثر</a>','<a href="#story">المشكلة</a><a href="#how">كيف تشتغل</a><a href="#palm">نخلتك</a><a href="#impact">الأثر</a>')

# ---------- rail ----------
rail='''<nav class="rail" id="rail" aria-label="أقسام الصفحة"><div class="bar"><b id="railbar"></b></div>
<a href="#top" data-s="top"><i></i><span>البداية</span></a><a href="#story" data-s="story"><i></i><span>المشكلة</span></a><a href="#name" data-s="name"><i></i><span>معنى الاسم</span></a><a href="#how" data-s="how"><i></i><span>كيف تشتغل</span></a><a href="#try" data-s="try"><i></i><span>المستويات وعمر المهارة</span></a><a href="#palm" data-s="palm"><i></i><span>نخلتك</span></a><a href="#faq" data-s="faq"><i></i><span>أسئلة الحزمة</span></a><a href="#impact" data-s="impact"><i></i><span>الأثر</span></a><a href="#final" data-s="final"><i></i><span>صِر دبره</span></a></nav>
'''
rep('<header class="hero" id="top">',rail+'<header class="hero" id="top">')

# ---------- story: replace persona with "with dabrah" ----------
a=s.index('<div class="persona reveal">');b=s.index('<div class="wrap stats">')
ok='<div class="ok"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L19 7"/></svg></div>'
withd=f'''<div class="withd reveal">
      <div class="eyebrow" style="color:var(--sand)">ومع دبره</div>
      <h3 style="font-size:26px;margin-bottom:10px">كل وحدة لها حل</h3>
      <div class="it">{ok}<div><b>طريق ترقية واضح</b><span>يعرف خطوته الجاية بالضبط، ووش ناقصه للدرجة اللي بعدها.</span></div></div>
      <div class="it">{ok}<div><b>كل مهارة لها دليل</b><span>يثبتها بتحدي من شغله، ويعتمدها مديره بضغطة.</span></div></div>
      <div class="it">{ok}<div><b>ذكاء اصطناعي بأمان</b><span>سياسة شركته قدامه داخل كل تحدي، فيستخدمه وهو مطمئن.</span></div></div>
    </div>
  </div>
  '''
s=s[:a]+withd+s[b:]
rep('<b>موظف تسأل هيا كيف تطوّرهم بميزانية محدودة</b><div class="src">من شخصيات حزمة التحدي</div>','<b>موظف ميداني تحتاج هيا تطوّرهم بميزانية محدودة</b><div class="src">من شخصيات حزمة التحدي</div>')

# ---------- name meaning ----------
rep('''<p class="meaning" id="meaning" aria-live="polite">في نجد يقولون «فلان دبره» عن الشخص السنع اللي يتدبّر أموره ويُعتمد عليه. وما يقولونها على عمره ولا شهاداته... يقولونها يوم يشوفونه يشتغل.</p>''','''<p class="meaning" id="meaning" aria-live="polite">في نجد يقولون «فلان دبره» عن الشخص السنع اللي يتدبّر أموره ويُعتمد عليه.
وما يقولونها على عمره ولا شهاداته... يقولونها يوم يشوفونه يشتغل.</p>''')
a=s.index("const MEAN=[");b=s.index("];",a)+2
s=s[:a]+r"""const MEAN=['الدال من «دبّر»، يعني تصرّف بحكمة.\nالدبره يعرف وش ناقصه ويروح يكمّله.\nوهذي خريطة الفجوة.','الباء من «باب».\nكل مهارة تثبتها تفتح لك باب.\nوالترقية الجاية باب ينفتح بسنعك.','الراء من «رُقي».\nخمس درجات من مبتدي إلى ذيب.\nوكل درجة ما تنكسب إلا بإثبات.','الهاء عينها كوّة نجدية.\nمنها تطل على السوق وتعرف وش المطلوب قبل غيرك.'];"""+s[b:]

# ---------- steps -> stairs ----------
a=s.index('<div class="steps" id="steps">');b=s.index('</section>',a)
steps=[('اعرف خطوتك','خريطة الفجوة من سلّم شركتك'),('تعلّم','محتوى قصير مربوط بمهامك'),('أثبت','تحدي من شغلك الحقيقي'),('يعتمدك مديرك','الذكاء الاصطناعي يقترح، والمدير يقرر'),('تترقى','المهارة تنحسب في ملفك'),('حافظ عليها','عمر المهارة يذكّرك تجددها')]
cols=''.join(f'<div class="sc"><div class="step"><div class="k">{i+1}</div><b>{t}</b><span>{d}</span></div><div class="base" style="height:{14+i*22}px"></div></div>' for i,(t,d) in enumerate(steps))
s=s[:a]+f'<div class="stairs" id="steps">{cols}</div>\n  </div>\n'+s[b:]
rep("$$('#steps .step').forEach((s,i)=>s.classList.toggle('on',i<n))","$$('#steps .sc').forEach((s,i)=>{s.classList.toggle('on',i<n);s.querySelector('.step').classList.toggle('on',i<n)})")

# ---------- try: remove renew demo ----------
rep('''        <button class="btn sand" id="renewDemo" style="margin-top:6px">تحدي تجديد 10 دقائق</button>\n''','')
rep(";$('#renewDemo').onclick=()=>{$('#age').value=0;age();toast('تجددت المهارة، ورجعت خضراء')};",";")
rep("'قرب موعد التجديد. بنبهك قبلها بشهر.'","'قرّب موعد التجديد، وبننبّهك قبلها بشهر.'")
rep("'نزلت درجة من سنع إلى شاطر. تحدي قصير يرجعها.'","'نزلت درجة من سنع إلى شاطر، وتحدي قصير يرجّعها.'")
rep("'ممتاز، المهارة شغالة.'","'ممتاز، المهارة شغّالة.'",0)

# house levels
a=s.index("let lvl=3;function drawLv(){");b=s.index("$('#lvUp').onclick")
s=s[:a]+r"""let lvl=3;
function house(i,on){const W=60,H=56+i*30,top=12,c=on?'#A4643C':'#2A3F35',d=on?'#7E4626':'#22352C',w=on?'#F3C86B':'#3A5146';let o=`<svg width="${W}" height="${H+top+8}" viewBox="0 0 ${W} ${H+top+8}" aria-hidden="true"><ellipse cx="${W/2}" cy="${H+top+4}" rx="${W/2}" ry="4" fill="rgba(0,0,0,.3)"/><rect x="2" y="${top}" width="${W-4}" height="${H}" fill="${c}"/><rect x="${W-12}" y="${top}" width="10" height="${H}" fill="${d}" opacity=".55"/>`;
 for(let k=0;k<3;k++){const x=4+k*18,st=2.6;o+=`<path d="M${x} ${top} v-4 h${st} v-4 h${st} v-4 h${st*2} v4 h${st} v4 h${st} v4Z" fill="${c}"/>`}
 for(let k=0;k<4;k++)o+=`<rect x="${6+k*14}" y="${top+8}" width="5" height="4" fill="#4A2B17"/>`;
 o+=`<rect x="2" y="${top+14}" width="${W-4}" height="2" fill="${d}"/>`;
 const rows=Math.min(3,1+Math.floor(i/1.4));for(let r=0;r<rows;r++)for(let q=0;q<=r;q++){const t=7,cx=W/2+(q-r/2)*(t+3),cy=top+24+r*(t*.9+3);o+=`<polygon points="${cx-t/2},${cy+t*.9} ${cx},${cy} ${cx+t/2},${cy+t*.9}" fill="${w}"/>`}
 if(i>=2){const y2=top+H*.62;for(let q=0;q<2;q++){const t=6,cx=W/2+(q?12:-12);o+=`<polygon points="${cx-t/2},${y2+t*.9} ${cx},${y2} ${cx+t/2},${y2+t*.9}" fill="${w}" opacity=".9"/>`}}
 o+=`<rect x="${W/2-7}" y="${top+H-24}" width="14" height="24" rx="1" fill="${on?'#2F6B60':'#1C2D26'}"/><polygon points="${W/2-3},${top+H-14} ${W/2},${top+H-19} ${W/2+3},${top+H-14}" fill="${on?'#F1E7D6':'#3A5146'}"/>`;
 return o+'</svg>'}
function drawLv(){let o='';for(let i=0;i<5;i++)o+=`<div class="lv">${house(i,i<lvl)}<span ${i===lvl-1?'style="color:#fff;font-weight:700"':''}>${LV[i]}</span></div>`;$('#levels').innerHTML=o;$('#lvname').textContent=LV[lvl-1];$('#lvDown').disabled=lvl<=1;$('#lvUp').disabled=lvl>=5;$('#lvUp').textContent=lvl>=5?'وصلت ذيب!':'أثبت تحدي'}
"""+s[b:]

# ---------- palm ----------
a=s.index("function palmSVG(fr){");b=s.index("const stageOf=")
s=s[:a]+r"""function palmSVG(fr){
  const st=stageOf(fr),H=[70,130,180,215][st],L=[40,56,68,78][st],n=[7,9,11,13][st];
  const cx=150,base=318,top=base-H;
  let o=`<svg viewBox="0 0 300 330" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><ellipse cx="150" cy="320" rx="${40+st*14}" ry="6" fill="rgba(0,0,0,.22)"/>`;
  o+=`<path d="M${cx-8} ${base} Q${cx-5} ${top+H*.45} ${cx-3} ${top} L${cx+3} ${top} Q${cx+5} ${top+H*.45} ${cx+8} ${base}Z" fill="#8A5A35"/>`;
  for(let y=base-8,k=0;y>top+6;y-=9,k++){const w=8-(base-y)/H*5;o+=`<path d="M${cx-w} ${y} L${cx} ${y-5} L${cx+w} ${y}" stroke="#6B4126" stroke-width="1.6" fill="none"/>`}
  o+=`<g class="sway" style="transform-origin:${cx}px ${top}px">`;
  const fronds=[];for(let i=0;i<n;i++){const t=i/(n-1);const ang=(-180+t*180)*Math.PI/180;fronds.push(ang)}
  fronds.sort((p,q)=>Math.abs(Math.sin(q))-Math.abs(Math.sin(p)));
  fronds.forEach((a,i)=>{const up=Math.abs(Math.sin(a));const len=L*(.75+.25*(1-up*.4));const ex=cx+Math.cos(a)*len,ey=top-up*len*.55+(1-up)*len*.45;const mx=cx+Math.cos(a)*len*.5,my=top-up*len*.6-len*.12;const g=i%2?'#4C8A5E':'#3E7652';
    o+=`<path d="M${cx} ${top} Q${mx.toFixed(1)} ${(my-5).toFixed(1)} ${ex.toFixed(1)} ${ey.toFixed(1)} Q${mx.toFixed(1)} ${(my+5).toFixed(1)} ${cx} ${top+3}Z" fill="${g}"/><path d="M${cx} ${top+1} Q${mx.toFixed(1)} ${my.toFixed(1)} ${ex.toFixed(1)} ${ey.toFixed(1)}" stroke="#2F5E42" stroke-width="1" fill="none"/>`});
  if(st===3)[-1,1].forEach(sd=>{for(let j=0;j<6;j++)o+=`<circle cx="${cx+sd*13+(j%2?3:-3)*sd}" cy="${top+9+j*4}" r="3.6" fill="${j%2?'#C0702F':'#D98B3E'}"/>`});
  o+=`<circle cx="${cx}" cy="${top+1}" r="5" fill="#5B3A22"/>`;
  return o+'</g></svg>';
}
"""+s[b:]

# ---------- FAQ ----------
rep('<section class="sec light" style="padding-top:0">','<section class="sec light" id="faq" style="padding-top:0">')
pal='<svg class="pi" viewBox="0 0 40 40" aria-hidden="true"><path d="M19 38 Q18.5 26 19.5 16 L21 16 Q22 26 22 38Z" fill="#8A5A35"/><g fill="#4C8A5E"><path d="M20 16 Q12 9 4 14 Q12 12 20 17Z"/><path d="M20 16 Q28 9 36 14 Q28 12 20 17Z"/><path d="M20 16 Q15 6 9 5 Q16 9 20 17Z"/><path d="M20 16 Q25 6 31 5 Q24 9 20 17Z"/><path d="M20 16 Q20 7 20 2 Q21 9 20.5 16Z"/></g></svg>'
s=re.sub(r'(<summary>)([^<]+)(</summary>)',lambda m:m.group(1)+'<span>'+m.group(2)+'</span>'+pal+m.group(3),s)

# ---------- final ----------
rep('<section class="sec final">','<section class="sec final" id="final">')
rep('<h2 class="reveal">صِر دبره</h2>','<h2 class="reveal glow">صِر دبره</h2>')
rep('<p class="sub reveal" style="margin:16px auto 28px">ادخل كأنك عبدالله، حل تحدي، وخل محمد يعتمدك.</p>\n    <a class="btn reveal" href="#app">ادخل البروتوتايب</a>','<p class="sub reveal" style="margin:16px auto 28px">سجّل دخولك، وحل أول تحدي، وخلّ مديرك يعتمدك.</p>\n    <a class="btn reveal" href="#login">تسجيل الدخول</a>')

# ---------- landing palm start ----------
open('v3.html','w',encoding='utf8').write(s)
print('ok')
