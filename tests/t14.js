const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await (await b.newContext({viewport:{width:1280,height:860}})).newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='warning'||m.type()==='error'){if(!/Failed to load|ERR_/.test(m.text()))errs.push(m.text())}});
const S=async n=>p.screenshot({path:'/home/claude/proto/v11-'+n+'.png'});const F=async n=>{await p.evaluate(()=>document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in')));await p.screenshot({path:'/home/claude/proto/v11-'+n+'.png',fullPage:true})};
const go=async(sel,t=500)=>{await p.click(sel);await p.waitForTimeout(t)};const log=(...a)=>console.log(...a);
await p.goto('file:///home/claude/proto/dabrah.html');await p.waitForTimeout(400);
log('h2g',await p.evaluate(()=>{const {AR}=window;return 1}));
await p.evaluate(()=>location.hash='#login');await p.waitForTimeout(400);await S('login-roles');
await go('[data-pick=emp]',300);await go('[data-lfill]',200);await go('button[type=submit]',1500);
// cert with hijri
await go('[data-act=openCert]');await p.fill('#ct','شهادة إدارة المخزون');await p.fill('#ci','معهد سلاسل الإمداد');await p.check('input[name=cal][value=h]');await p.waitForTimeout(200);
log('hijri opts',await p.evaluate(()=>[document.querySelector('#cdY option:nth-child(2)').textContent,document.querySelector('#cdM option:nth-child(2)').textContent,document.querySelector('#cdD option:nth-child(31)').textContent]));
await p.selectOption('#cdD','30');await p.selectOption('#cdM','2');await p.selectOption('#cdY','1447');S.cert=1;
await go('[data-act=certNext]',300);log('hijri err (30 safar 1447?)',await p.evaluate(()=>document.getElementById('cde').textContent));
await p.selectOption('#cdD','12');await p.selectOption('#cdM','3');await p.selectOption('#cdY','1448');await p.check('input[name=cal][value=g]');await p.waitForTimeout(200);
log('converted to greg',await p.evaluate(()=>[cdD.value,cdM.value,cdY.value,document.querySelector('#cdY option:nth-child(2)').textContent]));
await p.check('input[name=cal][value=h]');await p.waitForTimeout(200);log('back to hijri',await p.evaluate(()=>[cdD.value,cdM.value,cdY.value]));
await p.evaluate(()=>{DABRAH.S.cert.file='x.pdf'});await S('cert-hijri');await go('[data-act=certNext]',300);log('step',await p.evaluate(()=>[DABRAH.S.cert.step,DABRAH.S.cert.date,DABRAH.S.cert.cal]));
for(let i=0;i<4;i++)await p.check(`input[name=c${i}][value="${[1,1,0,1][i]}"]`);await go('[data-act=certSend]',900);await go('[data-act=closeModal]',300);
await F('emp-path');
await go('[data-tab=learn]',700);await go('[data-act=course][data-k=k1]',300);await go('[data-act=mentor]',300);await F('emp-learn');
await go('[data-tab=perf]',800);await F('emp-perf');await go('[data-act=drill][data-k=rankd]',400);await S('drill-rank');await go('[data-act=closeModal]',300);
await go('[data-act=drill][data-k="k:err"]',400);await S('drill-err');await go('[data-act=closeModal]',300);
// manager reject with reason
await go('[data-role=mgr]',1200);await p.evaluate(()=>document.getElementById('modal').classList.remove('on'));await p.evaluate(()=>document.querySelectorAll('details.disc').forEach(d=>d.open=true));
await go('[data-act=interview][data-v="0"]',300);log('no reason ->',await p.evaluate(()=>DABRAH.S.majed.status));
await p.fill('#ivr','ما قدر يشرح خطوات حل تحدي الجرد بنفسه');await go('[data-act=interview][data-v="0"]',500);log('with reason ->',await p.evaluate(()=>DABRAH.S.majed.status));
await F('mgr-team');await go('[data-act=drill][data-k="grp:0"]',400);await S('drill-grp');await go('[data-act=closeModal]',300);
// haya plan
await go('[data-role=haya]',900);await go('[data-tab=dev]',800);await go('[data-act=newPlan]',600);await go('[data-act=sendPlan]',600);await F('haya-dev');
// top
await go('[data-role=top]',900);await F('top-files');await go('[data-act=esc][data-v="0"]',500);log('top overturn ->',await p.evaluate(()=>DABRAH.S.majed.status));
await go('[data-act=vote][data-k=c]',300);
await go('[data-tab=plans]',700);await F('top-plans');if(await p.$('[data-act=planOk]')){await go('[data-act=planOk]',400)}log('plans',await p.evaluate(()=>DABRAH.S.plans.map(x=>x.st)));
await go('[data-tab=champs]',800);await F('top-champs');await go('[data-tab=overview]',800);await F('top-overview');await go('[data-act=drill][data-k="load:1"]',400);await S('drill-load');await go('[data-act=closeModal]',300);
await p.setViewportSize({width:390,height:844});
const audit=await p.evaluate(async()=>{const out={};const roles={emp:['path','perf','learn','jobs'],mgr:['team','perf','know','budget'],haya:['talent','needs','dev','gov'],top:['files','plans','champs','overview']};const acts=new Set();
 for(const r in roles){document.querySelector(`[data-role=${r}]`).click();document.getElementById('modal').classList.remove('on');for(const t of roles[r]){document.querySelector(`[data-tab=${t}]`).click();await new Promise(z=>setTimeout(z,150));document.querySelectorAll('details.disc').forEach(d=>d.open=true);document.querySelectorAll('[data-act]').forEach(x=>acts.add(x.dataset.act));if(document.documentElement.scrollWidth>innerWidth+1)out[r+'/'+t]='overflow '+document.documentElement.scrollWidth;
  const bad=[...document.querySelectorAll('#page *')].filter(e=>{const R=e.getBoundingClientRect();return R.width&&(R.right>innerWidth+1||R.left<-1)&&!e.closest('.scroll')&&!e.closest('.tabs')});if(bad.length)out[r+'/'+t+'-out']=bad.slice(0,3).map(e=>e.className||e.tagName)}}
 out.missing=[...acts].filter(a=>!DABRAH.ACT[a]);return out});
log('audit',JSON.stringify(audit));
await p.evaluate(()=>{document.querySelector('[data-role=top]').click()});await p.waitForTimeout(300);await p.evaluate(()=>{document.querySelector('[data-tab=champs]').click()});await p.waitForTimeout(500);await F('m-champs');
log('errors',errs);await b.close()})();
