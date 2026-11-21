// Fixed-camera filming: every state is the 1280x720 viewport (sticky header intact) at a given scroll, 3x.
const {chromium}=require('playwright');const fs=require('fs');
const OUT='/home/claude/proto/vid/s3/';fs.mkdirSync(OUT,{recursive:true});
(async()=>{
const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:720},deviceScaleFactor:3});const p=await ctx.newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));
const W=t=>p.waitForTimeout(t);const meta={};const ev=(f,a)=>p.evaluate(f,a);
const fire=`(e)=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))`;
const clk=async(sel,t=700)=>{await ev(s=>{const e=document.querySelector(s);if(!e)throw new Error('no '+s);e.dispatchEvent(new MouseEvent('click',{bubbles:true}))},sel);await W(t)};
await p.addInitScript(()=>{document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='.toast,#toast{display:none!important}*{scroll-behavior:auto!important}';document.head.appendChild(s)})});
// scroll: number, or {text, sel, off} -> scroll so the element top sits at `off` px from viewport top
const snap=async(name,scroll=0,boxes=[],wait=1300)=>{
  await ev(()=>document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in')));
  await ev(sc=>{let y=0;if(typeof sc==='number')y=sc;else{const c=[...document.querySelectorAll(sc.sel||'*')].filter(e=>e.textContent.includes(sc.text)&&e.getClientRects().length);c.sort((a,b)=>a.textContent.length-b.textContent.length);const r=c[0].getBoundingClientRect();y=r.top+scrollY-(sc.off??90)}window.scrollTo(0,y)},scroll);
  await W(wait);
  const std=[['role:emp','[data-role=emp]'],['role:mgr','[data-role=mgr]'],['role:haya','[data-role=haya]'],['role:top','[data-role=top]']];
  const tabs=await ev(()=>[...document.querySelectorAll('[data-tab]')].map(e=>['tab:'+e.dataset.tab,`[data-tab="${e.dataset.tab}"]`]));
  const bx=await ev(list=>{const o={};for(const [n,q] of list){let el=null;
     if(typeof q==='string')el=document.querySelector(q);else{const c=[...document.querySelectorAll(q.sel||'*')].filter(e=>e.textContent.includes(q.text)&&e.getClientRects().length);c.sort((a,b)=>a.textContent.length-b.textContent.length);el=c[0]}
     if(el){const r=el.getBoundingClientRect();if(r.width)o[n]=[r.left,r.top,r.width,r.height].map(Math.round)}}return o},[...std,...tabs,...boxes]);
  await p.screenshot({path:OUT+name+'.jpg',type:'jpeg',quality:92});
  meta[name]={boxes:bx,scrollY:await ev(()=>scrollY)};console.log(name,JSON.stringify(Object.fromEntries(Object.entries(bx).filter(([k])=>!k.startsWith('role')&&!k.startsWith('tab')))));
  fs.writeFileSync(OUT+'meta.json',JSON.stringify(meta,null,1));
};
await p.goto('file:///home/claude/proto/dabrah.html#login');await W(800);
await clk('[data-pick=emp]',300);await clk('[data-lfill]',300);await clk('button[type=submit]',1800);
// ---- employee: palm growth on مساري ----
const fr0=await ev(()=>DABRAH.S.fr);
for(const f of [2,8,17,26]){await ev(v=>{DABRAH.S.fr=v;document.querySelector('[data-tab=path]').dispatchEvent(new MouseEvent('click',{bubbles:true}))},f);
  await snap('palm'+f,0,[['palmcard',{text:'نخلتك',sel:'.card'}],['challenge',{text:'ابدأ التحدي',sel:'button'}],['cert',{text:'أضف شهادة',sel:'button'}],['hello','.hello']],1500)}
await ev(v=>{DABRAH.S.fr=v;document.querySelector('[data-tab=path]').dispatchEvent(new MouseEvent('click',{bubbles:true}))},fr0);
await snap('path0',0,[['palmcard',{text:'نخلتك',sel:'.card'}],['challenge',{text:'ابدأ التحدي',sel:'button'}],['cert',{text:'أضف شهادة',sel:'button'}],['p1',{text:'المسار 1',sel:'*'}],['hello','.hello']]);
// challenge
await clk('[data-act=openCase]',800);await snap('case0',0,[['next','[data-act=nextStep]'],['drawer','#drawer, .drawer']]);
await clk('[data-act=nextStep]',600);await snap('case1',0,[['next','[data-act=nextStep]']]);
await clk('[data-act=nextStep]',600);await snap('case2',0,[['sample','[data-act=sample]'],['submit','[data-act=submit]']]);
await clk('[data-act=sample]',900);await snap('caseS',0,[['submit','[data-act=submit]']]);
await clk('[data-act=submit]',1600);await snap('celeb',0,[['ok','.celeb button, [data-act=closeModal]'],['card','.celeb']],900);
await clk('[data-act=closeModal]',600);
await snap('path1',0,[['cert',{text:'أضف شهادة',sel:'button'}],['p2',{text:'المسار 2',sel:'*'}]]);
// certificate
await clk('[data-act=openCert]',800);await snap('certE',0,[['demo','[data-act=certDemo]'],['next','[data-act=certNext]']]);
await clk('[data-act=certDemo]',500);await ev(()=>{DABRAH.S.cert.file='shahada.pdf'});await snap('cert0',0,[['next','[data-act=certNext]']],500);
await clk('[data-act=certNext]',600);
for(let i=0;i<4;i++)await ev(([i,v])=>{const r=document.querySelector(`input[name=c${i}][value="${v}"]`);r&&(r.checked=true)},[i,[1,1,0,1][i]]);
await snap('cert1',0,[['send','[data-act=certSend]']],500);
await clk('[data-act=certSend]',1200);await snap('cert2',0,[['ok','[data-act=closeModal]'],['card','.celeb']]);
await ev(()=>{document.querySelectorAll('[data-act=closeModal],[data-act=closeD]').forEach(b=>b.offsetParent&&b.click())});await W(600);
await snap('path2',0,[['hello','.hello']]);
await snap('path306090',{text:'30-60-90',sel:'h2,h3',off:96},[['card',{text:'30-60-90',sel:'.card'}]]);
await snap('pathComp',{text:'جداراتي وطريقي',sel:'h2,h3',off:96},[['card',{text:'جداراتي وطريقي',sel:'.card'}]]);
// performance
await clk('[data-tab=perf]',900);await snap('perf0',0,[['kpis','.g4, .kpis']]);
await snap('perf360',{text:'تقييم 360',sel:'h2,h3',off:300},[['card',{text:'تقييم 360',sel:'.card'}]]);
// learning
await clk('[data-tab=learn]',900);await snap('learn0',0,[['mentor',{text:'مرشدك',sel:'.card'}],['content',{text:'محتوى من شركتك',sel:'.card'}]]);
await snap('learnWs',{text:'الورش والدورات',sel:'h2,h3',off:110},[['ws',{text:'الورش والدورات',sel:'.card'}]]);
// internal jobs
await clk('[data-tab=jobs]',900);await snap('jobs',0,[['list',{text:'منسق تخطيط عمليات',sel:'.card'}],['m1',{text:'تطابق 89',sel:'*'}]]);
// ---- haya ----
await clk('[data-role=haya]',1300);await ev(()=>document.getElementById('modal').classList.remove('on'));
await snap('h0',0,[['ready',{text:'جاهزون للترقية',sel:'.kpi, .card, div'}],['readyBtn','[data-act=drill][data-k=ready]']]);
await ev(()=>{const e=[...document.querySelectorAll('[data-act=drill]')].find(x=>x.dataset.k==='ready'||x.textContent.includes('جاهزون'));e.dispatchEvent(new MouseEvent('click',{bubbles:true}))});await W(900);
await snap('hready',0,[['ok','[data-act=closeModal]']]);await clk('[data-act=closeModal]',400);
await snap('hexc',{text:'ترقية استثنائية',sel:'h2,h3',off:200},[['exc',{text:'ترقية استثنائية',sel:'.card'}],['succ',{text:'التعاقب الوظيفي',sel:'.card'}]]);
await clk('[data-tab=needs]',900);await snap('hneeds',{text:'إدارة الوظائف',sel:'h2,h3',off:110},[['jobs',{text:'إدارة الوظائف',sel:'.card'}]]);
await clk('[data-tab=dev]',900);await snap('hdev',0,[['new','[data-act=newPlan]']]);
await clk('[data-act=newPlan]',800);await snap('hplan0',0,[['auto','[data-act=autoSa]'],['sa',{text:'الأولوية القصوى للسعوديين',sel:'div'}]]);
await clk('[data-act=autoSa]',700);await snap('hplan1',0,[['send','[data-act=sendPlan]']]);
await clk('[data-act=sendPlan]',800);
await clk('[data-tab=gov]',900);await snap('hgov',0,[['w',{text:'ملف جدارات',sel:'.card'}]]);
await snap('hbias',{text:'رصد التحيز',sel:'h2,h3',off:260},[['bias',{text:'رصد التحيز',sel:'.card'}]]);
// ---- manager ----
await clk('[data-role=mgr]',1300);await ev(()=>document.getElementById('modal').classList.remove('on'));
await snap('m0',0,[['garden','.garden'],['palm0','#garden [data-i="0"]']]);
await clk('#garden [data-i="0"]',900);await snap('mpal',0,[['ok','[data-act=closeModal]']]);await clk('[data-act=closeModal]',400);
await clk('[data-tab=perf]',900);await snap('mperf',0);
await clk('[data-tab=know]',900);await snap('mknow',0);
await clk('[data-tab=budget]',900);await snap('mbudget',0);
// ---- top ----
await clk('[data-role=top]',1300);await ev(()=>document.getElementById('modal').classList.remove('on'));
await snap('t0',0,[['vote','[data-act=vote]']]);
await clk('[data-tab=plans]',900);await snap('tplans',0,[['ok','[data-act=planOk]']]);
await clk('[data-tab=champs]',900);await snap('tchamps',0);
await clk('[data-tab=overview]',900);await snap('tover',0);
console.log('errors',errs);await b.close()})();
