import sys
P='/home/claude/proto/v11.html'
s=open(P,encoding='utf8').read()
def R(old,new,cnt=1):
    global s
    n=s.count(old)
    if n==0 and old.startswith('  '):
        old=' '+old.lstrip(' ');new=' '+new.lstrip(' ');n=s.count(old)
    if n==0 and '\n  ' in old:
        o2=old.replace('\n  ','\n ');
        if s.count(o2)==cnt: old=o2;new=new.replace('\n  ','\n ');n=cnt
    if n!=cnt: sys.exit(f'COUNT {n}!={cnt}: {old[:110]}')
    s=s.replace(old,new)

# =============== state / names ===============
R("names:{emp:'عبدالله',mgr:'محمد',haya:'هيا'}","names:{emp:'عبدالله',mgr:'محمد',haya:'هيا',top:'فيصل'}")
R("tab:{emp:'path',mgr:'team',haya:'talent'}","tab:{emp:'path',mgr:'team',haya:'talent',top:'files'}")
R("const nm=t=>t.replaceAll('عبدالله',S.names.emp).replaceAll('محمد',S.names.mgr).replaceAll('هيا',S.names.haya);",
  "const nm=t=>t.replaceAll('عبدالله',S.names.emp).replaceAll('محمد',S.names.mgr).replaceAll('هيا',S.names.haya).replaceAll('فيصل',S.names.top);")
R("""      <button data-role="haya" aria-pressed="false">مسؤول تطوير</button>""","""      <button data-role="haya" aria-pressed="false">مسؤول تطوير</button>
      <button data-role="top" aria-pressed="false">إدارة عليا</button>""")
R("{emp:'موظف',mgr:'مدير مباشر',haya:'تطوير'}[b.dataset.role]","{emp:'موظف',mgr:'مدير مباشر',haya:'تطوير',top:'إدارة عليا'}[b.dataset.role]")
R(".lroles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:28px}",".lroles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:28px}@media(max-width:1000px){.lroles{grid-template-columns:repeat(2,minmax(0,1fr))}}")
R(".mods{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:36px}",".mods{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:36px}@media(max-width:1100px){.mods{grid-template-columns:repeat(2,minmax(0,1fr))}}")
R("<p class=\"sub reveal\">من الموظف اللي يثبت مهارته، إلى المدير اللي يقود فريقه، إلى مسؤولة التطوير اللي تخطط للمنشأة كلها.</p>",
  "<p class=\"sub reveal\">من الموظف اللي يثبت مهارته، إلى المدير اللي يقود فريقه، إلى مسؤولة التطوير اللي تخطط، إلى الإدارة العليا اللي تعتمد وتراقب.</p>")
R("<li>حوكمة الجدارات والتظلّمات والترقية الاستثنائية</li></ul></div>",
  "<li>حوكمة الجدارات والتظلّمات والترقية الاستثنائية</li></ul></div>\n      <div class=\"mod reveal\"><b class=\"kufi\">الإدارة العليا</b><ul><li>مراجعة الترقيات المرفوضة بسبب مكتوب</li><li>اعتماد خطط التطوير وميزانيتها</li><li>أبطال الأقسام والمهارات</li><li>موظف الشهر بمعادلة معلنة</li><li>لوحة الشركة التفاعلية</li></ul></div>")
R("<li>مرشد وورش داخلية ومحتوى من شركته</li><li>فرص نقل داخلي تطابق مهاراته</li></ul>",
  "<li>مرشد وورش ودورات ومحتوى من شركته</li><li>مؤشر التعلّم 70-20-10 ودورة 30-60-90</li><li>لوحة الشرف وترتيبه في قسمه والشركة</li><li>فرص نقل داخلي تطابق مهاراته</li></ul>")

# login role
R(" haya:{t:'مسؤول تطوير',"," top:{t:'إدارة عليا',d:'راجع الترقيات المحوّلة، واعتمد الخطط، وشوف أبطال الشركة.',f:[['name','الاسم الكامل','name','فيصل الدوسري','مثال: فيصل الدوسري'],['eid','الرقم الوظيفي','id','40023','من 4 إلى 8 أرقام'],['email','البريد الإلكتروني للعمل','email','faisal.aldosari@sharq.sa','name@company.sa'],['title','المسمى الحالي','text','مدير العمليات','مثال: مدير العمليات']]},\n haya:{t:'مسؤول تطوير',")
# move top after haya in login order: rebuild order via Object keys order -> place explicitly
R("Object.entries(ROLES).map(([k,r])=>`<button class=\"lrole\" data-pick=\"${k}\">","['emp','mgr','haya','top'].map(k=>[k,ROLES[k]]).map(([k,r])=>`<button class=\"lrole\" data-pick=\"${k}\">")
R("const RI={emp:","const RI={top:'<svg width=\"28\" height=\"28\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#fff\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3 21h18M5 21V8l7-5 7 5v13M9 21v-6h6v6\"/></svg>',emp:")

# =============== promotion: rejection reason -> senior management ===============
R(" recordInterview(pass){const m=S.majed;m.interview=pass?'pass':'fail';",
  " recordInterview(pass,reason){const m=S.majed;m.interview=pass?'pass':'fail';m.reason=reason||'';")
R("}else{m.status='retry';S.hist.unshift({who:'ماجد القحطاني',what:'مقابلة الترقية',dec:'ما أثبت: تحدي إضافي ثم مقابلة ثانية',when:'اليوم',ok:0})}",
  "}else{m.status='esc';S.hist.unshift({who:'ماجد القحطاني',what:'مقابلة الترقية',dec:'رفضها المدير بسبب مكتوب، وتحوّلت للإدارة العليا',when:'اليوم',ok:0})}")
R("// PATCH /promotions/:id  {interview:'pass'|'fail'}  → لو نجح ينتقل الملف للجنة تلقائيًا",
  "// PATCH /promotions/:id  {interview:'pass'|'fail', reason}  → النجاح ينقل الملف للجنة، والرفض يحوّله للإدارة العليا\n // PATCH /promotions/:id/escalation  {decision:'uphold'|'overturn', note}\n reviewEscalation(uphold){const m=S.majed;m.status=uphold?'retry':'sent';m.top=uphold?'uphold':'overturn';S.hist.unshift({who:'ماجد القحطاني',what:'مراجعة الإدارة العليا',dec:uphold?'أيّدت الرفض: تحدي إضافي ثم مقابلة ثانية':'ألغت الرفض، وانتقل الملف للجنة',when:'اليوم',ok:uphold?0:1});if(!uphold)S.audit.unshift({who:'فيصل',what:'ألغى رفض ترقية ماجد القحطاني بعد مراجعة الأدلة',when:'اليوم'});return ()=>{m.status='esc';m.top=null;S.hist.shift();if(!uphold)S.audit.shift()}},")
R("const chip=m.status==='sent'?['g','انتقل للجنة تلقائيًا']:m.status==='retry'?['r','يحتاج تحدي إضافي']:",
  "const chip=m.status==='sent'?['g',m.top==='overturn'?'الإدارة العليا ألغت الرفض · عند اللجنة':'انتقل للجنة تلقائيًا']:m.status==='esc'?['y','رفضته · عند الإدارة العليا']:m.status==='retry'?['r','الإدارة العليا أيّدت الرفض · تحدي إضافي']:")
R("""<button class="btn ghost" data-act="interview" data-v="0">ما أثبت في المقابلة</button></div>`:'')""",
  """<button class="btn ghost" data-act="interview" data-v="0">ما أثبت في المقابلة</button></div><label class="f" for="ivr" style="margin-top:12px">سبب عدم الإثبات (إلزامي لو ما أثبت)</label><textarea id="ivr" placeholder="سبب مهني محدد، مثل: ما قدر يشرح خطوات حل التحدي"></textarea><p class="mut small" style="margin-top:6px">لو رفضت، يتحوّل الملف مع السبب لمدير الإدارة العليا يراجعه، عشان القرار ما يعتمد على شخص واحد.</p>`:'')+(m.status==='esc'?`<div class="banner y" style="margin-top:12px"><b>سبب الرفض:</b><span style="flex:1">${esc(m.reason)}</span></div>`:'')""")
R(" interview(b){const pass=b.dataset.v==='1';const u=API.recordInterview(pass);render();toast(pass?'سجّلت المقابلة، وانتقل ملف ماجد للجنة تلقائيًا':'سجّلت المقابلة: يحتاج تحدي إضافي',()=>{u();render()})},",
  """ interview(b){const pass=b.dataset.v==='1';let reason='';if(!pass){const ta=$('#ivr');reason=(ta?.value||'').replace(/\\s+/g,' ').trim();if(reason.length<10||!/[\\u0621-\\u064Aa-zA-Z]{3}/.test(reason)){ta?.classList.add('bad');ta?.focus();toast('اكتب سبب الرفض (10 أحرف على الأقل) قبل ما تسجّل');return}}const u=API.recordInterview(pass,reason);render();toast(pass?'سجّلت المقابلة، وانتقل ملف ماجد للجنة تلقائيًا':'سجّلت الرفض، وتحوّل الملف للإدارة العليا',()=>{u();render()})},
 esc(b){const up=b.dataset.v==='1';const u=API.reviewEscalation(up);render();toast(up?'أيّدت الرفض، ويحتاج ماجد تحدي إضافي':'ألغيت الرفض، وانتقل الملف للجنة',()=>{u();render()})},""")
R("recordInterview(pass){","recordInterview(pass,reason){",0) if False else None

# =============== exceptional vote + plans move to top ===============
R("[['m','مدير القسم'],['h','هيا (الموارد البشرية)'],['c','المدير التنفيذي']].map(([k,n])=>`<div class=\"vote\"><span>${n}</span>${ex.votes[k]?'<span class=\"chip g\">وافق</span>':ex.status==='ok'?'':`<button",
  "[['m','مدير القسم'],['h','هيا (الموارد البشرية)'],['c','فيصل (الإدارة العليا)']].map(([k,n])=>`<div class=\"vote\"><span>${n}</span>${ex.votes[k]?'<span class=\"chip g\">وافق</span>':ex.status==='ok'?'':k==='c'?'<span class=\"chip y\">عند الإدارة العليا</span>':`<button")
R("""  ${p.st==='wait'?`<div class="sim"><span class="mut">محاكاة قرار الإدارة:</span><button class="btn" data-act="planOk" data-i="${pi}" style="min-height:40px">اعتمدت</button><button class="btn ghost" data-act="planRej" data-i="${pi}" style="min-height:40px;color:var(--ink)">رفضت</button></div>`:''}""",
  """  ${p.st==='wait'?`<p class="mut small" style="margin-top:8px">أُرسلت لمدير الإدارة العليا يعتمدها.</p>`:''}""")
R("'بانتظار اعتماد الإدارة'}</span></div>","'بانتظار اعتماد الإدارة العليا'}</span></div>")
R(" planOk(b){API.setPlanStatus(+b.dataset.i,'ok');render();toast('اعتمدت الإدارة الخطة، ووصل الموظفين إشعار')},",
  " planOk(b){API.setPlanStatus(+b.dataset.i,'ok');render();toast('اعتمدت الخطة، ووصل الموظفين وهيا إشعار')},")
R(" planRej(b){API.setPlanStatus(+b.dataset.i,'rej');render();toast('رفضت الإدارة الخطة، تقدرين تعدّلينها')},",
  " planRej(b){API.setPlanStatus(+b.dataset.i,'rej');render();toast('رفضت الخطة، ووصل هيا إشعار تعدّلها')},")

# notifications for mgr/haya/top
R("if(S.majed.status==='sent')it.push(['ترقية','ملف ماجد اكتمل وانتقل للجنة تلقائيًا.']);it.push(['تذكير تلقائي','تقرير أثر التدريب الربعي يطلع بعد 10 أيام.'])}",
  """if(S.majed.status==='sent')it.push(['ترقية','ملف ماجد اكتمل وانتقل للجنة تلقائيًا.']);it.push(['تذكير تلقائي','تقرير أثر التدريب الربعي يطلع بعد 10 أيام.'])}
 if(S.role==='top'){if(S.majed.status==='esc')it.push(['ترقية محوّلة','محمد رفض ترقية ماجد بسبب مكتوب، وتحتاج مراجعتك.']);S.plans.filter(p=>p.st==='wait').forEach(p=>it.push(['خطة تطوير',PROG[p.k].n+' تنتظر اعتمادك.']));if(S.exc.status!=='ok'&&!S.exc.votes.c)it.push(['ترقية استثنائية','سارة الزهراني تنتظر موافقتك.']);it.push(['موظف الشهر','النتيجة جاهزة للإعلان.'])}""")

# =============== analytics: 70-20-10, growth, honor, champions, drill ===============
ANA=r"""
/* ================= ANALYTICS · 70-20-10 · 30-60-90 · الشرف والأبطال ================= */
/* مؤشر التعلّم: 70% عملي + 20% تواصل وتبادل خبرات + 10% تعلّم رسمي (كل جزء من 100) */
const L3=i=>{if(i===0){const P=Math.min(100,35+(S.rep.status==='ok'?30:S.rep.status==='low'?12:0)+(S.cert.status==='ok'?20:S.cert.status==='back'?6:0)+(S.excel==='g'?8:0));
  const So=Math.min(100,25+(S.mentorBook?25:0)+Object.keys(S.ws).length*15+(S.applied&&Object.keys(S.applied).length?5:0));
  const F=Math.min(100,20+Object.keys(S.courses).length*15+Object.values(S.content).reduce((a,v)=>a+(v==='done'?15:8),0)+(S.cert.status==='ok'?15:0));return [P,So,F]}
 return [40+(i*37)%55,30+(i*53)%65,25+(i*29)%70]};
const learnIdx=i=>{const [P,So,F]=L3(i);return Math.round(.7*P+.2*So+.1*F)};
const L3SRC=[['عملي · 70%','تحديات معتمدة، وتدوير، وظل، ومهام فعلية'],['تواصل وتبادل خبرات · 20%','جلسات المرشد، والورش الداخلية، ونقل المعرفة'],['تعلّم رسمي · 10%','الدورات، والمحتوى، والشهادات']];
/* التطور: كم نقطة ارتفعت الجاهزية خلال آخر 90 يوم */
let R0=null;const G90=[0,6,11,3,9,14,5,8,2,12,4,7,10,1,13,6,9,3,15,5,8];
const growthOf=i=>{if(i===0){if(R0===null)R0=readyOf(0)-9;return readyOf(0)-R0}return G90[i]};
const byGrowth=ids=>[...ids].sort((a,b)=>(growthOf(b)-growthOf(a))||(learnIdx(b)-learnIdx(a)));
const rankOf=(ids,i)=>byGrowth(ids).indexOf(i)+1;
/* موظف الشهر: 50% التطور (15 نقطة = 100) + 50% مؤشر التعلّم */
const eomScore=i=>Math.round(.5*Math.min(100,growthOf(i)/15*100)+.5*learnIdx(i));
const eom=()=>EMP.map((e,i)=>i).sort((a,b)=>eomScore(b)-eomScore(a))[0];
/* البطل: يحقق كل الجدارات المطلوبة، والأعلى جاهزية ثم تعلّمًا */
const meetsAll=i=>Object.keys(SK).every(k=>compLv(i,k)>=SK[k].req);
const champOfDept=d=>{const ids=EMP.map((e,i)=>i).filter(i=>EMP[i].d===d);const full=ids.filter(meetsAll);const pool=full.length?full:ids;const w=[...pool].sort((a,b)=>(readyOf(b)-readyOf(a))||(learnIdx(b)-learnIdx(a)))[0];return {i:w,full:!!full.length}};
const CHSK=['cap','inv','ai','wms','data','lead'];
const champOfSkill=k=>EMP.map((e,i)=>i).sort((a,b)=>(compLv(b,k)-compLv(a,k))||(readyOf(b)-readyOf(a)))[0];
const CROWN='<svg viewBox="0 0 48 32" width="44" height="30" aria-hidden="true"><path d="M4 28 L2 8 L14 18 L24 3 L34 18 L46 8 L44 28Z" fill="#E3B34F" stroke="#8A6516" stroke-width="1.5" stroke-linejoin="round"/><circle cx="24" cy="4" r="2.6" fill="#F5D88A"/><circle cx="2.5" cy="8" r="2.2" fill="#F5D88A"/><circle cx="45.5" cy="8" r="2.2" fill="#F5D88A"/><rect x="4" y="24" width="40" height="4" fill="#B98A2C"/></svg>';
function champBoard(){return `<div class="card night reveal champs"><div class="row between"><div><span class="mut">لوحة الأبطال</span><h2 style="font-size:26px;margin:2px 0 0">أبطال الأقسام والمهارات</h2></div><button class="linkbtn" data-act="drill" data-k="champrule" style="color:var(--sand)">كيف يُختار البطل؟</button></div>
 <div class="crowns">${DEPTS.map((d,di)=>{const c=champOfDept(di);return `<button class="crown" data-act="pal" data-i="${c.i}">${CROWN}<b>${enm(c.i)}</b><span>بطل ${d}</span><span class="cr2">${c.full?'كل الجدارات مكتملة':'الأقرب للاكتمال'} · ${readyOf(c.i)}%</span></button>`}).join('')}</div>
 <h3 class="subh" style="color:var(--sand)">أبطال المهارات</h3><div class="skchamps">${CHSK.map(k=>{const i=champOfSkill(k);return `<button class="skc" data-act="pal" data-i="${i}"><span class="mut">${SK[k].n}</span><b>${enm(i)}</b><span class="mut">«${LV[compLv(i,k)-1]}»</span></button>`}).join('')}</div></div>`}
function eomCard(dark){const w=eom();return `<div class="card reveal eom ${dark?'night':''}"><div class="row between" style="align-items:center"><div style="display:flex;gap:14px;align-items:center">${CROWN}<div><span class="mut">موظف الشهر</span><h3 style="font-size:22px;margin:2px 0 0">${enm(w)}</h3><span class="mut">${DEPTS[EMP[w].d]} · تطور +${growthOf(w)} نقطة · مؤشر التعلّم ${learnIdx(w)}</span></div></div><button class="linkbtn" data-act="drill" data-k="eom">كيف انحسب؟</button></div></div>`}
function honorBoard(){const me=0,dIds=EMP.map((e,i)=>i).filter(i=>EMP[i].d===EMP[0].d),all=EMP.map((e,i)=>i);const rd=rankOf(dIds,me),ra=rankOf(all,me);const top=byGrowth(dIds).slice(0,3);
 return `<div class="card reveal"><div class="row between"><h3 style="font-size:20px">لوحة الشرف</h3><span class="mut">الترتيب حسب تطورك في آخر 90 يوم</span></div>
 <div class="g2 ranks"><button class="rk" data-act="drill" data-k="rankd"><span class="mut">ترتيبك في قسمك</span><b class="kufi">${rd} <small>من ${dIds.length}</small></b></button><button class="rk" data-act="drill" data-k="ranka"><span class="mut">ترتيبك في الشركة</span><b class="kufi">${ra} <small>من ${all.length}</small></b></button></div>
 <div class="podium">${top.map((i,n)=>`<div class="pd ${i===me?'me':''}"><span class="pn">${n+1}</span><b>${i===me?'أنت':enm(i)}</b><span class="mut">+${growthOf(i)} نقطة</span></div>`).join('')}</div>
 ${disc('وش يرفع ترتيبك؟','<ul class="plain"><li>كل تحدي معتمد يرفع جاهزيتك، والجاهزية هي أساس الترتيب.</li><li>الترتيب على التطور، مو على الأقدمية، فالجديد يقدر يتصدر.</li><li>عند التعادل يتقدم الأعلى في مؤشر التعلّم.</li></ul>')}</div>`}
function learnCard(i){const [P,So,F]=L3(i);const v=learnIdx(i);return `<div class="card reveal"><div class="row between"><h3 style="font-size:20px">مؤشر التعلّم 70-20-10</h3><button class="kbig" data-act="drill" data-k="learn">${v}<small> من 100</small></button></div>
 <div class="bars">${[P,So,F].map((x,j)=>`<div><div class="l"><span>${L3SRC[j][0]}</span><b>${x}</b></div>${bar(x,['var(--teen)','#C9A24A','#C3743F'][j])}<span class="mut small">${L3SRC[j][1]}</span></div>`).join('')}</div></div>`}
/* دورة 30-60-90 */
function cycleCard(){const day=45;const m=[['30 يوم · تعلّم','جلسة مع المرشد أو محتوى من شركتك',!!(S.mentorBook||Object.keys(S.content).length||Object.keys(S.ws).length||Object.keys(S.courses).length)],['60 يوم · طبّق','سلّم تحدي من شغلك أو شهادة تثبتها',['ok','low'].includes(S.rep.status)||['ok','back'].includes(S.cert.status)],['90 يوم · أثبت','مهارة توصل المطلوب، ومؤشر يتحسن عن البداية',S.lv.ai>=3||S.cert.status==='ok']];
 return `<div class="card reveal"><div class="row between"><h3 style="font-size:20px">دورتك 30-60-90</h3><span class="mut">اليوم ${day} من 90</span></div>${bar(day/90*100)}
 <div class="cyc">${m.map(([t,d,ok],j)=>{const due=(j+1)*30;const st=ok?'تمت':day>due?'متأخرة':day>=due-30?'الحين':'قادمة';return `<div class="cy ${ok?'ok':st==='متأخرة'?'late':''}"><span class="cyn">${ok?ICN.ok:j+1}</span><div><b>${t}</b><span class="mut">${d}</span></div><span class="chip ${ok?'g':st==='متأخرة'?'r':st==='الحين'?'y':''}">${st}</span></div>`}).join('')}</div>
 <p class="mut small" style="margin-top:8px">بداية الدورة: جاهزية ${readyOf(0)-growthOf(0)}% ← الحين ${readyOf(0)}%</p></div>`}
const planCycle=p=>{const avg=Math.round(p.sel.reduce((a,i)=>a+progOf(i),0)/p.sel.length);return `<div class="cyc mini">${[['30','تعلّم',avg>=20],['60','طبّق',avg>=60],['90','أثبت',avg>=100]].map(([d,t,ok])=>`<span class="chip ${ok?'g':''}">${AR?d:d} يوم · ${t}${ok?' ✓':''}</span>`).join('')}</div>`};
/* لوحات تفاعلية: كل رقم ينفتح على تفاصيله */
const KV={err:[2.1,3.4,2.6,3.1,2.4,2.9,2.2],late:[31,44,35,40,29,38,33],inv:[99.1,97.4,98.8,97.9,99.3,98.2,98.6],uph:[96,84,93,88,99,90,94],keep:[100,80,90,70,100,85,95]};
const UNIT={err:'%',late:' د',inv:'%',uph:'',keep:'%'};
const BAD={err:1,late:1,inv:-1,uph:-1,keep:-1};
function drillHTML(k){const T=team(),N=EMP.length,all=EMP.map((e,i)=>i);
 const list=(ids,val,fmt=v=>v)=>`<div class="pss">${ids.map(i=>`<button class="ps psb" data-act="pal" data-i="${i}"><span>${enm(i)}</span><span class="mut" style="color:#C3B8A6">${DEPTS[EMP[i].d]}</span><b>${fmt(val(i))}</b></button>`).join('')||'<p class="mut">ما فيه أحد.</p>'}</div>`;
 const head=(t,f,src)=>`<h2 id="mt" style="font-size:24px">${t}</h2>${f?`<p class="mut" style="color:#D9CFBE;margin:6px 0 0"><b style="color:var(--sand)">المعادلة:</b> ${f}</p>`:''}${src?`<p class="mut" style="color:#C3B8A6;margin:4px 0 0"><b>المصدر:</b> ${src}</p>`:''}`;
 if(k.startsWith('k:')){const q=k.slice(2);const X=KPIX[q];const ids=[...T].sort((a,b)=>BAD[q]*(KV[q][T.indexOf(b)]-KV[q][T.indexOf(a)]));return head(X[0],X[1],X[2])+`<p class="mut" style="color:#C3B8A6;margin:10px 0 0">الأقل أداءً أول:</p>`+list(ids,i=>KV[q][T.indexOf(i)],v=>v+UNIT[q])}
 if(k==='load'||k.startsWith('load:')){const ids=k==='load'?T:all.filter(i=>EMP[i].d===+k.split(':')[1]);return head(k==='load'?'عبء العمل':'عبء '+DEPTS[+k.split(':')[1]],KPIX.load[1],KPIX.load[2])+list([...ids].sort((a,b)=>loadOf(b)-loadOf(a)),loadOf,v=>v+'%')}
 if(k.startsWith('grp:')){const g=+k.split(':')[1];const ids=T.filter(i=>grpOf(readyOf(i))===g);return head(`${GRP[g][0]} (${ids.length})`,'الجاهزية = مجموع (وزن الجدارة × مستوى الموظف ÷ المستوى المطلوب)، وأعلى قيمة لكل جدارة 100%','أدلة الجدارات المعتمدة و360 ومؤشرات الأداء')+list(ids,readyOf,v=>v+'%')}
 if(k==='ready'){const ids=all.filter(i=>readyOf(i)>=80).sort((a,b)=>readyOf(b)-readyOf(a));return head(`جاهزون للترقية (${ids.length} من ${N})`,'الموظفين اللي جاهزيتهم 80% أو أكثر للوظيفة التالية','حساب الجاهزية من الجدارات وأوزانها')+list(ids,readyOf,v=>v+'%')}
 if(k==='ai'){const ids=all.filter(i=>lvOf(i,'ai')>=3);return head(`يستخدمون الذكاء الاصطناعي أسبوعيًا`,'الموظفين اللي سلّموا مهمة واحدة على الأقل بأداة ذكاء اصطناعي هالأسبوع ÷ كل الموظفين','سجل الاستخدام في تحديات دبره')+list(ids,i=>LV[lvOf(i,'ai')-1])}
 if(k==='plans'){return head('إكمال خطط التطوير','الخطط المكتملة ÷ الخطط المعتمدة','خطط التطوير في دبره')+`<div class="pss">${[...DONE.map(p=>[p.n,'مكتملة']),...S.plans.map(p=>[PROG[p.k].n,p.st==='ok'?'جارية':p.st==='rej'?'مرفوضة':'بانتظار الاعتماد'])].map(([n,st])=>`<div class="ps"><span>${n}</span><span></span><b>${st}</b></div>`).join('')}</div>`}
 if(k==='succ'){return head('أدوار حرجة لها خليفة','الأدوار الحرجة اللي لها خليفة جاهزيته 80% أو أكثر ÷ كل الأدوار الحرجة','خطة التعاقب')+`<div class="pss">${[['مخطط عمليات',`ماجد ${readyOf(1)}%`],['مشرف التبريد','ما فيه خليفة جاهز'],['قائد فريق التوزيع',`سارة ${readyOf(9)}%`]].map(([a,b])=>`<div class="ps"><span>${a}</span><span></span><b>${b}</b></div>`).join('')}</div>`}
 if(k==='learn'||k==='learnT'||k==='learnC'){const ids=k==='learnT'?T:all;if(k==='learn'){const [P,So,F]=L3(0);return head('مؤشر التعلّم 70-20-10','(70% × العملي) + (20% × التواصل وتبادل الخبرات) + (10% × التعلّم الرسمي)','تحديات دبره، والإرشاد والورش، والدورات والمحتوى')+`<div class="pss">${[P,So,F].map((x,j)=>`<div class="ps"><span>${L3SRC[j][0]}</span><span class="mut" style="color:#C3B8A6">${L3SRC[j][1]}</span><b>${x}</b></div>`).join('')}</div>`}
  return head('مؤشر التعلّم 70-20-10','(70% × العملي) + (20% × التواصل) + (10% × الرسمي)','تحديات دبره، والإرشاد والورش، والدورات والمحتوى')+list([...ids].sort((a,b)=>learnIdx(b)-learnIdx(a)),learnIdx)}
 if(k==='rankd'||k==='ranka'){const ids=k==='rankd'?all.filter(i=>EMP[i].d===EMP[0].d):all;return head(k==='rankd'?'ترتيب قسمك':'ترتيب الشركة','الترتيب حسب ارتفاع الجاهزية في آخر 90 يوم، وعند التعادل مؤشر التعلّم','حساب الجاهزية الأسبوعي')+list(byGrowth(ids),growthOf,v=>'+'+v)}
 if(k==='eom'){const ids=[...all].sort((a,b)=>eomScore(b)-eomScore(a)).slice(0,5);return head('موظف الشهر','(50% × التطور، و15 نقطة = 100) + (50% × مؤشر التعلّم)','حساب الجاهزية ومؤشر التعلّم')+list(ids,eomScore)}
 if(k==='champrule'){return head('كيف يُختار البطل؟','بطل القسم: موظف حقق كل الجدارات المطلوبة لوظيفته الجاية، وأعلى جاهزية، وعند التعادل الأعلى في مؤشر التعلّم. ولو ما فيه أحد مكتمل، يظهر «الأقرب للاكتمال». بطل المهارة: الأعلى مستوى فيها.','أدلة الجدارات المعتمدة')}
 if(k==='bud'){return head('الميزانية','المصروف = الخطط المنتهية + الخطط المعتمدة الجارية (بعد دعم هدف)','خطط التطوير')+`<div class="pss">${[...DONE.map(p=>[p.n,p.cost]),...S.plans.filter(p=>p.st==='ok').map(p=>[PROG[p.k].n,p.net])].map(([n,c])=>`<div class="ps"><span>${n}</span><span></span><b>${sar(c)}</b></div>`).join('')}</div>`}
 if(k==='esc'){return head('ملفات تنتظر قرارك','ترقيات رفضها المدير بسبب مكتوب، وخطط تنتظر الاعتماد','دبره')}
 return head('تفاصيل','','')}
function drill(k){modal(`<div class="psum">${drillHTML(k)}<button class="btn sand" data-act="closeModal" style="margin-top:14px">تمام</button></div>`)}

/* ================= TOP MANAGEMENT ================= */
V.top=()=>tabs('top',[['files','الملفات المحوّلة'],['plans','اعتماد الخطط'],['champs','الأبطال'],['overview','نظرة الشركة']])+({files:tFiles,plans:tPlans,champs:tChamps,overview:tOverview})[S.tab.top]();
function tFiles(){const m=S.majed,ex=S.exc;return `<div class="card night reveal hello"><span class="mut">الإدارة العليا · مستودعات الشرق</span><h1>حياك فيصل</h1><p style="color:#D9CFBE;margin:0">أي ترقية يرفضها مدير مباشر توصلك مع السبب، عشان القرار ما يعتمد على شخص واحد.</p></div>
 <div class="card reveal"><h2 style="font-size:22px">ترقيات رفضها المدير</h2>${m.status==='esc'?`<div class="pos"><div><b>ماجد القحطاني · مشرف مستودع ← مخطط عمليات</b><span class="mut">رفضه محمد بعد المقابلة · جاهزية ${readyOf(1)}% · 360: 4.4 · بدون فجوة تحيز</span><div class="banner y" style="margin-top:8px"><b>سبب المدير:</b><span style="flex:1">${esc(m.reason)}</span></div>${critList([['أدلة الجدارات الفنية','4 تحديات معتمدة تلقائيًا'],['تقييم 360','متّسق مع الأدلة'],['سجل المدير','أول رفض لموظف أدلته قوية هالسنة']],[1,1,1])}</div><div class="row" style="gap:8px;margin-top:10px"><button class="btn" data-act="esc" data-v="0">ألغِ الرفض وارفع الملف للجنة</button><button class="btn ghost" data-act="esc" data-v="1" style="color:var(--ink)">أيّد الرفض: تحدي إضافي</button></div></div>`:`<div class="empty"><b style="display:block;font-size:18px">ما فيه ملفات محوّلة</b><p class="mut">${m.status==='sent'&&m.top?'راجعت ملف ماجد، وانتقل للجنة.':m.status==='retry'?'أيّدت رفض ماجد، ويحتاج تحدي إضافي.':'لما يرفض مدير ترقية موظف بعد المقابلة، يوصلك الملف هنا مع السبب.'}</p><button class="btn dark" data-act="goMgr">جرّب كأنك محمد</button></div>`}</div>
 <div class="card reveal"><div class="row between"><h3 style="font-size:20px">ترقية استثنائية · سارة الزهراني</h3><span class="chip ${ex.status==='ok'?'g':'y'}">${ex.status==='ok'?'معتمدة':Object.values(ex.votes).filter(Boolean).length+' من 3 موافقات'}</span></div><p class="mut" style="margin:6px 0">من مشرفة توزيع إلى مديرة توزيع. وفّرت 340 ألف ريال بالسنة، وأثبتت 4 من 5 جدارات المنصب الأعلى.</p>${ex.votes.c?'<span class="chip g">وافقت</span>':ex.status==='ok'?'':'<button class="btn" data-act="vote" data-k="c" style="min-height:44px">وافق</button>'}</div>`}
function tPlans(){const W=S.plans.map((p,pi)=>[p,pi]).filter(([p])=>p.st==='wait');const used=usedBudget();return `<div class="g3">${[['الميزانية السنوية',sar(BUDGET.total),'bud'],['المصروف',sar(used),'bud'],['المتبقي',sar(BUDGET.total-used),'bud']].map(([n,v,k])=>kpi(n,v,'اضغط للتفاصيل',{drill:k})).join('')}</div>
 <div class="card reveal"><h2 style="font-size:22px">خطط تنتظر اعتمادك</h2>${W.length?W.map(([p,pi])=>{const P=PROG[p.k];const sa=p.sel.filter(i=>isSa(EMP[i])).length;return `<div class="pos"><div><b>${P.n}</b><span class="mut">${p.sel.length} موظف (${sa} سعودي) · صافي التكلفة ${sar(p.net)}${p.hadaf?` · دعم هدف ${sar(p.hadaf)}`:''} · من هيا</span>${p.net>BUDGET.total-used?'<span class="chip r" style="margin-top:6px;width:fit-content">تتجاوز المتبقي</span>':''}</div><div class="row" style="gap:6px"><button class="btn" data-act="planOk" data-i="${pi}" style="min-height:42px">اعتمد</button><button class="btn ghost" data-act="planRej" data-i="${pi}" style="min-height:42px;color:var(--ink)">ارفض</button></div></div>`}).join(''):`<div class="empty"><b style="display:block;font-size:18px">ما فيه خطط تنتظرك</b><p class="mut">لما ترسل هيا خطة تطوير، تطلع هنا تعتمدها أو ترفضها.</p><button class="btn dark" data-act="goHaya">جرّب كأنك هيا</button></div>`}</div>`}
function tChamps(){return champBoard()+eomCard(false)}
function tOverview(){const N=EMP.length,all=EMP.map((e,i)=>i);const avgL=Math.round(all.reduce((a,i)=>a+learnIdx(i),0)/N);const pend=(S.majed.status==='esc'?1:0)+S.plans.filter(p=>p.st==='wait').length;
 return `<div class="g4">${[['جاهزون للترقية',`${all.filter(i=>readyOf(i)>=80).length} من ${N}`,'اضغط للأسماء','ready'],['متوسط مؤشر التعلّم',`${avgL}`,'70-20-10 · اضغط للتفاصيل','learnC'],['يستخدمون الذكاء الاصطناعي',`${Math.round(all.filter(i=>lvOf(i,'ai')>=3).length/N*100)}%`,'أسبوعيًا · اضغط للأسماء','ai'],['ملفات تنتظر قرارك',`${pend}`,'ترقيات وخطط','esc']].map(([n,v,w,k],j)=>kpi(n,v,w,{drill:k,night:j===0})).join('')}</div>
 <div class="g3">${DEPTS.map((d,di)=>{const ids=all.filter(i=>EMP[i].d===di);const load=Math.round(ids.reduce((a,i)=>a+loadOf(i),0)/ids.length);const rd=Math.round(ids.reduce((a,i)=>a+readyOf(i),0)/ids.length);return `<button class="card reveal dcard" data-act="drill" data-k="load:${di}"><span class="mut">${d} · ${ids.length} موظفين</span><div class="big" style="margin:6px 0;color:${load>105?'#B4532E':'var(--teenD)'}">${load}%</div><span class="mut">متوسط العبء · متوسط الجاهزية ${rd}%</span>${bar(load/1.4,load>105?'#B4532E':'')}</button>`}).join('')}</div>
 ${eomCard(true)}`}
"""
i=s.index("/* ================= HAYA ================= */")
s=s[:i]+ANA+"\n"+s[i:]

# kpi drill support
R("const kpi=(n,v,sub,o={})=>`<div class=\"card reveal kpi2 ${o.night?'night':''}\"><span class=\"mut\">${n}</span><div class=\"big\">${v}</div>${o.p!=null?bar(o.p,o.col):''}<span class=\"mut\">${sub}</span></div>`;",
  "const kpi=(n,v,sub,o={})=>{const tag=o.drill?'button':'div';return `<${tag} class=\"card reveal kpi2 ${o.night?'night':''} ${o.drill?'drillable':''}\" ${o.drill?`data-act=\"drill\" data-k=\"${o.drill}\" aria-label=\"${n}: ${v}، اضغط للتفاصيل\"`:''}><span class=\"mut\">${n}</span><div class=\"big\">${v}</div>${o.p!=null?bar(o.p,o.col):''}<span class=\"mut\">${sub}</span>${o.drill?'<span class=\"dhint\">التفاصيل ←</span>':''}</${tag}>`};")
# employee perf: drill + learning + honor
R("""function empPerf(){const k=[['أخطاء التجهيز في فريقك','2.6%','الهدف 2.5%',90],['متوسط التأخير','34 د','الهدف 30 د',82],['دقة الجرد','98.6%','الهدف 99%',96],['المحافظة على المهارات',S.excel==='g'?'100%':'80%','تدخل في تقييمك السنوي',S.excel==='g'?100:80]];
 return `<div class="g4">${k.map(([n,v,t,p])=>kpi(n,v,t,{p,col:p>=95?'var(--ok)':''})).join('')}</div>""",
"""function empPerf(){const k=[['أخطاء التجهيز في فريقك','2.6%','الهدف 2.5%',90,'k:err'],['متوسط التأخير','34 د','الهدف 30 د',82,'k:late'],['دقة الجرد','98.6%','الهدف 99%',96,'k:inv'],['المحافظة على المهارات',S.excel==='g'?'100%':'80%','تدخل في تقييمك السنوي',S.excel==='g'?100:80,'k:keep']];
 return `<div class="g4">${k.map(([n,v,t,p,d])=>kpi(n,v,t,{p,col:p>=95?'var(--ok)':'',drill:d})).join('')}</div>
 <div class="g2">${learnCard(0)}${honorBoard()}</div>
 ${eomCard(false)}""")
# employee path: 30-60-90 after the g2
R(""" <div class="card reveal">
  <div class="row between"><h2 style="font-size:24px">جداراتي وطريقي للترقية</h2>""",""" ${cycleCard()}
 <div class="card reveal">
  <div class="row between"><h2 style="font-size:24px">جداراتي وطريقي للترقية</h2>""")
# manager perf drill + team learning
R("""function mgrPerf(){const T=team();const K=[['أخطاء التجهيز','2.8%','2.5%',89],['متوسط التأخير','37 د','30 د',81],['دقة الجرد','98.1%','99%',95],['طلبات في الساعة','92','95',97]];
 return `<div class="g4">${K.map(([n,v,t,p])=>kpi(n,v,`الهدف ${t}`,{p,col:p>=95?'var(--ok)':''})).join('')}</div>""",
"""function mgrPerf(){const T=team();const K=[['أخطاء التجهيز','2.8%','2.5%',89,'k:err'],['متوسط التأخير','37 د','30 د',81,'k:late'],['دقة الجرد','98.1%','99%',95,'k:inv'],['طلبات في الساعة','92','95',97,'k:uph']];
 return `<div class="g4">${K.map(([n,v,t,p,d])=>kpi(n,v,`الهدف ${t}`,{p,col:p>=95?'var(--ok)':'',drill:d})).join('')}</div>""")
R("""<div class="row between"><h3 style="font-size:20px">تحليل عبء العمل</h3><span class="mut">ساعات فعلية من 40 أسبوعيًا</span></div>""",
  """<div class="row between"><h3 style="font-size:20px">تحليل عبء العمل</h3><button class="linkbtn" data-act="drill" data-k="load">ساعات فعلية من 40 · التفاصيل</button></div>""")
# manager team: color legend clickable + champions + team learning
R("""function colorStrip(ids){const c=[0,0,0,0];ids.forEach(i=>c[grpOf(readyOf(i))]++);return `<div class="cstrip">${c.map((n,g)=>n?`<span style="flex:${n};background:${GRP[g][2]}" title="${GRP[g][0]}"></span>`:'').join('')}</div><div class="clegend">${GRP.map((g,j)=>`<span><i style="background:${g[2]}"></i>${g[0]} <b>${c[j]}</b></span>`).join('')}</div>`}""",
  """function colorStrip(ids){const c=[0,0,0,0];ids.forEach(i=>c[grpOf(readyOf(i))]++);return `<div class="cstrip">${c.map((n,g)=>n?`<button style="flex:${n};background:${GRP[g][2]}" data-act="drill" data-k="grp:${g}" aria-label="${GRP[g][0]}: ${n}"></button>`:'').join('')}</div><div class="clegend">${GRP.map((g,j)=>`<button data-act="drill" data-k="grp:${j}"><i style="background:${g[2]}"></i>${g[0]} <b>${c[j]}</b></button>`).join('')}</div>`}""")
R(""" <div class="card reveal">${promoFile()}</div>
 <div class="banner y reveal">""",""" <div class="card reveal">${promoFile()}</div>
 ${champBoard()}
 <div class="banner y reveal">""")
# haya talent KPIs drill
R("""[['يستخدمون الذكاء الاصطناعي أسبوعيًا',`${S.lv.ai>=3?43:41}%`,'قبل: 18%',1],['أكملوا خطط التطوير',`${S.plans.some(p=>p.st==='ok')?70:64}%`,'قبل: 22%'],['جاهزون للترقية',`${EMP.filter((e,i)=>readyOf(i)>=80).length} من ${N}`,'قبل دبره: 1'],['أدوار حرجة لها خليفة','2 من 3','الهدف: 3 من 3']].map(([n,v,w,nt])=>kpi(n,v,w,{night:nt})).join('')}""",
  """[['يستخدمون الذكاء الاصطناعي أسبوعيًا',`${S.lv.ai>=3?43:41}%`,'قبل: 18%',1,'ai'],['أكملوا خطط التطوير',`${S.plans.some(p=>p.st==='ok')?70:64}%`,'قبل: 22%',0,'plans'],['جاهزون للترقية',`${EMP.filter((e,i)=>readyOf(i)>=80).length} من ${N}`,'قبل دبره: 1',0,'ready'],['أدوار حرجة لها خليفة','2 من 3','الهدف: 3 من 3',0,'succ']].map(([n,v,w,nt,d])=>kpi(n,v,w,{night:nt,drill:d})).join('')}""")
# haya needs dept cards drill
R("""return `<div class="card reveal"><span class="mut">${d}</span><div class="big" style="margin:6px 0;color:${load>105?'#B4532E':'var(--teenD)'}">${load}%</div><span class="mut">متوسط العبء · ${ids.length} موظفين</span>${bar(load/1.4,load>105?'#B4532E':'')}</div>`}).join('')}</div>""",
  """return `<button class="card reveal dcard" data-act="drill" data-k="load:${di}"><span class="mut">${d}</span><div class="big" style="margin:6px 0;color:${load>105?'#B4532E':'var(--teenD)'}">${load}%</div><span class="mut">متوسط العبء · ${ids.length} موظفين · التفاصيل ←</span>${bar(load/1.4,load>105?'#B4532E':'')}</button>`}).join('')}</div>""")
# haya dev: company learning split + plan cycle
R("""  <div class="card reveal"><div class="row between"><h3 style="font-size:20px">خطط التطوير</h3>""",
  """  <div class="card reveal"><div class="row between"><h3 style="font-size:20px">مؤشر التعلّم في الشركة · 70-20-10</h3><button class="kbig" data-act="drill" data-k="learnC">${Math.round(EMP.reduce((a,e,i)=>a+learnIdx(i),0)/N)}<small> متوسط</small></button></div><div class="bars">${[0,1,2].map(j=>{const v=Math.round(EMP.reduce((a,e,i)=>a+L3(i)[j],0)/N);return `<div><div class="l"><span>${L3SRC[j][0]}</span><b>${v}</b></div>${bar(v,['var(--teen)','#C9A24A','#C3743F'][j])}</div>`}).join('')}</div></div>
  <div class="card reveal"><div class="row between"><h3 style="font-size:20px">خطط التطوير</h3>""")
R("""${p.st==='ok'?`<div style="margin-top:12px"><div class="l row between"><span>تقدّم الخطة</span><b>${avg}%</b></div>${bar(avg)}""",
  """${p.st==='ok'?`<div style="margin-top:12px"><div class="l row between"><span>تقدّم الخطة</span><b>${avg}%</b></div>${bar(avg)}${planCycle(p)}""")
# budget tiles in mgr budget clickable
R("""<div class="g3 tiles"><div><span class="mut">الميزانية السنوية</span><b class="kufi">${sar(BUDGET.total)}</b></div><div><span class="mut">المصروف</span><b class="kufi">${sar(used)}</b></div>""",
  """<div class="g3 tiles"><div><span class="mut">الميزانية السنوية</span><b class="kufi">${sar(BUDGET.total)}</b></div><button data-act="drill" data-k="bud" class="tilebtn"><span class="mut">المصروف · التفاصيل</span><b class="kufi">${sar(used)}</b></button>""")

# ACT handlers
R(" course(b){"," drill(b){drill(b.dataset.k)},\n pal(b){palmSummary(+b.dataset.i)},\n goHaya(){S.role='haya';S.tab.haya='dev';render()},goMgr(){S.role='mgr';S.tab.mgr='team';render()},\n course(b){")

# CSS
R("/* v8 */",r"""/* v8 */
.drillable{cursor:pointer;text-align:start;border:0;font:inherit;color:inherit;transition:transform .25s var(--ease),box-shadow .25s}.drillable:hover{transform:translateY(-3px)}.drillable:focus-visible{outline:3px solid var(--teenL)}
.dhint{font-size:12.5px;font-weight:700;color:var(--teen)}.kpi2.night .dhint{color:var(--sand)}
.dcard{border:0;font:inherit;color:inherit;text-align:start;cursor:pointer;display:block;width:100%}
.clegend button{background:none;border:0;font:inherit;color:inherit;cursor:pointer;padding:2px 0;display:inline-flex;align-items:center}
.cstrip button{border:0;cursor:pointer;padding:0;min-height:0}
.tilebtn{border:0;font:inherit;color:inherit;text-align:start;cursor:pointer}
.psb{width:100%;background:none;border:0;border-top:1px solid rgba(241,231,214,.1);font:inherit;color:inherit;text-align:start;cursor:pointer}.psb:hover{background:rgba(241,231,214,.06)}
.kbig{border:0;background:var(--teen);color:#fff;border-radius:16px;padding:6px 14px;font:800 26px/1.1 'Kufam';cursor:pointer}.kbig small{font:600 13px 'IBM Plex Sans Arabic'}
.champs .crowns{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:16px}
.crown{background:linear-gradient(180deg,rgba(227,179,79,.16),rgba(227,179,79,.04));border:1px solid rgba(227,179,79,.35);border-radius:22px;padding:16px 10px;display:flex;flex-direction:column;align-items:center;gap:4px;color:var(--jes);font:inherit;cursor:pointer;text-align:center}
.crown b{font:800 18px 'Kufam';color:#F5D88A}.crown span{font-size:13.5px}.crown .cr2{color:#C3B8A6;font-size:12.5px}
.skchamps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:8px}
.skc{background:rgba(241,231,214,.06);border:0;border-radius:16px;padding:10px 12px;display:flex;flex-direction:column;gap:2px;text-align:start;font:inherit;color:var(--jes);cursor:pointer}.skc .mut{color:#C3B8A6}
@media(max-width:700px){.champs .crowns,.skchamps{grid-template-columns:1fr 1fr}}
.eom .mut{display:block}
.ranks{gap:10px;margin-top:10px}.rk{background:#F7EFE2;border:0;border-radius:18px;padding:12px 14px;text-align:start;font:inherit;color:inherit;cursor:pointer;display:flex;flex-direction:column;gap:2px}.rk b{font-size:30px;color:var(--teenD)}.rk small{font-size:14px;color:var(--mut)}
.podium{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:12px 0 4px}.pd{background:#F7EFE2;border-radius:16px;padding:10px;display:flex;flex-direction:column;align-items:center;gap:2px;text-align:center}.pd.me{background:#E6F1EA;outline:2px solid var(--ok)}.pn{font:800 20px 'Kufam';color:#B98A2C}
.cyc{display:grid;gap:8px;margin-top:12px}.cy{display:flex;align-items:center;gap:12px;background:#F7EFE2;border-radius:16px;padding:10px 14px}.cy>div{flex:1;min-width:0}.cy b{display:block}.cyn{width:30px;height:30px;border-radius:50%;display:grid;place-items:center;background:#fff;font-weight:800;flex:none}.cy.ok .cyn{background:var(--ok);color:#fff}.cy.ok .cyn svg{width:16px}
.cyc.mini{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
""",1)
assert '�' not in s
open(P,'w',encoding='utf8').write(s);print('ok')
