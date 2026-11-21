/* =====================================================================
   API LAYER · نقاط الربط مع قاعدة البيانات
   كل تغيير في البيانات يمر من هنا. لربط قاعدة بيانات حقيقية: استبدل جسم
   كل دالة باستدعاء الخدمة المذكورة في التعليق، واترك الواجهة كما هي.
   ===================================================================== */
const API={
 // POST /submissions  {employeeId, skillId:'ai', type:'report', text, verify, fileName, score, criteria[]}
 submitReport(sub){S.attempts++;S.rep.sub=sub;
  if(sub.score===8){S.rep.status='ok';const prev=S.lv.ai;S.lv.ai=3;const fr=3+(prev<3?5:0);S.fr+=fr;S.newUC=true;S.hist.unshift({who:enm(0),what:'تقرير الأداء الأسبوعي',dec:'اعتماد تلقائي «سنع» (8 من 8)',when:'اليوم',ok:1});return {auto:true,fr}}
  S.rep.status='sent';S.queue.push({id:'q'+Date.now(),type:'report',sub,st:'pending'});return {auto:false}},
 // POST /submissions  {employeeId, skillId, type:'certificate', title, issuer, date, fileUrl, answers[], score}
 submitCert(cert){S.cert.status='sent';S.queue.push({id:'c'+Date.now(),type:'cert',cert,st:'pending'})},
 // PATCH /submissions/:id  {decision:'approve'|'return', note}  → يرجّع دالة تراجع
 decide(id,approve,note){const q=S.queue.find(x=>x.id===id);q.st='done';
  if(q.type==='cert')return decideCert(q,approve,note);
  const sb=q.sub;if(approve){const prev=S.lv.ai;S.lv.ai=Math.max(prev,sb.level);const fr=3+(S.lv.ai>=3&&prev<3?5:0);S.fr+=fr;S.rep.status='ok';S.celebrate={lv:S.lv.ai,req:3,skill:SK.ai.n,fr,by:'محمد اعتمدك'};S.hist.unshift({who:enm(0),what:'تقرير الأداء الأسبوعي',dec:`اعتمد «${LV[sb.level-1]}»`,when:'اليوم',ok:1});return ()=>{S.lv.ai=prev;S.fr-=fr;S.rep.status='sent';S.celebrate=null;S.hist.shift();q.st='pending'}}
  S.rep.status='edit';S.rep.note=note;S.hist.unshift({who:enm(0),what:'تقرير الأداء الأسبوعي',dec:'طلب تعديل',when:'اليوم',ok:0});return ()=>{S.rep.status='sent';S.hist.shift();q.st='pending'}},
 // POST /skills/:id/renewals  {employeeId, score}
 renewSkill(sc){S.excel='g';S.fr+=1;S.hist.unshift({who:enm(0),what:'تحدي تجديد Excel',dec:`تجديد تلقائي (${sc} من 3)`,when:'اليوم',ok:1})},
 // PATCH /employees/:id/leave  (يجي تلقائيًا من نظام الإجازات)
 toggleLeave(){S.leave=!S.leave;return S.leave},
 // POST /mentorship/sessions  {menteeId, mentorId, slot}
 bookMentor(){S.mentorBook=true},
 // POST /workshops/:id/registrations
 registerWorkshop(k){S.ws[k]=1},
 // PATCH /content/:id/progress
 toggleContent(k){S.content[k]=!S.content[k]},
 // POST /internal-jobs/:id/applications
 applyInternal(k){S.applied[k]=1},
 // PATCH /promotions/:id  {interview:true}
 recordInterview(){S.majed.interview=true},
 // PATCH /promotions/:id  {status:'nominated'}
 nominate(){S.majed.status='sent';S.hist.unshift({who:'ماجد القحطاني',what:'ملف ترقية · مخطط عمليات',dec:'رشّحه للجنة',when:'اليوم',ok:1});return ()=>{S.majed.status='open';S.hist.shift()}},
 // PATCH /promotions/:id  {status:'rejected', reason}  + POST /appeals (تلقائي لأن الأدلة قوية)
 rejectNomination(reason){S.majed.status='rej';S.appeals.push({who:'ماجد القحطاني',what:'رُفض ترشيحه وأدلته قوية · السبب: '+reason,st:'تحوّل لهيا'});S.hist.unshift({who:'ماجد القحطاني',what:'ملف ترقية · مخطط عمليات',dec:'رفض: '+reason,when:'اليوم',ok:0})},
 // POST /rotations/:id/approve
 approveRotation(k){S.rot[k]=1},
 // POST /shadowing  {skillId, expertId, learnerId, weeks:6}
 startShadow(k){S.shadows[k]={wms:'خالد المطيري',cold:'سلطان العتيبي',cap:'عبدالله الشمري'}[k]},
 // POST /promotions/exceptional/:id/votes  {approverRole}
 castVote(k){S.exc.votes[k]=1;if(Object.values(S.exc.votes).filter(Boolean).length===3){S.exc.status='ok';S.audit.unshift({who:'اللجنة',what:'ترقية استثنائية: سارة الزهراني إلى مديرة توزيع (تجربة 3 شهور)',when:'اليوم'})}},
 // PATCH /positions/:id  {decision}
 decidePosition(k,v){S.positions[k]=v},
 // POST /competency-profiles/:job/change-requests  {weights}
 requestWeights(){S.Wpending=S.Wdraft;S.audit.unshift({who:'هيا',what:'طلبت تعديل أوزان «مخطط عمليات»',when:'اليوم'})},
 // PATCH /competency-profiles/:job/change-requests/:id  {decision}
 resolveWeights(ok){if(ok)S.W=S.Wpending;S.Wpending=null;S.Wdraft=null;S.audit.unshift({who:'لجنة الموارد البشرية',what:ok?'اعتمدت أوزان «مخطط عمليات» الجديدة':'رفضت تعديل الأوزان',when:'اليوم'})},
 // POST /development-plans  {skillId, employeeIds[], netCost, hadafSupport}
 createPlan(b){const P=PROG[b.k],n=b.sel.length;S.plans=S.plans.filter(p=>!(p.k===b.k&&p.st==='rej'));S.plans.push({k:b.k,sel:[...b.sel],net:n*P.cost*(1-P.hadaf),hadaf:n*P.cost*P.hadaf,st:'wait',open:false})},
 // PATCH /development-plans/:id  {status}
 setPlanStatus(i,st){S.plans[i].st=st},
 // PATCH /notifications/:id  {read:true}
 dismiss(key){S.dis.add(key)}
};

const newBuilder=k=>({k,f:{g:'',nat:'',d:'',lv:'',rd:''},sel:missing(k).filter(i=>isSa(EMP[i]))});
function decideCert(q,ok,note){const c=q.cert,res=certResult(c.k,c.score);
 if(ok){S.cert.status='ok';const prev=S.lv[c.k];S.lv[c.k]=res.lv;const met=res.lv>=SK[c.k].req&&prev<SK[c.k].req;const fr=3+(met?5:0);S.fr+=fr;S.celebrate={lv:res.lv,req:SK[c.k].req,skill:SK[c.k].n,fr,by:'محمد اعتمدك'};S.hist.unshift({who:enm(0),what:'شهادة خارجية · '+SK[c.k].n,dec:`اعتمد «${LV[res.lv-1]}»`,when:'اليوم',ok:1});return ()=>{S.cert.status='sent';S.lv[c.k]=prev;S.fr-=fr;S.celebrate=null;S.hist.shift();q.st='pending'}}
 S.cert.status='back';S.cert.note=note||(c.score<=2?'انسجلت كمعرفة نظرية. جرّب التحدي العملي بعد ما تطبّق في المستودع.':'رجّعها محمد للمراجعة.');S.hist.unshift({who:enm(0),what:'شهادة خارجية · '+SK[c.k].n,dec:c.score<=2?'رجّعها: معرفة نظرية':'رجّعها',when:'اليوم',ok:0});return ()=>{S.cert.status='sent';S.hist.shift();q.st='pending'}}

/* ---------- event wiring ---------- */
$('#tbtn').onclick=()=>{if(S.undo){S.undo();S.undo=null;$('#toast').classList.remove('on')}};
$('#bell').onclick=e=>{e.stopPropagation();S.notifOpen=!S.notifOpen;$('#npanel').hidden=!S.notifOpen;$('#bell').setAttribute('aria-expanded',S.notifOpen)};
$('#npanel').addEventListener('click',e=>{e.stopPropagation();const d=e.target.closest('[data-dis]');if(d){API.dismiss(d.dataset.dis);notif()}if(e.target.closest('[data-disall]')){$$('#npanel [data-dis]').forEach(x=>API.dismiss(x.dataset.dis));notif()}});
document.addEventListener('click',e=>{if(S.notifOpen&&!e.target.closest('#npanel')){S.notifOpen=false;$('#npanel').hidden=true;$('#bell').setAttribute('aria-expanded',false)}});
document.addEventListener('input',e=>{const t=e.target;if(t.dataset&&t.dataset.w&&t.tagName==='INPUT'){S.Wdraft={...(S.Wdraft||S.W),[t.dataset.w]:+t.value};const tot=Object.values(S.Wdraft).reduce((a,b)=>a+b,0);t.parentElement.querySelector('.wv').textContent=t.value+'%';const sp=$('#wtot');if(sp){sp.textContent=tot+'%';sp.style.color=tot===100?'var(--ok)':'#A33A16'}const sb=$('[data-act=wSend]');if(sb)sb.disabled=tot!==100}});
document.addEventListener('change',e=>{const t=e.target;
 if(t.dataset&&t.dataset.f){const tgt=t.dataset.scope==='gap'?S.gf:S.builder.f;tgt[t.dataset.f]=t.value;t.dataset.scope==='gap'?render():drawPlan();return}
 if(t.dataset&&t.dataset.w&&t.tagName==='INPUT'){render();return}
 if(!S.builder)return;
 if(t.dataset.act==='selEmp'){const i=+t.dataset.i;S.builder.sel=t.checked?[...S.builder.sel,i]:S.builder.sel.filter(x=>x!==i);drawPlan()}
 if(t.dataset.act==='selDept'){const d=+t.dataset.d;const ids=missing(S.builder.k).filter(i=>EMP[i].d===d&&passF(i,S.builder.f,S.builder.k));S.builder.sel=t.checked?[...new Set([...S.builder.sel,...ids])]:S.builder.sel.filter(x=>!ids.includes(x));drawPlan()}});

const ACT={
 openCase(){if(S.attempts>=2)return toast('خلّصت محاولاتك هالشهر');S.step=0;S.t0=Date.now();curText='';curFile='';drawer(true)},
 resubmit(){S.step=2;curText=S.rep.sub?.text||'';drawer(true)},
 nextStep(){S.step++;drawStep()},prev(){S.step--;drawStep()},
 sample(){$('#rtext').value=SAMPLE;curText=SAMPLE;$('#chk').value=SAMPLEV;curFile='';$('#repn').textContent='';runCheck()},
 check(){runCheck()},
 submit(){if(!lastA||!lastA.ok)return;const r=API.submitReport({text:$('#rtext').value,verify:$('#chk').value,file:curFile,r:lastA.r,score:lastA.score,level:lastA.level});drawer(false);render();
  if(r.auto)celebrate({lv:3,req:3,skill:SK.ai.n,fr:r.fr,by:'انعتمدت تلقائيًا'});else toast('سلّمت التحدي لمحمد. السعف ينضاف بعد اعتماده.')},
 openCert(){S.cert={status:S.cert.status,k:S.cert.k||'inv',step:0,title:S.cert.title,issuer:S.cert.issuer,date:S.cert.date,file:S.cert.file};drawer(true,'cert')},
 certNext(){let ok=true;[['ct','اكتب اسم الشهادة'],['ci','اكتب الجهة المانحة'],['cd','اكتب التاريخ']].forEach(([id,m])=>{const el=$('#'+id);const bad=el.value.trim().length<2;el.parentElement.classList.toggle('bad',bad);el.parentElement.querySelector('.err').textContent=bad?m:'';if(bad)ok=false});if(!S.cert.file){$('#cfe').textContent='أرفق ملف الشهادة';ok=false}if(!ok)return;Object.assign(S.cert,{k:$('#ck').value,title:$('#ct').value.trim(),issuer:$('#ci').value.trim(),date:$('#cd').value.trim(),step:1});drawCert()},
 certBack(){S.cert.step=0;drawCert()},
 certSend(){const qs=CQ[S.cert.k];const ans=qs.map((q,i)=>+(document.querySelector(`input[name=c${i}]:checked`)?.value??-1));if(ans.includes(-1)){$('#cres').innerHTML='<div class="banner y" style="margin-top:10px">جاوب على المواقف الأربعة.</div>';return}const score=ans.filter((v,i)=>v===qs[i][2]).length;API.submitCert({k:S.cert.k,title:S.cert.title,issuer:S.cert.issuer,date:S.cert.date,file:S.cert.file,ans,score});drawer(false);render();toast(`جاوبت ${score} من 4. وصلت شهادتك لمحمد مع نتيجة التحدي.`)},
 toggle(b){S.openSk[b.dataset.id]=!S.openSk[b.dataset.id];const w=b.parentElement;w.classList.toggle('open');b.setAttribute('aria-expanded',w.classList.contains('open'))},
 renew(){quiz()},
 quizGo(){const ans=QZ.map((q,i)=>+(document.querySelector(`input[name=q${i}]:checked`)?.value??-1));if(ans.includes(-1)){$('#qres').innerHTML='<p class="qmsg">جاوب على الأسئلة الثلاثة.</p>';return}const sc=ans.filter((v,i)=>v===QZ[i][2]).length;
  if(sc>=2){API.renewSkill(sc);$('#modal').classList.remove('on');render();toast(`جاوبت ${sc} من 3 صح. رجعت Excel خضراء (+1 سعفة)`)}else $('#qres').innerHTML=`<p class="qmsg bad">جاوبت ${sc} من 3 صح. راجع وجرّب مرة ثانية.</p>`},
 leave(){const on=API.toggleLeave();render();toast(on?'تجمّدت نخلتك وعمر مهاراتك لين ترجع':'رجعت من الإجازة، ورجع العداد يمشي')},
 mentor(){API.bookMentor();render();toast('حجزت جلسة مع ماجد الأحد 2 م')},
 ws(b){API.registerWorkshop(b.dataset.k);render();toast('سجّلت في الورشة')},
 content(b){API.toggleContent(b.dataset.k);render()},
 apply(b){API.applyInternal(b.dataset.k);render();toast('قدّمت، ووصل طلبك لهيا')},
 approve(b){decideBtn(b,true)},askEdit(b){decideBtn(b,false)},
 interview(){API.recordInterview();render();toast('سجّلت: ماجد شرح تحديه بنفسه')},
 nominate(){const u=API.nominate();render();toast('رشّحت ماجد، ووصل ملفه للجنة',()=>{u();render()})},
 rejMajed(){const r=($('#mjr')?.value||'').trim();if(r.length<10){toast('اكتب سبب مهني واضح قبل الرفض');$('#mjr')?.focus();return}API.rejectNomination(r);render();toast('رفضت، وتحوّل الملف لهيا للمراجعة لأن الأدلة قوية')},
 rot(b){API.approveRotation(b.dataset.k);render();toast('اعتمدت التدوير، ووصل إشعار للموظفين')},
 shadow(b){API.startShadow(b.dataset.k);render();toast('بدأ الظل 6 أسابيع')},
 palmInfo(b){palmSummary(+b.dataset.i)},
 goEmp(){S.role='emp';S.tab.emp='path';render();scrollTo({top:0})},
 gap(b){const k=b.dataset.k;S.openGap[k]=!S.openGap[k];const w=b.parentElement;w.classList.toggle('open');b.setAttribute('aria-expanded',w.classList.contains('open'))},
 box(b){S.box=S.box===b.dataset.k?null:b.dataset.k;render()},
 boxAct(b){toast(b.dataset.msg)},
 vote(b){API.castVote(b.dataset.k);render()},
 pos(b){API.decidePosition(b.dataset.k,b.dataset.v);render();toast('انطبق القرار: '+b.dataset.v)},
 wSend(){API.requestWeights();render();toast('أرسلتِ التعديل للجنة')},
 wApprove(){API.resolveWeights(true);render();toast('اعتمدت اللجنة الأوزان، وتحدّثت الجاهزية للكل')},
 wReject(){API.resolveWeights(false);render()},
 newPlan(){const k=['cap','ai','inv','xl'].find(k=>!planOf(k));if(!k)return toast('كل المهارات الناقصة لها خطط');S.builder=newBuilder(k);drawer(true,'plan')},
 bk(b){S.builder=newBuilder(b.dataset.k);drawPlan()},
 autoSa(){const P=PROG[S.builder.k],net=P.cost*(1-P.hadaf);let rem=BUDGET.total-usedBudget();const order=missing(S.builder.k).filter(i=>passF(i,S.builder.f,S.builder.k)).sort(prio);const sel=[];for(const i of order){if(rem-net<0)break;sel.push(i);rem-=net}S.builder.sel=sel;drawPlan();toast(`اخترنا ${sel.length} موظف، السعوديين أول`)},
 sendPlan(){API.createPlan(S.builder);S.builder=null;drawer(false);render();toast('أرسلتِ الخطة للاعتماد')},
 planOk(b){API.setPlanStatus(+b.dataset.i,'ok');render();toast('اعتمدت الإدارة الخطة، ووصل الموظفين إشعار')},
 planRej(b){API.setPlanStatus(+b.dataset.i,'rej');render();toast('رفضت الإدارة الخطة، تقدرين تعدّلينها')},
 editPlan(b){const p=S.plans[+b.dataset.i];S.builder={k:p.k,f:{g:'',nat:'',d:'',lv:'',rd:''},sel:[...p.sel]};drawer(true,'plan')},
 track(b){const p=S.plans[+b.dataset.i];p.open=!p.open;render()},
 copyPlan(b){const p=S.plans[+b.dataset.i];const txt=nm(`خطة تطوير: ${PROG[p.k].n}\n${PROG[p.k].p}\nعدد الموظفين: ${p.sel.length}\nصافي التكلفة: ${sar(p.net)}\n`+[...p.sel].sort(prio).map(i=>`- ${enm(i)} (${DEPTS[EMP[i].d]}): ${progOf(i)}%`).join('\n'));navigator.clipboard?.writeText(txt).then(()=>toast('نسختِ ملخص الخطة'),()=>toast('ما قدرنا ننسخ في هالمتصفح'))},
 closeD(){S.builder=null;drawer(false)},
 closeModal(){$('#modal').classList.remove('on')},
 logout(){S.logged=false}
};
function decideBtn(b,approve){const id=b.dataset.q;const note=($('#mn-'+id)?.value||'').trim();const und=API.decide(id,approve,note);render();toast(approve?'اعتمدت، وانضاف للسجل':'رجّعته لعبدالله مع ملاحظتك',()=>{und();render()})}
document.addEventListener('click',e=>{
 const tb=e.target.closest('[data-tab]');if(tb){S.tab[S.role]=tb.dataset.tab;render();return}
 const r=e.target.closest('[data-role]');if(r){S.role=r.dataset.role;render();scrollTo({top:0});return}
 if(e.target.id==='conf'||e.target.closest('.celeb')&&!e.target.closest('button')){confetti();return}
 const b=e.target.closest('[data-act]');if(!b||b.tagName==='INPUT')return;
 const fn=ACT[b.dataset.act];if(fn)fn(b);else console.warn('no handler:',b.dataset.act);
});
$('#dClose').onclick=()=>ACT.closeD();$('#scrim').onclick=()=>ACT.closeD();
document.addEventListener('keydown',e=>{if(e.key==='Escape'){if($('#drawer').classList.contains('on'))ACT.closeD();$('#modal').classList.remove('on')}});

