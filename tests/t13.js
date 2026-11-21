const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await (await b.newContext({viewport:{width:1280,height:860}})).newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='warning'||m.type()==='error'){if(!/Failed to load|ERR_/.test(m.text()))errs.push(m.text())}});
const S=async n=>p.screenshot({path:'/home/claude/proto/v9-'+n+'.png'});const F=async n=>p.screenshot({path:'/home/claude/proto/v9-'+n+'.png',fullPage:true});
const go=async(sel,t=500)=>{await p.click(sel);await p.waitForTimeout(t)};const log=(...a)=>console.log(...a);
await p.goto('file:///home/claude/proto/dabrah.html');await p.waitForTimeout(400);
await p.evaluate(()=>location.hash='#login');await p.waitForTimeout(400);await go('[data-pick=emp]',300);await go('[data-lfill]',200);await go('button[type=submit]',1500);
await go('[data-act=openCase]');await go('[data-act=nextStep]',200);await go('[data-act=nextStep]',200);
await p.fill('#rtext','تقرير الأسبوع\n1. الطلبات 4,120 طلب هذا الأسبوع وهي أعلى من قبل\n2. أخطاء التجهيز 2.8% تقريبًا في المستودع\n3. التأخير 37 دقيقة والخميس هو الأعلى\nالتوصية: نضيف مجهزين');await p.fill('#chk','راجعت الأرقام');await go('[data-act=check]',900);
log('weak score',await p.evaluate(()=>document.querySelector('.rescard b')?.textContent), await p.evaluate(()=>document.getElementById('subBtn').textContent));
if(await p.evaluate(()=>!document.getElementById('subBtn').disabled)){await go('[data-act=submit]',800);log('status',await p.evaluate(()=>DABRAH.S.rep.status));await F('emp-low')}else{await go('[data-act=closeD]',400)}
await go('[data-act=openCase]');await go('[data-act=nextStep]',200);await go('[data-act=nextStep]',200);await go('[data-act=sample]',900);await go('[data-act=submit]',1200);log('status2',await p.evaluate(()=>DABRAH.S.rep.status));await go('[data-act=closeModal]',300);
await go('[data-act=openCert]');await go('[data-act=certDemo]',200);await go('[data-act=certNext]',300);for(let i=0;i<4;i++)await p.check(`input[name=c${i}][value="${[1,1,0,1][i]}"]`);await go('[data-act=certSend]',900);await S('cert-auto');log('cert',await p.evaluate(()=>DABRAH.S.cert.status));await go('[data-act=closeModal]',300);
await F('emp-path');
await go('[data-role=mgr]',1300);await p.evaluate(()=>document.querySelectorAll('details.disc').forEach(d=>d.open=true));await F('mgr-team');
await go('[data-act=interview][data-v="1"]',500);log('majed',await p.evaluate(()=>JSON.stringify(DABRAH.S.majed)));await go('#tbtn',300);log('undo',await p.evaluate(()=>JSON.stringify(DABRAH.S.majed)));
await p.evaluate(()=>document.querySelectorAll('details.disc').forEach(d=>d.open=true));await go('[data-act=interview][data-v="0"]',500);log('fail',await p.evaluate(()=>JSON.stringify(DABRAH.S.majed)));
await go('#bell',300);await S('mgr-bell');await go('#bell',200);
await go('[data-role=haya]',900);await go('[data-tab=gov]',900);await F('h-gov');
await p.setViewportSize({width:390,height:844});
const audit=await p.evaluate(async()=>{const out={};const roles={emp:['path','perf','learn','jobs'],mgr:['team','perf','know','budget'],haya:['talent','needs','dev','gov']};const acts=new Set();
 for(const r in roles){document.querySelector(`[data-role=${r}]`).click();document.getElementById('modal').classList.remove('on');for(const t of roles[r]){document.querySelector(`[data-tab=${t}]`).click();await new Promise(z=>setTimeout(z,150));document.querySelectorAll('details.disc').forEach(d=>d.open=true);document.querySelectorAll('[data-act]').forEach(x=>acts.add(x.dataset.act));if(document.documentElement.scrollWidth>innerWidth+1)out[r+'/'+t]='overflow'}}
 out.missing=[...acts].filter(a=>!DABRAH.ACT[a]);return out});
log('audit',JSON.stringify(audit));log('errors',errs);await b.close()})();
