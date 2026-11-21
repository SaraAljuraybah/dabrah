import sys,re
P='/home/claude/proto/v9.html'
s=open(P,encoding='utf8').read()
def R(old,new,cnt=1):
    global s
    n=s.count(old)
    if n!=cnt: sys.exit(f'COUNT {n}!={cnt}: {old[:100]}')
    s=s.replace(old,new)
def cut(start,end,new=''):
    """replace from start marker up to (not incl.) end marker"""
    global s
    i=s.index(start);j=s.index(end,i)
    s=s[:i]+new+s[j:]

# ---------- landing ----------
R("يثبتها بتحدي من شغله، ويعتمدها مديره بضغطة.","يثبتها بتحدي من شغله، وتُعتمد تلقائيًا بمعايير معلنة.")
R("<b>يعتمدك مديرك</b><span>الذكاء الاصطناعي يقترح، والمدير يقرر</span>","<b>تُعتمد تلقائيًا</b><span>بمعايير معلنة، بدون انطباعات</span>")
R("المهارة مربوطة بسلّم الشركة الوظيفي، والمدير يشوف الدليل ويعتمد بضغطة، فتُحسب مباشرة في ملف الترقية.",
  "المهارة مربوطة بسلّم الشركة الوظيفي، وتُعتمد تلقائيًا بمعايير معلنة يعرفها الموظف ومديره، فتُحسب مباشرة في ملف الترقية. ودور المدير مقابلة قبل الترقية يتأكد فيها إن الموظف حلّ تحدياته بنفسه.")
R('<h3 style="font-size:20px;margin-bottom:6px">الآلة تقترح والمدير يقرر</h3><p style="color:var(--mut);margin:0">ما فيه تقييم آلي بدون علم الموظف.</p>',
  '<h3 style="font-size:20px;margin-bottom:6px">معايير معلنة بدل الانطباع</h3><p style="color:var(--mut);margin:0">الاعتماد تلقائي بمعايير يعرفها الموظف، وما فيه تقييم بدون علمه. والترقية النهائية عند لجنة الموارد البشرية.</p>')
R("سجّل دخولك، وحل أول تحدي، وخلّ مديرك يعتمدك.","سجّل دخولك، وحل أول تحدي، وشوف مهارتك تُعتمد.")

# ---------- state ----------
R("rep:{status:'idle',note:''},cert:{status:'idle'},queue:[],","rep:{status:'idle'},cert:{status:'idle'},")
R("majed:{interview:false,status:'open',reason:''},","majed:{interview:null,status:'open'},")
R("dec:'اعتمد «سنع»',when:'قبل أسبوعين'","dec:'اعتماد تلقائي «سنع» (7 من 8)',when:'قبل أسبوعين'")
R("dec:'رجّعها: معرفة نظرية بدون تطبيق'","dec:'سُجّلت نظرية تلقائيًا (2 من 4)'")

# ---------- API: everything automatic ----------
a=s.index(" submitReport(sub){");b=s.index(" // POST /skills/:id/renewals")
s=s[:a]+r""" submitReport(sub){S.attempts++;S.rep.sub=sub;const prev=S.lv.ai;
  if(sub.score>=7){S.rep.status='ok';S.lv.ai=Math.max(prev,3);const fr=3+(prev<3?5:0);S.fr+=fr;S.newUC=true;S.hist.unshift({who:enm(0),what:'تقرير الأداء الأسبوعي',dec:`اعتماد تلقائي «سنع» (${sub.score} من 8)`,when:'اليوم',ok:1});return {lv:3,fr}}
  S.rep.status='low';S.fr+=1;S.hist.unshift({who:enm(0),what:'تقرير الأداء الأسبوعي',dec:`سُجّل تلقائيًا «شاطر» (${sub.score} من 8)`,when:'اليوم',ok:0});return {lv:2,fr:1}},
 // POST /submissions  {employeeId, skillId, type:'certificate', title, issuer, date, fileUrl, answers[], score}  → قرار تلقائي
 submitCert(c){const res=certResult(c.k,c.score);S.cert={...S.cert,...c,status:c.score>2?'ok':'back'};
  if(c.score>2){const prev=S.lv[c.k];S.lv[c.k]=res.lv;const met=res.lv>=SK[c.k].req&&prev<SK[c.k].req;const fr=3+(met?5:0);S.fr+=fr;S.hist.unshift({who:enm(0),what:'شهادة خارجية · '+SK[c.k].n,dec:`اعتماد تلقائي «${LV[res.lv-1]}» (${c.score} من 4)`,when:'اليوم',ok:1});return {ok:true,lv:res.lv,req:SK[c.k].req,fr}}
  S.cert.note='سُجّلت كمعرفة نظرية. طبّق في المستودع، ثم أعد تحدي المواقف العملية.';S.hist.unshift({who:enm(0),what:'شهادة خارجية · '+SK[c.k].n,dec:`سُجّلت نظرية تلقائيًا (${c.score} من 4)`,when:'اليوم',ok:0});return {ok:false}},
"""+s[b:]
# promotion: interview only; nomination is automatic
a=s.index(" recordInterview(){");b=s.index(" // POST /rotations/:id/approve")
s=s[:a]+r""" recordInterview(pass){const m=S.majed;m.interview=pass?'pass':'fail';if(pass){m.status='sent';S.hist.unshift({who:'ماجد القحطاني',what:'ملف ترقية · مخطط عمليات',dec:'اكتمل الملف وانتقل للجنة تلقائيًا',when:'اليوم',ok:1})}else{m.status='retry';S.hist.unshift({who:'ماجد القحطاني',what:'مقابلة الترقية',dec:'ما أثبت: تحدي إضافي ثم مقابلة ثانية',when:'اليوم',ok:0})}
  return ()=>{m.interview=null;m.status='open';S.hist.shift()}},
"""+s[b:]
R("// PATCH /promotions/:id  {interview:true}","// PATCH /promotions/:id  {interview:'pass'|'fail'}  → لو نجح ينتقل الملف للجنة تلقائيًا")

# remove manual decision helpers
cut("function decideCert(","/* ---------- event wiring ---------- */")
a=s.index("function decideBtn(b,approve)");b=s.index("\n",a);s=s[:a]+s[b+1:]
cut("function reqCard(q)","function mgrPerf(){")

# ---------- ACT ----------
R(" resubmit(){S.step=2;curText=S.rep.sub?.text||'';drawer(true)},\n","")
R("""  if(r.auto)celebrate({lv:3,req:3,skill:SK.ai.n,fr:r.fr,by:'اعتُمدت تلقائيًا'});else toast('سلّمت التحدي لمحمد. السعف يُضاف بعد اعتماده.')},""",
  """  if(r.lv===3)celebrate({lv:3,req:3,skill:SK.ai.n,fr:r.fr,by:'اعتُمدت تلقائيًا'});else toast(`سُجّل تلقائيًا «شاطر» (+1 سعفة). ${S.attempts<2?'تقدر تحاول مرة ثانية هالشهر.':'تقدر تحاول الشهر الجاي.'}`)},""")
R("""API.submitCert({k:S.cert.k,title:S.cert.title,issuer:S.cert.issuer,date:S.cert.date,file:S.cert.file,ans,score});drawer(false);render();toast(`جاوبت ${score} من 4. وصلت شهادتك لمحمد مع نتيجة التحدي.`)},""",
  """const r=API.submitCert({k:S.cert.k,title:S.cert.title,issuer:S.cert.issuer,date:S.cert.date,file:S.cert.file,ans,score});drawer(false);render();if(r.ok)celebrate({lv:r.lv,req:r.req,skill:SK[S.cert.k].n,fr:r.fr,by:'اعتُمدت شهادتك تلقائيًا'});else toast(`جاوبت ${score} من 4، فسُجّلت الشهادة معرفة نظرية.`)},""")
R(" approve(b){decideBtn(b,true)},askEdit(b){decideBtn(b,false)},\n","")
a=s.index(" interview(){API.recordInterview()");b=s.index(" rot(b){",a)
s=s[:a]+""" interview(b){const pass=b.dataset.v==='1';const u=API.recordInterview(pass);render();toast(pass?'سجّلت المقابلة، وانتقل ملف ماجد للجنة تلقائيًا':'سجّلت المقابلة: يحتاج تحدي إضافي',()=>{u();render()})},
"""+s[b:]

# ---------- employee path ----------
R("""const nx=rs==='sent'?['بانتظار اعتماد محمد','تقريرك عند محمد يراجعه.',0]:rs==='edit'?['عدّل تقريرك وسلّمه','محمد رجّعه لك بملاحظة، تلقاها فوق.',0]:rs==='ok'?""",
  """const nx=rs==='low'?['تقرير الأداء: «شاطر»',S.attempts<2?'سُجّل تلقائيًا. حسّن تقريرك وحاول مرة ثانية.':'سُجّل تلقائيًا. تقدر تحاول الشهر الجاي.',S.attempts<2?1:0]:rs==='ok'?""")
a=s.index(" ${rs==='edit'?`<div class=\"banner y reveal\"><b>محمد طلب تعديل:</b>");b=s.index("\n",a);s=s[:a]+s[b+1:]
R("${cs==='sent'?'شهادتك عند محمد':cs==='ok'?'شهادتك حُسبت':'عندك شهادة؟'}","${cs==='ok'?'شهادتك حُسبت':cs==='back'?'شهادتك سُجّلت نظرية':'عندك شهادة؟'}")
R("${cs==='sent'?'أثبتها بالتحدي، وتنتظر اعتماده.':cs==='ok'?","${cs==='back'?'طبّقها في شغلك، وأعد تحدي المواقف.':cs==='ok'?")
R("لو الدليل كامل يُعتمد تلقائيًا","الاعتماد تلقائي")
R("ولو التقييم عالي والأداء ضعيف يوصل تنبيه لمديرك.","ولو التقييم عالي والأداء ضعيف يوصل تنبيه للموارد البشرية.")
R("التجربة مؤقتة أول، ومديرك الحالي ما يقدر يمنعك بدون سبب مكتوب.","التجربة مؤقتة أول، والانتقال ما يحتاج موافقة مديرك الحالي.")

# ---------- report drawer ----------
R("8 من 8 = يُعتمد «سنع» تلقائيًا · 7 = «سنع» بعد مراجعة محمد · 5 أو 6 = يبقى «شاطر» · أقل من 5 ما يُقبل",
  "الاعتماد تلقائي: 7 أو 8 = «سنع» · 5 أو 6 = «شاطر» · أقل من 5 ما يُقبل")
R("${a.score===8?'يُعتمد تلقائيًا: سنع':a.score===7?'المقترح: سنع (يراجعه محمد)':a.ok?'المقترح: يبقى شاطر':'ما يُقبل بعد'}",
  "${a.score>=7?'يُعتمد تلقائيًا: سنع':a.ok?'يُسجّل تلقائيًا: شاطر':'ما يُقبل بعد'}")
R("$('#subBtn').textContent=a.score===8?'سلّم (اعتماد تلقائي)':'سلّم لمحمد'","$('#subBtn').textContent=a.score>=7?'سلّم (اعتماد تلقائي)':'سلّم'")
R("""<button class="btn" data-act="certSend">سلّم لمحمد</button>""","""<button class="btn" data-act="certSend">سلّم</button>""")
R("أربعة مواقف من شغل المستودع. 4 من 4 = مهارة عملية مثبتة","أربعة مواقف من شغل المستودع، والقرار تلقائي: 4 من 4 = مهارة عملية مثبتة")

# ---------- manager ----------
R("""function mgrTeam(){const pend=S.queue.filter(q=>q.st==='pending');const T=team();return `""","""function mgrTeam(){const T=team();return `""")
R("""<p style="color:#D9CFBE;margin:0">${pend.length?`عندك ${pend.length===1?'طلب واحد':pend.length+' طلبات'} ينتظرك.`:'ما عندك طلبات معلّقة.'} والمهارات الفنية ذات الدليل الكامل يُعتمد أغلبها تلقائيًا.</p>""",
  """<p style="color:#D9CFBE;margin:0">الاعتمادات كلها تلقائية بمعايير معلنة، ودورك مقابلة الترقية.</p>""")
a=s.index("""  <div class="card reveal"><h2 style="font-size:22px;margin-bottom:12px">طلبات الاعتماد</h2>""");b=s.index("\n",a)
s=s[:a]+"""  <div class="card reveal"><div class="row between"><h2 style="font-size:22px">آخر الاعتمادات التلقائية</h2><span class="mut">${S.hist.length}</span></div><div class="hist" style="margin-top:10px">${S.hist.slice(0,5).map(h=>`<div class="hi"><span class="hd ${h.ok?'ok':'no'}">${h.ok?ICN.ok:ICN.no}</span><div><b>${h.who}</b><span class="mut">${h.what}</span></div><span>${h.dec}</span><span class="mut">${h.when}</span></div>`).join('')}</div><p class="mut small" style="margin-top:8px">النظام يقرر بمعايير معلنة، والموظف يشوف ليش أخذ كل مستوى.</p></div>"""+s[b:]
a=s.index(""" <div class="card reveal">${disc(`<b class="kufi" style="font-size:20px">سجل القرارات</b>""");b=s.index("\n",a);s=s[:a]+s[b+1:]
# promo file
a=s.index("function promoFile(){");b=s.index("function mgrPerf(){")
s=s[:a]+r"""function promoFile(){const m=S.majed,rd=readyOf(1);const checks=[['أدلة الجدارات الفنية','4 تحديات معتمدة تلقائيًا، آخرها «ذيب» في المخزون',true],['تقييم 360','4.4 من 5 من 5 زملاء، ومتّسق مع الأدلة',true],['كشف التحيز','ما فيه فجوة بين التقييم والأداء',true],['مقابلة الترقية','يشرح لك تحدي حلّه، عشان تتأكد إنه حلّه بنفسه',m.interview==='pass']];const auto=checks.slice(0,3).every(c=>c[2]);
 const chip=m.status==='sent'?['g','انتقل للجنة تلقائيًا']:m.status==='retry'?['r','يحتاج تحدي إضافي']:['y',auto?'بانتظار مقابلتك':'الأدلة ما اكتملت'];
 return `<div class="row between"><div><h2 style="font-size:22px">ملف ترقية · ماجد القحطاني</h2><span class="mut">مشرف مستودع ← مخطط عمليات · جاهزية ${rd}%</span></div><span class="chip ${chip[0]}">${chip[1]}</span></div>
 ${disc('افتح ملف الترقية',critList(checks.map(c=>[c[0],c[1]]),checks.map(c=>c[2]))+(m.status==='open'&&auto?`<div class="row" style="margin-top:12px"><button class="btn" data-act="interview" data-v="1">المقابلة تمت وأثبت</button><button class="btn ghost" data-act="interview" data-v="0">ما أثبت في المقابلة</button></div>`:'')+`<p class="mut small" style="margin-top:8px">النظام يجهّز الملف تلقائيًا من الأدلة و360 وكشف التحيز. دورك المقابلة فقط، ولو أثبت فيها ينتقل الملف للجنة الموارد البشرية تلقائيًا.</p>`)}`}
"""+s[b:]

# ---------- governance ----------
R("""ما فيه تظلّمات. لو مدير رفض موظف أدلته قوية، يتحوّل الملف هنا تلقائيًا.""","""ما فيه تظلّمات. لو اعترض موظف على قرار تلقائي أو على نتيجة مقابلة، يطلع هنا.""")
R("""<h3 style="font-size:20px">رصد تحيز المديرين</h3>${[['محمد · المستودع المركزي','تقييماته متوازنة، و18% منها «ممتاز»','g','سليم'],['مدير التوزيع','92% من تقييماته «ممتاز»، وما يطابق الأدلة','r','يحتاج مراجعة'],['مديرة خدمة العملاء','رفضت موظفة واحدة 3 مرات','y','تحت المتابعة']]""",
  """<h3 style="font-size:20px">رصد التحيز في التقييم</h3>${[['تقييم 360 · المستودع المركزي','التقييمات متوازنة ومتّسقة مع الأدلة','g','سليم'],['تقييم 360 · التوزيع','92% من التقييمات «ممتاز»، وما تطابق الأدلة','r','يحتاج مراجعة'],['مقابلات الترقية · خدمة العملاء','نتيجة المقابلة خالفت الأدلة القوية 3 مرات','y','تحت المتابعة']]""")

# ---------- notifications ----------
R("""if(S.rep.status==='edit')it.push(['طلب تعديل','محمد رجّع تقريرك بملاحظة.']);if(S.rep.status==='ok')it.push(['اعتماد','تقريرك اعتُمد.']);if(S.cert.status==='ok')it.push(['اعتماد','محمد اعتمد شهادتك.']);if(S.cert.status==='back')it.push(['شهادة','محمد رجّع شهادتك بملاحظة.']);""",
  """if(S.rep.status==='ok')it.push(['اعتماد تلقائي','تقريرك اعتُمد «سنع».']);if(S.rep.status==='low')it.push(['نتيجة تلقائية','تقريرك سُجّل «شاطر». حسّنه وحاول مرة ثانية.']);if(S.cert.status==='ok')it.push(['اعتماد تلقائي','اعتُمدت شهادتك.']);if(S.cert.status==='back')it.push(['شهادة','سُجّلت شهادتك معرفة نظرية. أثبت التطبيق بالتحدي.']);""")
R("""S.queue.filter(q=>q.st==='pending').forEach(q=>it.push(['طلب اعتماد',q.type==='cert'?'عبدالله أضاف شهادة خارجية.':'عبدالله سلّم تقرير يحتاج رأيك.']));if(S.rep.status==='ok')it.push(['اعتماد تلقائي','تقرير عبدالله اعتُمد تلقائيًا (دليل كامل).']);""",
  """if(S.rep.status==='ok')it.push(['اعتماد تلقائي','تقرير عبدالله اعتُمد «سنع».']);if(S.cert.status==='ok')it.push(['اعتماد تلقائي','شهادة عبدالله اعتُمدت.']);if(S.majed.status==='open')it.push(['مقابلة ترقية','ملف ماجد جاهز وينتظر مقابلتك.']);""")
R("""if(S.majed.status==='sent')it.push(['ترشيح','محمد رشّح ماجد للترقية.']);""","""if(S.majed.status==='sent')it.push(['ترقية','ملف ماجد اكتمل وانتقل للجنة تلقائيًا.']);""")

# ---------- login role text ----------
R("تابع فريقك وأداءهم وعبء شغلهم، ورشّح الجاهزين.","تابع فريقك وأداءهم وعبء شغلهم، وأجرِ مقابلات الترقية.")

for bad in ['queue','decideBtn','askEdit','rejMajed','resubmit','reqCard','نشرف','يحتاج رأيك','سلّم لمحمد']:
    if bad in s: print('STILL',bad,s.count(bad))
assert '�' not in s
open(P,'w',encoding='utf8').write(s);print('ok')
