import re,sys
P='/home/claude/proto/v8.html'
s=open(P,encoding='utf8').read()
def R(old,new,cnt=1):
    global s
    n=s.count(old)
    if n!=cnt: sys.exit(f'COUNT {n}!={cnt} for: {old[:90]}')
    s=s.replace(old,new)

# ---------- 0. remove duplicated old event wiring ----------
a=s.index("$('#tbtn').onclick")
b=s.index("/* =====================================================================\n   API LAYER")
assert a<b and s.count("$('#tbtn').onclick")==2
s=s[:a]+"\n"+s[b:]

# ---------- 1. CSS ----------
CSS=r"""
/* v8 */
.crits .crit{justify-content:flex-start}.crit>div{flex:1;min-width:0;text-align:start}
.dprog{padding:14px 24px 12px;border-bottom:1px solid var(--line)}
textarea.bad{border-color:#C0502A}
.fld .hint{display:block;color:var(--mut);font-size:13px;margin-top:4px}
.fld input[dir=ltr]{text-align:left}
.lform .lacts{display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;align-items:center;margin-top:18px}
.lform .lacts .grp{display:flex;gap:10px;flex-wrap:wrap}
.fillbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;background:#F7EFE2;border-radius:16px;padding:10px 14px;margin-bottom:6px}
.fillbar span{font-size:14px;color:var(--mut)}
.myreg{display:grid;gap:8px;margin-top:10px}
.myreg .ri2{display:flex;align-items:center;gap:12px;background:#F7EFE2;border-radius:14px;padding:10px 14px}
.myreg .ri2>div{flex:1;min-width:0}.myreg .ri2 b{display:block;font-size:15px}
.myreg .tag{font-size:12px;font-weight:700;border-radius:999px;padding:3px 10px;background:#E6F1EA;color:var(--ok);flex:none}
.myreg .tag.c{background:#F3E6D6;color:var(--teenD)}
.kx{display:grid;gap:8px}.kx div{background:#F7EFE2;border-radius:14px;padding:10px 14px;text-align:start}.kx b{display:block;font-size:15px}.kx span{display:block;font-size:14px;color:var(--mut)}
.rotfx{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}.rotfx span{font-size:12.5px;border-radius:999px;padding:3px 10px;background:#fff;border:1px solid var(--line)}
.ctype{border-top:1px solid var(--line)}.ctype>summary{padding:14px 4px}
.ctype .skill:first-child{border-top:0}
.tsum{font-weight:800;color:var(--teenD)}
.wgrp{display:grid;gap:12px;padding-top:4px}
.tyrow{display:grid;grid-template-columns:minmax(0,1fr) 120px 70px;gap:10px;align-items:center;padding:8px 0;border-top:1px solid rgba(241,231,214,.12);font-size:14px}
.tyrow .prog{height:6px}
@media(max-width:560px){.tyrow{grid-template-columns:minmax(0,1fr) 70px}.tyrow .prog{display:none}}
"""
i=s.index('</style>');s=s[:i]+CSS+s[i:]

# ---------- 2. competencies: 4 types ----------
R("const SK={cap:{n:'تخطيط الطاقة الاستيعابية',t:'فنية',req:3},ai:{n:'تقارير الأداء بالذكاء الاصطناعي',t:'فنية',req:3},inv:{n:'إدارة المخزون',t:'فنية',req:4},lead:{n:'قيادة فريق المستودع',t:'قيادية',req:3},xl:{n:'Excel',t:'فنية',req:3}};",
"""const TYPES=[['فنية','تُثبت بالتحديات والشهادات المطبّقة'],['سلوكية','تُقاس بتقييم 360 من زملاء يختارهم النظام'],['قيادية','تُقاس بتقييم 360 ومواقف قيادية فعلية'],['جوهرية','قيم المنشأة، تُقاس من مؤشرات الأداء والالتزام']];
const SK={cap:{n:'تخطيط الطاقة الاستيعابية',t:'فنية',req:3},ai:{n:'تقارير الأداء بالذكاء الاصطناعي',t:'فنية',req:3},inv:{n:'إدارة المخزون',t:'فنية',req:4},xl:{n:'Excel',t:'فنية',req:3},fc:{n:'التنبؤ بالطلب',t:'فنية',req:3},
 com:{n:'التواصل الفعّال',t:'سلوكية',req:3},team:{n:'العمل الجماعي',t:'سلوكية',req:3},prob:{n:'حل المشكلات',t:'سلوكية',req:3},
 lead:{n:'قيادة فريق المستودع',t:'قيادية',req:3},dec:{n:'اتخاذ القرار بالبيانات',t:'قيادية',req:3},dev:{n:'تطوير الآخرين ونقل المعرفة',t:'قيادية',req:3},
 safe:{n:'السلامة والجودة',t:'جوهرية',req:3},cust:{n:'التوجه بالعميل',t:'جوهرية',req:3},integ:{n:'النزاهة وحماية البيانات',t:'جوهرية',req:3}};""")
R("W:{cap:30,ai:25,inv:20,lead:15,xl:10}","W:{cap:15,ai:10,inv:10,xl:5,fc:5,com:6,team:6,prob:8,lead:8,dec:7,dev:5,safe:5,cust:5,integ:5}")
R("بوزن 25%'","بوزن 10%'")
R("const readyOf=i=>{let t=0,w=0;for(const k in S.W){const req=SK[k].req;const L=k==='xl'?((i===0?S.excel:EMP[i].xl)==='g'?3:2):lvOf(i,k);t+=S.W[k]*Math.min(1,L/req);w+=S.W[k]}return Math.round(t/w*100)};",
"""const cl=v=>Math.max(1,Math.min(5,Math.round(v)));
/* الجدارات غير الفنية مشتقة من مصادرها: 360 والأداء والأدلة الفنية */
const DER={fc:i=>cl(lvOf(i,'cap')+1),com:i=>cl(EMP[i].b360-1),team:i=>cl(EMP[i].b360+.2-1),prob:i=>cl(EMP[i].b360-.3-1),dec:i=>cl((lvOf(i,'ai')+lvOf(i,'cap'))/2),dev:i=>cl(lvOf(i,'lead')-1),safe:i=>cl(EMP[i].perf+1),cust:i=>cl(EMP[i].perf+(EMP[i].b360>=4?1:0)),integ:i=>3+(EMP[i].perf===3?1:0)};
const xlOk=i=>(i===0?S.excel:EMP[i].xl)==='g';
const compLv=(i,k)=>k==='xl'?(xlOk(i)?3:2):DER[k]?DER[k](i):lvOf(i,k);
const dispLv=(i,k)=>k==='xl'?3:compLv(i,k);
const readyOf=i=>{let t=0,w=0;for(const k in S.W){t+=S.W[k]*Math.min(1,compLv(i,k)/SK[k].req);w+=S.W[k]}return w?Math.round(t/w*100):0};
const typeStat=(i,ty)=>{const ks=Object.keys(SK).filter(k=>SK[k].t===ty);return {n:ks.length,met:ks.filter(k=>compLv(i,k)>=SK[k].req).length,w:ks.reduce((a,k)=>a+(S.W[k]||0),0)}};""")

# rotation-aware workload
R("const loadOf=i=>Math.round(EMP[i].hrs/40*100);",
"""/* التدوير: [المفتاح، المستلم، المعطي، الساعات الأسبوعية المنقولة، العنوان، الأثر] */
const ROT=[['r1',5,1,10,'خالد المطيري يتدوّر 3 شهور مع ماجد في نظام إدارة المستودع','يخفف ضغط ماجد، ويكسر احتكار المعرفة'],['r2',3,6,6,'سلطان العتيبي ينتقل شهرين لمنطقة التبريد مع عمر','يتعلم مهارة حرجة، ويرفع أدلته الفنية'],['r3',2,0,5,'عبدالله الشمري يسلّم تقرير الخميس لفهد','يوازن العبء ويطوّر فهد في التقارير']];
const hrsOf=i=>EMP[i].hrs+ROT.reduce((a,[k,to,fr,h])=>a+(S.rot[k]?(i===to?h:i===fr?-h:0):0),0);
const loadOf=i=>Math.round(hrsOf(i)/40*100);""")

# skList -> all competencies
R("""{id:'xl',c:3,h:S.excel,d:S.excel==='g'?'اليوم':'قبل 11 شهر',plan:S.excel==='g'?'تجددت. التذكير الجاي بعد سنة.':'ما استخدمتها من 11 شهر، ومستواها ينزل بعد 12 يوم.'}].map(s=>({...s,...SK[s.id],w:S.W[s.id]}))};""",
"""{id:'xl',c:3,h:S.excel,d:S.excel==='g'?'اليوم':'قبل 11 شهر',plan:S.excel==='g'?'تجددت. التذكير الجاي بعد سنة.':'ما استخدمتها من 11 شهر، ومستواها ينزل بعد 12 يوم.'},
 ...['fc','com','team','prob','dec','dev','safe','cust','integ'].map(k=>{const c=compLv(0,k),ok=c>=SK[k].req;return {id:k,c,h:'g',d:{fc:'مشتقة من تخطيط الطاقة',dec:'مشتقة من تقاريرك وتخطيطك',dev:'من 360 وجلسات نقل المعرفة'}[k]||(SK[k].t==='سلوكية'?'تقييم 360 قبل شهر':'من مؤشرات أدائك'),plan:ok?'وصلت المطلوب.':{fc:'ترتفع تلقائيًا لما ترتفع في تخطيط الطاقة الاستيعابية.',dec:'ترتفع لما تثبت تقارير الأداء وتخطيط الطاقة.'}[k]||'تتحسن من تقييم 360 الجاي ومؤشرات أدائك.'}})].map(s=>({...s,...SK[s.id],w:S.W[s.id]}))};
const jd=n=>n===1?'جدارة وحدة':n===2?'جدارتين':n<=10?n+' جدارات':n+' جدارة';""")
R("${rem?`باقي لك ${['','مهارة وحدة','مهارتين','ثلاث مهارات','أربع مهارات'][rem]} وتكون جاهز للترقية.`:'أنت جاهز للترقية!'}",
  "${rem?`باقي لك ${jd(rem)} وتكون جاهز للترقية.`:'أنت جاهز للترقية!'}")
# group the skills list by type
old_sk=s[s.index("  ${skList().map(s=>`<div class=\"skill"):]
old_sk=old_sk[:old_sk.index("</div></div></div></div>`).join('')}")+len("</div></div></div></div>`).join('')}")]
new_sk=old_sk.replace("${skList().map(s=>","${TYPES.map(([ty,how],ti)=>{const L=skList().filter(x=>x.t===ty);const st=typeStat(0,ty);return disc(`<b>${ty}</b> <span class=\"mut\">· وزنها ${st.w}% · ${st.met} من ${st.n} توصل المطلوب</span>`,`<p class=\"mut small\" style=\"margin:0 0 4px\">${how}</p>`+L.map(s=>").replace("</div></div></div></div>`).join('')}","</div></div></div></div>`).join(''),ti===0?'open':'')}).join('')}")
s=s.replace(old_sk,new_sk,1)

# palm summary grouped
a=s.index("function palmSummary(i){");b=s.index("\n",a)
s=s[:a]+"""function palmSummary(i){const f=i===0?S.fr:EMP[i].fr,rd=readyOf(i),g=grpOf(rd);
 const rows=TYPES.map(([ty])=>{const st=typeStat(i,ty);return `<div class="tyrow"><span><b>${ty}</b> <span class="mut" style="color:#C3B8A6">· ${st.w}%</span></span>${bar(st.met/st.n*100)}<span class="mut" style="color:#C3B8A6">${st.met} من ${st.n}</span></div>`}).join('');
 const all=Object.keys(SK).map(k=>{const L=dispLv(i,k);const h=k==='xl'?(xlOk(i)?'محدّثة':'قربت تذبل'):'';return `<div class="ps"><span>${SK[k].n}</span>${houses(L,SK[k].req,false)}<span class="mut">${LV[L-1]}${h?' · '+h:''}</span></div>`}).join('');
 modal(`<div class="psum"><div class="row between" style="align-items:center"><div style="text-align:start"><h2 id="mt" style="font-size:24px">${enm(i)}</h2><span class="mut" style="color:#C3B8A6">${STN[stageOf(f)]} · ${f} سعفة · عبء ${loadOf(i)}%</span></div><span class="chip" style="background:${GRP[g][2]};color:#fff">${GRP[g][0]} · ${rd}%</span></div><div class="pss">${rows}</div><details class="disc dk"><summary><span>كل الجدارات (${Object.keys(SK).length})</span><span class="chev" aria-hidden="true">${ICN.chev}</span></summary><div class="dbody"><div class="pss">${all}</div></div></details><div class="row" style="gap:10px;justify-content:space-between;margin-top:8px"><span class="mut" style="color:#C3B8A6">360: ${EMP[i].b360} من 5</span><span class="mut" style="color:#C3B8A6">الأداء: ${['','يحتاج دعم','جيد','عالي'][EMP[i].perf]}</span></div><button class="btn sand" data-act="closeModal" style="margin-top:14px">تمام</button></div>`)}"""+s[b:]

# governance grouped weights
R("""  <div class="wts">${Object.keys(SK).map(k=>`<div class="wt"><label for="w-${k}"><b>${SK[k].n}</b><span class="mut">${SK[k].t} · المطلوب ${LV[SK[k].req-1]}</span></label><input id="w-${k}" type="range" min="0" max="50" step="5" value="${W[k]}" data-w="${k}" ${S.Wpending?'disabled':''}><b class="wv">${W[k]}%</b></div>`).join('')}</div>""",
"""  <div class="wts">${TYPES.map(([ty,how],ti)=>{const ks=Object.keys(SK).filter(k=>SK[k].t===ty);const sub=ks.reduce((a,k)=>a+W[k],0);return disc(`<b>${ty}</b> <span class="mut">· ${ks.length} جدارات · </span><span class="tsum" data-tsum="${ty}">${sub}%</span>`,`<p class="mut small" style="margin:0 0 8px">${how}</p><div class="wgrp">${ks.map(k=>`<div class="wt"><label for="w-${k}"><b>${SK[k].n}</b><span class="mut">المطلوب ${LV[SK[k].req-1]}</span></label><input id="w-${k}" type="range" min="0" max="40" step="1" value="${W[k]}" data-w="${k}" aria-label="وزن ${SK[k].n}" ${S.Wpending?'disabled':''}><b class="wv">${W[k]}%</b></div>`).join('')}</div>`,ti===0?'open':'')}).join('')}</div>""")
R("<span class=\"mut\">الأوزان تحدد الجاهزية. أي تعديل يحتاج اعتماد لجنة، وينسجل.</span>",
  "<span class=\"mut\">${Object.keys(SK).length} جدارة في أربعة أنواع: فنية، سلوكية، قيادية، جوهرية. الأوزان تحدد الجاهزية، وأي تعديل يحتاج اعتماد لجنة ويُسجَّل.</span>")
R("const sb=$('[data-act=wSend]');if(sb)sb.disabled=tot!==100}});",
  "const sb=$('[data-act=wSend]');if(sb)sb.disabled=tot!==100;TYPES.forEach(([ty])=>{const el=document.querySelector(`[data-tsum=\"${ty}\"]`);if(el)el.textContent=Object.keys(SK).filter(k=>SK[k].t===ty).reduce((a,k)=>a+S.Wdraft[k],0)+'%'})}});")

# ---------- 3. gender ----------
R("['g','الجنس',[['','الكل'],['m','ولد'],['f','بنت']]]","['g','الجنس',[['','الكل'],['m','ذكر'],['f','أنثى']]]")
R("${EMP[i].g==='f'?'بنت':'ولد'}","${EMP[i].g==='f'?'أنثى':'ذكر'}")

# ---------- 4. KPI explanations ----------
R("const BUDGET={total:120000};","""const BUDGET={total:120000};
/* شرح المؤشرات: [الاسم، طريقة الحساب، المصدر] */
const KPIX={err:['أخطاء التجهيز','الطلبات اللي طلع فيها خطأ (صنف غلط أو كمية ناقصة) ÷ كل الطلبات المجهّزة','بلاغات المراجعة في نظام إدارة المستودع'],late:['متوسط التأخير','متوسط الدقائق بين وقت خروج الطلب المخطط ووقت خروجه الفعلي، مرجّح بعدد الطلبات','أوقات المسح في نظام إدارة المستودع'],inv:['دقة الجرد','المواقع اللي عدّها الفعلي يطابق رصيد النظام ÷ كل المواقع المجرودة','نتائج الجرد الدوري'],uph:['طلبات في الساعة','الطلبات المجهّزة ÷ ساعات التجهيز الفعلية للفريق','نظام إدارة المستودع ونظام الحضور'],keep:['المحافظة على المهارات','مهاراتك المحدّثة ÷ كل مهاراتك المعتمدة','عمر المهارة في دبره'],load:['عبء العمل','ساعات الشغل الفعلية في الأسبوع ÷ 40 ساعة. فوق 110% مضغوط، وتحت 80% عنده مساحة','نظام الحضور والمهام المسندة، ويتحدث مع كل تدوير']};
const kpiHelp=keys=>disc('كيف تُحسب هالمؤشرات؟',`<div class="kx">${keys.map(k=>`<div><b>${KPIX[k][0]}</b><span>${KPIX[k][1]}</span><span>المصدر: ${KPIX[k][2]}</span></div>`).join('')}</div><p class="mut small" style="margin:10px 0 0">الأهداف يحددها المدير مع مسؤولة التطوير من أداء الربع الماضي، والأرقام تتحدث كل أسبوع.</p>`);""")
R("['أخطاء التجهيز في ورديتك','2.6%','الهدف 2.5%',90]","['أخطاء التجهيز في فريقك','2.6%','الهدف 2.5%',90]")
R("""return `<div class="g4">${k.map(([n,v,t,p])=>kpi(n,v,t,{p,col:p>=95?'var(--ok)':''})).join('')}</div>
 <div class="card reveal"><div class="row between"><h3 style="font-size:20px">تقييم 360""",
"""return `<div class="g4">${k.map(([n,v,t,p])=>kpi(n,v,t,{p,col:p>=95?'var(--ok)':''})).join('')}</div>
 <div class="card reveal">${kpiHelp(['err','late','inv','keep'])}</div>
 <div class="card reveal"><div class="row between"><h3 style="font-size:20px">تقييم 360""")
R("""return `<div class="g4">${K.map(([n,v,t,p])=>kpi(n,v,`الهدف ${t}`,{p,col:p>=95?'var(--ok)':''})).join('')}</div>""",
"""return `<div class="g4">${K.map(([n,v,t,p])=>kpi(n,v,`الهدف ${t}`,{p,col:p>=95?'var(--ok)':''})).join('')}</div>
 <div class="card reveal">${kpiHelp(['err','late','inv','uph','load'])}</div>""")
R("""<p class="mut small" style="margin-top:10px">مأخوذ من الورديات والمهام المسجلة في نظام المستودع.</p></div>""","</div>")
# rotation cards with before/after
R("""  ${[['r1','خالد المطيري (68%) يتدوّر 3 شهور مع ماجد (130%) في نظام إدارة المستودع','يخفف ضغط ماجد، ويكسر احتكار المعرفة'],['r2','سلطان العتيبي (78%) ينتقل شهرين لمنطقة التبريد مع عمر','يتعلم مهارة حرجة، ويرفع أدلته الفنية'],['r3','عبدالله الشمري (115%) يسلّم تقرير الخميس لفهد (90%)','يوازن العبء ويطوّر فهد في التقارير']].map(([k,t,w])=>`<div class="rot"><div><b>${t}</b><span class="mut">${w}</span></div>${S.rot[k]?'<span class="chip g">اعتمدته</span>':`<button class="btn" data-act="rot" data-k="${k}" style="min-height:44px">اعتمد</button>`}</div>`).join('')}</div></div>`}""",
"""  ${ROT.map(([k,to,fr,h,t,w])=>{const on=!!S.rot[k];const L=i=>Math.round((hrsOf(i)+(on?0:(i===to?h:-h)))/40*100);const nmf=i=>enm(i).split(' ')[0];return `<div class="rot"><div><b>${t}</b><span class="mut">${w} · ينقل ${h} ساعات أسبوعيًا</span><div class="rotfx"><span>${nmf(fr)}: ${on?`${L(fr)}%`:`${loadOf(fr)}% ← ${L(fr)}%`}</span><span>${nmf(to)}: ${on?`${L(to)}%`:`${loadOf(to)}% ← ${L(to)}%`}</span></div></div>${on?'<span class="chip g">اعتمدته · العبء تحدّث</span>':`<button class="btn" data-act="rot" data-k="${k}" style="min-height:44px">اعتمد</button>`}</div>`}).join('')}</div></div>`}""")
R("rot(b){API.approveRotation(b.dataset.k);render();toast('اعتمدت التدوير، ووصل إشعار للموظفين')},",
  "rot(b){const k=b.dataset.k;API.approveRotation(k);render();toast('اعتمدت التدوير، وتحدّث عبء العمل',()=>{API.undoRotation(k);render()})},")
R(" approveRotation(k){S.rot[k]=1},"," approveRotation(k){S.rot[k]=1},\n // DELETE /rotations/:id/approval\n undoRotation(k){delete S.rot[k]},")
R("'العبء 128% على ماجد، والطلبات زادت 6%'","`العبء ${loadOf(1)}% على ماجد، والطلبات زادت 6%`")

# ---------- 5. hero paragraphs removed ----------
R("""<h1 style="font-size:32px">تعلّم من أهل الدبره</h1><p style="color:#D9CFBE;margin:0">بدون ميزانية: مرشدك، وورش يقدمها خبراء الشركة، ومحتوى رفعته شركتك. وكل تعلّم تثبته بتحدي.</p></div>""",
  """<h1 style="font-size:32px;margin:0">تعلّم من أهل الدبره</h1></div>""")
R("""<h1 style="font-size:32px">وش تحتاج الشركة فعلًا؟</h1><p style="color:#D9CFBE;margin:0">من عبء العمل، والمهارات الحرجة، والأهداف. ودايمًا الداخلي أول.</p></div>""",
  """<h1 style="font-size:32px;margin:0">وش تحتاج الشركة فعلًا؟</h1></div>""")

# ---------- 6. learning: my registrations ----------
a=s.index("function empLearn(){");b=s.index("function empJobs(){")
s=s[:a]+r"""const MENTOR={n:'ماجد القحطاني',slot:'الأحد 2 م · 30 دقيقة'};
const WS=[['wms','نظام إدارة المستودع المتقدم','يقدمها ماجد القحطاني · الأحد 10 ص'],['cold','تحميل التبريد بأمان','يقدمها عمر الحسيني · الثلاثاء 1 م'],['ai','تقارير الأداء بالذكاء الاصطناعي','تقدمها نورة السبيعي · الخميس 11 ص']];
const CT=[['c1','دليل إجراءات الجرد الدوري','PDF · 12 صفحة · رفعته الشركة'],['c2','فيديو: ترتيب الرفوف حسب ABC','8 دقائق · رفعه ماجد'],['c3','قوالب تقرير الأداء الأسبوعي','ملف Excel · رفعته هيا']];
function myRegs(){const it=[];if(S.mentorBook)it.push(['جلسة إرشاد','مع '+MENTOR.n,MENTOR.slot,'mentor','',0]);
 WS.forEach(([k,n,d])=>{if(S.ws[k])it.push(['ورشة',n,d,'ws',k,0])});CT.forEach(([k,n,d])=>{if(S.content[k])it.push(['محتوى',n,S.content[k]==='done'?'خلّصته':'في قائمتك',  'content',k,S.content[k]==='done'?1:0])});return it}
function empLearn(){const R=myRegs();
 return `<div class="card night reveal hello"><span class="mut">الشركة تعلّم نفسها</span><h1 style="font-size:32px;margin:0">تعلّم من أهل الدبره</h1></div>
 <div class="card reveal"><div class="row between"><h3 style="font-size:20px">تسجيلاتي</h3><span class="mut">${R.length?R.length+' عناصر':''}</span></div>${R.length?`<div class="myreg">${R.map(([t,n,d,kind,k,done])=>`<div class="ri2"><span class="tag ${kind==='content'&&!done?'c':''}">${t}</span><div><b>${n}</b><span class="mut">${d}</span></div>${kind==='content'&&!done?`<button class="btn ghost" data-act="ctDone" data-k="${k}" style="min-height:40px;color:var(--ink)">خلّصته</button>`:''}${done?'':`<button class="linkbtn" data-act="unreg" data-kind="${kind}" data-k="${k}">إلغاء</button>`}</div>`).join('')}</div>`:'<p class="mut" style="margin:8px 0 0">ما سجّلت في شيء للحين. احجز جلسة مع مرشدك، أو سجّل في ورشة، أو أضف محتوى لقائمتك من تحت.</p>'}</div>
 <div class="g2"><div class="card reveal"><h3 style="font-size:20px">مرشدك</h3><div class="mentor"><div class="av2">م</div><div><b>${MENTOR.n}</b><span class="mut">«ذيب» في إدارة المخزون · مرشد المستودع المركزي</span></div></div>${S.mentorBook?`<span class="chip g">محجوزة: ${MENTOR.slot}</span>`:'<button class="btn" data-act="mentor">احجز جلسة 30 دقيقة</button>'}</div>
 <div class="card reveal"><h3 style="font-size:20px">ورش داخلية</h3>${WS.map(([k,n,d])=>`<div class="nmrow" style="margin-top:8px"><span><b>${n}</b><span class="mut">${d}</span></span>${S.ws[k]?'<span class="chip g">مسجّل</span>':`<button class="btn ghost" data-act="ws" data-k="${k}" style="min-height:40px;color:var(--ink)">سجّل</button>`}</div>`).join('')}</div></div>
 <div class="card reveal"><h3 style="font-size:20px">محتوى من شركتك</h3><div class="uc">${CT.map(([k,n,d])=>`<div><b>${n}</b><span class="mut">${d}</span>${S.content[k]?`<span class="chip ${S.content[k]==='done'?'g':''}" style="margin-top:8px;width:fit-content">${S.content[k]==='done'?'خلّصته':'في قائمتك'}</span>`:`<button class="linkbtn" data-act="content" data-k="${k}">أضفه لقائمتي</button>`}</div>`).join('')}</div><p class="mut small" style="margin-top:8px">المحتوى يساعدك تتعلم، بس المستوى ما يرتفع إلا بتحدي.</p></div>`}
"""+s[b:]
R(" bookMentor(){S.mentorBook=true},"," bookMentor(){S.mentorBook=true},\n // DELETE /mentorship/sessions/:id\n cancelMentor(){S.mentorBook=false},")
R(" registerWorkshop(k){S.ws[k]=1},"," registerWorkshop(k){S.ws[k]=1},\n // DELETE /workshops/:id/registrations/me\n cancelWorkshop(k){delete S.ws[k]},")
R(" toggleContent(k){S.content[k]=!S.content[k]},"," setContent(k,st){if(st)S.content[k]=st;else delete S.content[k]},")
R(" content(b){API.toggleContent(b.dataset.k);render()},",
  """ content(b){API.setContent(b.dataset.k,'saved');render();toast('أضفناه لقائمتك في «تسجيلاتي»')},
 ctDone(b){API.setContent(b.dataset.k,'done');render();toast('أحسنت، خلّصته. ثبّت اللي تعلمته بتحدي.')},
 unreg(b){const kind=b.dataset.kind,k=b.dataset.k;if(kind==='mentor')API.cancelMentor();else if(kind==='ws')API.cancelWorkshop(k);else API.setContent(k,null);render();toast('ألغيت التسجيل',()=>{if(kind==='mentor')API.bookMentor();else if(kind==='ws')API.registerWorkshop(k);else API.setContent(k,'saved');render()})},""")
R("mentor(){API.bookMentor();render();toast('حجزت جلسة مع ماجد الأحد 2 م')},","mentor(){API.bookMentor();render();toast('حجزت جلسة مع ماجد، وتلقاها في «تسجيلاتي»')},")
R("ws(b){API.registerWorkshop(b.dataset.k);render();toast('سجّلت في الورشة')},","ws(b){API.registerWorkshop(b.dataset.k);render();toast('سجّلت في الورشة، وتلقاها في «تسجيلاتي»')},")

# ---------- 7. manager notes validation ----------
R("function decideBtn(b,approve){const id=b.dataset.q;const note=($('#mn-'+id)?.value||'').trim();",
  "function decideBtn(b,approve){const id=b.dataset.q;const ta=$('#mn-'+id);const note=(ta?.value||'').replace(/\\s+/g,' ').trim();if(!approve&&note.length<5){ta?.classList.add('bad');ta?.focus();toast('اكتب ملاحظتك (5 أحرف على الأقل) قبل ما ترجّع الطلب');return}ta?.classList.remove('bad');")
R("rejMajed(){const r=($('#mjr')?.value||'').trim();if(r.length<10){toast('اكتب سبب مهني واضح قبل الرفض');$('#mjr')?.focus();return}",
  "rejMajed(){const ta=$('#mjr');const r=(ta?.value||'').replace(/\\s+/g,' ').trim();if(r.length<10||!/[\\u0621-\\u064Aa-zA-Z]{3}/.test(r)){ta?.classList.add('bad');toast('اكتب سببًا مهنيًا واضحًا (10 أحرف على الأقل) قبل الرفض');ta?.focus();return}ta?.classList.remove('bad');")

# ---------- 8. certificate form: empty + demo fill + validation ----------
R("""<div class="fld"><label for="ct">اسم الشهادة</label><input id="ct" value="${esc(c.title||'شهادة إدارة المخزون والمستودعات')}"><span class="err"></span></div>
 <div class="fgrid"><div class="fld"><label for="ci">الجهة المانحة</label><input id="ci" value="${esc(c.issuer||'معهد سلاسل الإمداد')}"><span class="err"></span></div><div class="fld"><label for="cd">تاريخ الحصول عليها</label><input id="cd" value="${esc(c.date||'سبتمبر 2026')}"><span class="err"></span></div></div>""",
"""<div class="fillbar"><span>تعرض المنصة لأحد؟ عبّئ النموذج ببيانات تجريبية.</span><button type="button" class="btn ghost" data-act="certDemo" style="min-height:40px;color:var(--ink)">عبّئ ببيانات تجريبية</button></div>
 <div class="fld"><label for="ct">اسم الشهادة</label><input id="ct" maxlength="80" placeholder="مثال: شهادة إدارة المخزون والمستودعات" value="${esc(c.title||'')}"><span class="err"></span></div>
 <div class="fgrid"><div class="fld"><label for="ci">الجهة المانحة</label><input id="ci" maxlength="60" placeholder="مثال: معهد سلاسل الإمداد" value="${esc(c.issuer||'')}"><span class="err"></span></div><div class="fld"><label for="cd">تاريخ الحصول عليها</label><input id="cd" type="date" min="1990-01-01" max="${new Date().toISOString().slice(0,10)}" value="${esc(c.date||'')}"><span class="err"></span></div></div>""")
R("""$('#cf').onchange=e=>{const f=e.target.files[0];if(f){S.cert.file=f.name;$('#cfn').textContent=f.name;$('#cfe').textContent=''}};""",
  """$('#cf').onchange=e=>{const f=e.target.files[0];if(!f)return;const okT=/\\.(pdf|png|jpe?g|webp|heic)$/i.test(f.name);if(!okT){$('#cfe').textContent='الملف لازم يكون PDF أو صورة';e.target.value='';return}if(f.size>5*1024*1024){$('#cfe').textContent='حجم الملف أكبر من 5 ميجا';e.target.value='';return}S.cert.file=f.name;$('#cfn').textContent=f.name;$('#cfe').textContent=''};""")
R("""certNext(){let ok=true;[['ct','اكتب اسم الشهادة'],['ci','اكتب الجهة المانحة'],['cd','اكتب التاريخ']].forEach(([id,m])=>{const el=$('#'+id);const bad=el.value.trim().length<2;el.parentElement.classList.toggle('bad',bad);el.parentElement.querySelector('.err').textContent=bad?m:'';if(bad)ok=false});if(!S.cert.file){$('#cfe').textContent='أرفق ملف الشهادة';ok=false}if(!ok)return;""",
"""certDemo(){$('#ct').value=$('#ck').value==='cap'?'شهادة تخطيط الطاقة والعمليات':'شهادة إدارة المخزون والمستودعات';$('#ci').value='معهد سلاسل الإمداد';$('#cd').value='2026-09-15';S.cert.file='شهادة-تجريبية.pdf';$('#cfn').textContent=S.cert.file;$$('#dbody .fld').forEach(f=>{f.classList.remove('bad');const e=f.querySelector('.err');if(e)e.textContent=''})},
 certNext(){let ok=true,first=null;const chk=(id,msg)=>{const el=$('#'+id);el.value=el.value.replace(/\\s+/g,' ').trim();const m=msg(el.value);el.parentElement.classList.toggle('bad',!!m);el.parentElement.querySelector('.err').textContent=m||'';if(m){ok=false;first=first||el}};
  chk('ct',v=>!v?'اكتب اسم الشهادة':v.length<4?'الاسم قصير، اكتبه كامل':!/[\\u0621-\\u064Aa-zA-Z]{3}/.test(v)?'اسم الشهادة لازم يكون كلام، مو أرقام بس':'');
  chk('ci',v=>!v?'اكتب الجهة المانحة':!/^[\\u0621-\\u064A\\u0660-\\u0669a-zA-Z0-9\\s.&()\\-]+$/.test(v)?'الجهة فيها رموز غير مقبولة':v.length<3?'اكتب اسم الجهة كامل':'');
  chk('cd',v=>{if(!v)return 'اختر تاريخ الحصول على الشهادة';const d=new Date(v);if(isNaN(d))return 'التاريخ غير صحيح';if(d>new Date())return 'التاريخ ما يصير في المستقبل';if(d<new Date('1990-01-01'))return 'التاريخ قديم جدًا';return ''});
  if(!S.cert.file){$('#cfe').textContent='أرفق ملف الشهادة';ok=false}if(!ok){first?.focus();return}""")
R("<span class=\"mut\">${esc(c.issuer)} · ${esc(c.date)}</span>","<span class=\"mut\">${esc(c.issuer)} · ${fmtD(c.date)}</span>")
R("const esc=t=>","const fmtD=d=>{const x=new Date(d);return isNaN(x)?esc(d):x.toLocaleDateString('ar-SA-u-ca-gregory-nu-latn',{year:'numeric',month:'long'})};\nconst esc=t=>")

# ---------- 9. login: empty + demo fill + strict validation ----------
a=s.index("const ROLES={");b=s.index("/* scroll spy */")
s=s[:a]+r"""const ROLES={
 emp:{t:'موظف',d:'أثبت مهاراتك، واعرف طريقك للترقية.',f:[['name','الاسم الكامل','name','عبدالله الشمري','مثال: عبدالله الشمري'],['eid','الرقم الوظيفي','id','10482','من 4 إلى 8 أرقام'],['email','البريد الإلكتروني للعمل','email','abdullah.alshammari@sharq.sa','name@company.sa'],['title','المسمى الحالي','text','مشرف مستودع','مثال: مشرف مستودع'],['dept','الإدارة','dept','0','']]},
 mgr:{t:'مدير مباشر',d:'تابع فريقك وأداءهم وعبء شغلهم، ورشّح الجاهزين.',f:[['name','الاسم الكامل','name','محمد العنزي','مثال: محمد العنزي'],['eid','الرقم الوظيفي','id','20117','من 4 إلى 8 أرقام'],['email','البريد الإلكتروني للعمل','email','mohammed.alanazi@sharq.sa','name@company.sa'],['dept','الإدارة','dept','0',''],['team','عدد أعضاء فريقك','num','7','من 1 إلى 200',1,200]]},
 haya:{t:'مسؤول تطوير',d:'المواهب والوظائف والتدريب والحوكمة في مكان واحد.',f:[['name','الاسم الكامل','name','هيا القحطاني','مثال: هيا القحطاني'],['eid','الرقم الوظيفي','id','30561','من 4 إلى 8 أرقام'],['email','البريد الإلكتروني للعمل','email','haya.alqahtani@sharq.sa','name@company.sa'],['org','المنشأة','org','مستودعات الشرق','اسم منشأتك'],['count','عدد الموظفين','num','52','من 1 إلى 100,000',1,100000]]}};
/* تحويل الأرقام العربية للاتينية، وتوحيد المسافات */
const normD=v=>v.replace(/[٠-٩]/g,d=>'٠١٢٣٤٥٦٧٨٩'.indexOf(d));
const clean=v=>v.replace(/\s+/g,' ').trim();
const VAL={
 name:v=>!v?'اكتب اسمك':/[0-9٠-٩]/.test(v)?'الاسم ما يكون فيه أرقام':!/^[ء-يـa-zA-Z\s'-]+$/.test(v)?'الاسم يكون حروف بس، بدون رموز':v.split(' ').length<2?'اكتب اسمك الأول واسم العائلة':v.split(' ').some(w=>w.length<2)?'كل جزء من الاسم لازم يكون حرفين أو أكثر':v.length>50?'الاسم أطول من 50 حرف':'',
 id:v=>{v=normD(v);return !v?'اكتب رقمك الوظيفي':!/^\d+$/.test(v)?'الرقم الوظيفي أرقام بس':v.length<4||v.length>8?'الرقم الوظيفي من 4 إلى 8 أرقام':''},
 email:v=>!v?'اكتب بريدك الإلكتروني':/\s/.test(v)?'البريد ما يكون فيه مسافات':!/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/.test(v)?'اكتب بريد صحيح، مثل name@company.sa':'',
 text:v=>!v?'اكتب مسماك الوظيفي':/[0-9٠-٩]/.test(v)?'المسمى يكون كلام، بدون أرقام':!/^[ء-يـa-zA-Z\s()\-]+$/.test(v)?'المسمى فيه رموز غير مقبولة':v.length<3?'المسمى قصير':v.length>40?'المسمى أطول من 40 حرف':'',
 org:v=>!v?'اكتب اسم المنشأة':!/[ء-يa-zA-Z]{2}/.test(v)?'اسم المنشأة لازم يكون فيه حروف':!/^[ء-يـa-zA-Z0-9\s&.()\-]+$/.test(v)?'اسم المنشأة فيه رموز غير مقبولة':v.length>60?'الاسم أطول من 60 حرف':'',
 dept:v=>v===''?'اختر الإدارة':'',
 num:(v,mn,mx)=>{v=normD(v);return !v?'اكتب الرقم':!/^\d+$/.test(v)?'اكتب رقم صحيح بس، بدون حروف أو كسور':+v<mn||+v>mx?`الرقم لازم يكون بين ${mn} و${mx.toLocaleString('en-US')}`:''}};
function fieldHTML([id,l,k,demo,ph,mn,mx]){const inp=k==='dept'?`<select id="i-${id}" data-k="${k}"><option value="" selected disabled>اختر الإدارة</option>${DEPTS.map((d,i)=>`<option value="${i}">${d}</option>`).join('')}</select>`:`<input id="i-${id}" data-k="${k}" ${mn!=null?`data-min="${mn}" data-max="${mx}"`:''} type="${k==='email'?'email':'text'}" ${k==='email'?'dir="ltr" autocomplete="email" spellcheck="false"':k==='name'?'autocomplete="name"':'autocomplete="off"'} ${k==='id'||k==='num'?'inputmode="numeric"':''} maxlength="${k==='email'?80:k==='id'?8:k==='num'?6:60}" placeholder="${ph}" aria-describedby="e-${id}">`;
 return `<div class="fld" id="f-${id}"><label for="i-${id}">${l}</label>${inp}<span class="err" id="e-${id}" aria-live="polite"></span></div>`}
function loginStep(role){
 if(!role){$('#lbox').innerHTML=`<div class="eyebrow">تسجيل الدخول · الخطوة 1 من 2</div><h1 style="font-size:clamp(32px,4.5vw,48px)">مين أنت في المنشأة؟</h1><p style="color:#CFC4B2;margin-top:10px">اختر دورك، ونجهّز لك الشاشة اللي تناسبك.</p><div class="lroles">${Object.entries(ROLES).map(([k,r])=>`<button class="lrole" data-pick="${k}"><span class="ri">${RI[k]}</span><b>${r.t}</b><span>${r.d}</span></button>`).join('')}</div>`;return}
 const r=ROLES[role];
 $('#lbox').innerHTML=`<div class="eyebrow">تسجيل الدخول · الخطوة 2 من 2</div><h1 style="font-size:clamp(30px,4vw,44px)">بياناتك الأساسية · ${r.t}</h1><p style="color:#CFC4B2;margin-top:10px">كل الحقول مطلوبة.</p>
 <form class="lform" id="lform" novalidate data-lrole="${role}"><div class="fillbar"><span>تعرض المنصة لأحد؟ عبّئ كل الحقول ببيانات تجريبية بضغطة.</span><button type="button" class="btn ghost" data-lfill style="min-height:40px;color:var(--ink)">عبّئ ببيانات تجريبية</button></div><div class="fgrid">${r.f.map(fieldHTML).join('')}</div>
 <div class="lacts"><button type="button" class="btn ghost" data-pick="" style="color:var(--ink)">غيّر الدور</button><span class="grp"><button type="button" class="btn ghost" data-lclear style="color:var(--ink)">امسح</button><button type="submit" class="btn">دخول</button></span></div></form>`;
 setTimeout(()=>$('#i-name')?.focus(),200)}
const fieldErr=el=>{const k=el.dataset.k;const v=k==='dept'?el.value:clean(el.value);return VAL[k](v,+el.dataset.min,+el.dataset.max)};
const showErr=(el,m)=>{const w=el.closest('.fld');w.classList.toggle('bad',!!m);w.querySelector('.err').textContent=m||'';el.setAttribute('aria-invalid',!!m)};
document.addEventListener('click',e=>{const p=e.target.closest('[data-pick]');if(p){loginStep(p.dataset.pick||null);return}
 const f=e.target.closest('[data-lfill]');if(f){const fm=$('#lform');ROLES[fm.dataset.lrole].f.forEach(([id,,,demo])=>{const el=$('#i-'+id);el.value=demo;showErr(el,'')});$('[type=submit]',fm)?.focus();toast('عبّينا الحقول ببيانات تجريبية');return}
 const c=e.target.closest('[data-lclear]');if(c){$$('#lform input,#lform select').forEach(el=>{el.value='';showErr(el,'')});$('#i-name')?.focus()}});
document.addEventListener('focusout',e=>{const el=e.target;if(!el.closest||!el.closest('#lform')||!el.dataset.k)return;if(el.value!=='')showErr(el,fieldErr(el))});
document.addEventListener('input',e=>{const el=e.target;if(!el.closest||!el.closest('#lform')||!el.dataset.k)return;if(el.closest('.fld').classList.contains('bad'))showErr(el,fieldErr(el))});
document.addEventListener('change',e=>{const el=e.target;if(el.closest&&el.closest('#lform')&&el.dataset.k==='dept')showErr(el,fieldErr(el))});
document.addEventListener('submit',e=>{const f=e.target;if(f.id!=='lform')return;e.preventDefault();if(f.dataset.busy)return;const role=f.dataset.lrole;let first=null;
 $$('#lform [data-k]').forEach(el=>{if(el.dataset.k!=='dept')el.value=clean(el.dataset.k==='id'||el.dataset.k==='num'?normD(el.value):el.value);const m=fieldErr(el);showErr(el,m);if(m&&!first)first=el});
 if(first){first.focus();return}
 f.dataset.busy=1;const sb=f.querySelector('[type=submit]');sb.disabled=true;sb.textContent='جاري الدخول…';
 const prof={};$$('#lform [data-k]').forEach(el=>prof[el.id.slice(2)]=el.value);API.login(role,prof);
 setTimeout(()=>{location.hash='#app'},350);setTimeout(()=>toast(`حياك ${S.names[role]}، سجّلت دخولك`),400)});

"""+s[b:]
R(" dismiss(key){S.dis.add(key)}"," dismiss(key){S.dis.add(key)},\n // POST /auth/login  {role, employeeId, email, ...}  → {token, user}\n login(role,prof){S.profile={role,...prof};S.names[role]=prof.name.split(' ')[0];S.role=role;S.logged=true}")
R("logout(){S.logged=false}","logout(){S.logged=false;S.profile=null}")

# ---------- 10. config / env ----------
R("const DEPTS=","""/* CONFIG · على Netlify: عرّف API_BASE في متغيرات البيئة وحقنه في window.__ENV (Snippet injection). بدونه تشتغل المنصة على البيانات التجريبية */
const CONFIG={API_BASE:(window.__ENV&&window.__ENV.API_BASE)||'',USE_MOCK:!(window.__ENV&&window.__ENV.API_BASE)};
const DEPTS=""")

# ---------- 11. proofreading ----------
rep=[('انعتمدت تلقائيًا','اعتُمدت تلقائيًا'),('ينعتمد','يُعتمد'),('انعتمد','اعتُمد'),('انرسلت','أُرسلت'),('تنرسل','تُرسل'),('انرسل ','أُرسل '),
('تنحسب','تُحسب'),('انحسبت','حُسبت'),('ينكسب','يُكتسب'),('تنكسب','تُكتسب'),('تنقاس','تُقاس'),('ينفتح','يُفتح'),
('انضافوا','أُضيفوا'),('ينضاف','يُضاف'),('وانضاف','وأُضيف'),('انسجلت','سُجّلت'),('وينسجل','ويُسجَّل'),('وتنسجل','وتُسجَّل'),
('انطبق القرار','طُبّق القرار'),('وين انصرفت','وين صُرفت'),('كيف بينقيّم تقريرك','كيف يُقيَّم تقريرك'),('ما يتسلّم بعد','ما يُقبل بعد'),('أقل من 5 ما يتسلّم','أقل من 5 ما يُقبل'),
('مبتدي','مبتدئ'),('عبّ تقرير نموذجي','عبّئ تقرير نموذجي'),('ياخذ','يأخذ'),('تاخذ','تأخذ'),('تقراها','تقرأها'),('وجا 780','وجاء 780'),
('بتصدّي بعد','تذبل بعد'),('بتصدّي هالشهر','تذبل هالشهر'),('بتصدّي','قربت تذبل'),('أربع مواقف','أربعة مواقف'),
('«يوضح المطلوب قبل بداية الوردية»','«يوضح المطلوب قبل بداية الشغل»'),
('اختار النظام 4 زملاء اشتغلوا معك أكثر شي من الورديات والمهام المشتركة، والنتيجة معدّل بدون أسماء. وأي تقييم متطرف لازم معه مثال، ولو التقييم عالي والأداء ضعيف يطلع تنبيه لمديرك.',
 'اختار النظام 4 زملاء اشتغلوا معك أكثر من غيرهم في المهام المشتركة، والنتيجة متوسط تقييماتهم بدون أسماء. وأي تقييم مرتفع جدًا أو منخفض جدًا لازم يكون معه مثال، ولو التقييم عالي والأداء ضعيف يوصل تنبيه لمديرك.'),
('تنقصك','تنقصك')]
for o,n in rep:
    if o not in s: print('MISS',o)
    s=s.replace(o,n)
s=re.sub(r'(?<![؀-ۿ])شي(?![؀-ۿ])','شيء',s)
for bad in ['متطرف','معدّل بدون','ورديتك','الورديات']:
    if bad in s: print('STILL',bad)
assert '�' not in s
open('/home/claude/proto/v8.html','w',encoding='utf8').write(s)
print('ok',len(s))
