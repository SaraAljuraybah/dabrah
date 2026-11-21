// v4 filming: full pages (header hidden) + header strips + real UI motion sequences (drawers, modals, celebrations)
// captured frame-by-frame with a paused fake clock, so the site's own animations play in the video.
const {chromium}=require('playwright');const fs=require('fs');
const OUT='/home/claude/proto/vid/s4/';fs.mkdirSync(OUT,{recursive:true});
(async()=>{
const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:720},deviceScaleFactor:3});const p=await ctx.newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.clock.install();
const W=t=>p.waitForTimeout(t);const meta={pages:{},seqs:{},shots:{},boxes:{}};const ev=(f,a)=>p.evaluate(f,a);
const save=()=>fs.writeFileSync(OUT+'meta.json',JSON.stringify(meta,null,1));
const clickEl=`e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))`;
const clk=async(sel,t=700)=>{await ev(s=>{const e=document.querySelector(s);if(!e)throw new Error('no '+s);e.dispatchEvent(new MouseEvent('click',{bubbles:true}))},sel);await W(t)};
await p.addInitScript(()=>{document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='.toast,#toast{display:none!important}*{scroll-behavior:auto!important}';document.head.appendChild(s)})});
const rect=async(q)=>ev(q=>{let el=null;if(typeof q==='string')el=document.querySelector(q);else{const c=[...document.querySelectorAll(q.sel||'*')].filter(e=>e.textContent.includes(q.text)&&e.getClientRects().length);c.sort((a,b)=>a.textContent.length-b.textContent.length);el=c[q.i||0]}
  if(!el)return null;const r=el.getBoundingClientRect();return [r.left+scrollX,r.top+scrollY,r.width,r.height].map(Math.round)},q);
const revealAll=()=>ev(()=>document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in')));
const bar=async()=>ev(()=>{let e=document.elementFromPoint(640,8);while(e&&e!==document.body){const ps=getComputedStyle(e).position;if(ps==='sticky'||ps==='fixed')break;e=e.parentElement}const r=e.getBoundingClientRect();return {sel:e.id?('#'+e.id):e.className,h:Math.round(r.bottom)}});
let BAR=null;
// full page, header hidden, plus viewport header strip
const page_=async(name,boxes=[])=>{
  await revealAll();await ev(()=>window.scrollTo(0,0));await W(1300);
  if(!BAR){BAR=await bar();meta.bar=BAR;console.log('bar',BAR)}
  await p.screenshot({path:OUT+'hdr_'+name+'.jpg',type:'jpeg',quality:92});           // viewport (for header strip + scroll-0 view)
  await ev(h=>{const e=document.elementFromPoint(640,8);let x=e;while(x&&x!==document.body){const ps=getComputedStyle(x).position;if(ps==='sticky'||ps==='fixed')break;x=x.parentElement}x.style.visibility='hidden';x.dataset.vh=1},0);
  const bx={};for(const [n,q] of boxes)bx[n]=await rect(q);
  const H=await ev(()=>document.documentElement.scrollHeight);
  await p.screenshot({path:OUT+'pg_'+name+'.jpg',type:'jpeg',quality:92,fullPage:true});
  await ev(()=>document.querySelectorAll('[data-vh]').forEach(e=>{e.style.visibility='';delete e.dataset.vh}));
  meta.pages[name]={h:H,boxes:bx};console.log('page',name,H,JSON.stringify(bx));save();
};
const vshot=async(name,boxes=[],wait=900)=>{await W(wait);const bx={};for(const [n,q] of boxes)bx[n]=await rect(q);
  await p.screenshot({path:OUT+'v_'+name+'.jpg',type:'jpeg',quality:92});meta.shots[name]={boxes:bx};console.log('shot',name,JSON.stringify(bx));save()};
// motion sequence: pause fake clock, run action, then step 1/30 s per frame driving JS timers and CSS animations
const seq=async(name,action,frames)=>{
  await ev(()=>window.scrollTo(0,0));
  const now=await ev(()=>Date.now());await p.clock.pauseAt(now+20);
  await ev(()=>{window.__pre=new Set(document.getAnimations())});
  await ev(action);
  for(let i=0;i<frames;i++){
    await ev(i=>{for(const a of document.getAnimations()){if(window.__pre.has(a))continue;a.pause();a.currentTime=i*1000/30}},i);
    await p.screenshot({path:OUT+`q_${name}_${String(i).padStart(3,'0')}.jpg`,type:'jpeg',quality:90});
    await p.clock.runFor(1000/30);
  }
  await ev(()=>{for(const a of document.getAnimations())if(!window.__pre.has(a)){try{a.finish()}catch(e){}}});
  await p.clock.resume();await W(500);meta.seqs[name]=frames;console.log('seq',name,frames);save();
};
await p.goto('file:///home/claude/proto/dabrah.html#login');await W(900);
await clk('[data-pick=emp]',300);await clk('[data-lfill]',300);await clk('button[type=submit]',1800);
// ---------- employee ----------
await page_('E_path',[['hello','.hello'],['challenge',{text:'ابدأ التحدي',sel:'button'}],['cert',{text:'أضف شهادة',sel:'button'}],['palm',{text:'نخلتك',sel:'.card'}]]);
await seq('caseOpen',()=>document.querySelector('[data-act=openCase]').dispatchEvent(new MouseEvent('click',{bubbles:true})),16);
await vshot('case0',[['next','[data-act=nextStep]'],['drawer','#drawer']]);
await clk('[data-act=nextStep]',600);await vshot('case1',[['next','[data-act=nextStep]']]);
await clk('[data-act=nextStep]',600);await vshot('case2',[['sample','[data-act=sample]']]);
await clk('[data-act=sample]',900);await vshot('caseS',[['submit','[data-act=submit]']]);
await seq('celebA',()=>document.querySelector('[data-act=submit]').dispatchEvent(new MouseEvent('click',{bubbles:true})),96);
await vshot('celebA',[['ok','.celeb button'],['card','.celeb']]);
await seq('celebAclose',()=>document.querySelector('.celeb button, [data-act=closeModal]').dispatchEvent(new MouseEvent('click',{bubbles:true})),10);
await page_('E_path1',[['cert',{text:'أضف شهادة',sel:'button'}],['certcard',{text:'المسار 2',sel:'.card, div'}]]);
await seq('certOpen',()=>document.querySelector('[data-act=openCert]').dispatchEvent(new MouseEvent('click',{bubbles:true})),16);
await vshot('certE',[['demo','[data-act=certDemo]'],['next','[data-act=certNext]']]);
await clk('[data-act=certDemo]',500);await ev(()=>{DABRAH.S.cert.file='shahada.pdf'});await vshot('cert0',[['next','[data-act=certNext]']],400);
await clk('[data-act=certNext]',600);
for(let i=0;i<4;i++)await ev(([i,v])=>{const r=document.querySelector(`input[name=c${i}][value="${v}"]`);r&&(r.checked=true)},[i,[1,1,0,1][i]]);
await vshot('cert1',[['send','[data-act=certSend]']],400);
await seq('celebB',()=>document.querySelector('[data-act=certSend]').dispatchEvent(new MouseEvent('click',{bubbles:true})),75);
await vshot('celebB',[['ok','.celeb button']]);
await seq('celebBclose',()=>document.querySelector('.celeb button, [data-act=closeModal]').dispatchEvent(new MouseEvent('click',{bubbles:true})),10);
await ev(()=>{document.querySelectorAll('[data-act=closeD]').forEach(b=>b.offsetParent&&b.click())});await W(400);
await page_('E_path2',[['palm',{text:'نخلتك',sel:'.card'}],['comp',{text:'جداراتي وطريقي',sel:'h2,h3'}],['compcard',{text:'جداراتي وطريقي',sel:'.card'}]]);
const fr0=await ev(()=>DABRAH.S.fr);
for(const f of [2,8,17]){await ev(v=>{DABRAH.S.fr=v;document.querySelector('[data-tab=path]').dispatchEvent(new MouseEvent('click',{bubbles:true}))},f);await revealAll();await vshot('palm'+f,[],1500)}
await ev(v=>{DABRAH.S.fr=v;document.querySelector('[data-tab=path]').dispatchEvent(new MouseEvent('click',{bubbles:true}))},fr0);await W(800);
await clk('[data-tab=perf]',900);await page_('E_perf',[['r360',{text:'تقييم 360',sel:'.card'}]]);
await clk('[data-tab=learn]',900);await page_('E_learn',[['mentor',{text:'مرشدك',sel:'.card'}],['content',{text:'محتوى من شركتك',sel:'.card'}],['ws',{text:'الورش والدورات',sel:'.card'}]]);
await clk('[data-tab=jobs]',900);await page_('E_jobs',[['list',{text:'منسق تخطيط عمليات',sel:'.card'}]]);
// ---------- haya ----------
await clk('[data-role=haya]',1300);await ev(()=>document.getElementById('modal').classList.remove('on'));
await page_('H_talent',[['ready',{text:'جاهزون للترقية',sel:'.kpi, .card, div'}]]);
await seq('readyOpen',()=>{const e=[...document.querySelectorAll('[data-act=drill]')].find(x=>x.dataset.k==='ready'||x.textContent.includes('جاهزون'));e.dispatchEvent(new MouseEvent('click',{bubbles:true}))},14);
await vshot('hready',[['ok','[data-act=closeModal]'],['box','#mbox']]);
await seq('readyClose',()=>document.querySelector('[data-act=closeModal]').dispatchEvent(new MouseEvent('click',{bubbles:true})),10);
await clk('[data-tab=needs]',900);
await page_('H_needs',[['jobs',{text:'إدارة الوظائف',sel:'.card'}],['r0',{text:'التوصية',sel:'*',i:0}]]);
meta.pages.H_needs.recs=await ev(()=>{const card=[...document.querySelectorAll('.card')].find(c=>c.textContent.includes('إدارة الوظائف'));const btns=[...card.querySelectorAll('button')].filter(b=>b.textContent.includes('طبّقي'));
  return btns.map(b=>{let row=b;while(row.parentElement&&row.parentElement!==card&&!(row.parentElement.children.length>2&&[...row.parentElement.children].filter(c=>c.querySelector&&c.querySelector('button')).length>1))row=row.parentElement;const r=row.getBoundingClientRect(),q=b.getBoundingClientRect();return {row:[r.left+scrollX,r.top+scrollY,r.width,r.height].map(Math.round),btn:[q.left+scrollX,q.top+scrollY,q.width,q.height].map(Math.round)}})});
console.log('recs',JSON.stringify(meta.pages.H_needs.recs));save();
await clk('[data-tab=dev]',900);await page_('H_dev',[['new','[data-act=newPlan]']]);
const ny=meta.pages.H_dev.boxes.new[1];const sDev=Math.max(0,Math.round(ny-420));meta.sDev=sDev;
await seq('planOpen',async()=>{document.querySelector('[data-act=newPlan]').dispatchEvent(new MouseEvent('click',{bubbles:true}))},16);
await vshot('hplan0',[['auto','[data-act=autoSa]'],['sa',{text:'الأولوية القصوى للسعوديين',sel:'div'}],['drawer','#drawer']]);
await clk('[data-act=autoSa]',700);await vshot('hplan1',[['send','[data-act=sendPlan]']]);
await seq('planSend',()=>document.querySelector('[data-act=sendPlan]').dispatchEvent(new MouseEvent('click',{bubbles:true})),12);
await clk('[data-tab=gov]',900);await page_('H_gov',[['w',{text:'ملف جدارات',sel:'.card'}],['bias',{text:'رصد التحيز',sel:'.card'}]]);
// ---------- manager ----------
await clk('[data-role=mgr]',1300);await ev(()=>document.getElementById('modal').classList.remove('on'));
await page_('M_team',[['garden','.garden'],['palm0','#garden [data-i="0"]']]);
await seq('palOpen',()=>document.querySelector('#garden [data-i="0"]').dispatchEvent(new MouseEvent('click',{bubbles:true})),22);
await vshot('mpal',[['box','#mbox'],['all',{text:'كل الجدارات',sel:'summary'}]]);
await ev(()=>{const d=document.querySelector('#modal details');d.open=true});await W(700);
await vshot('mpalX',[['box','#mbox']]);
meta.mboxX=await ev(()=>{const r=document.getElementById('mbox').getBoundingClientRect();return [r.left,r.top,r.width,r.height]});
await ev(()=>{const m=document.getElementById('mbox');m.dataset.mh=m.style.maxHeight;m.style.maxHeight='none';m.style.overflow='visible'});await W(300);
const mb=p.locator('#mbox');await mb.screenshot({path:OUT+'mbox_tall.jpg',type:'jpeg',quality:92});
meta.mboxTallH=await ev(()=>document.getElementById('mbox').getBoundingClientRect().height);
await ev(()=>{const m=document.getElementById('mbox');m.style.maxHeight=m.dataset.mh;m.style.overflow=''});save();
await clk('[data-act=closeModal]',500);
// ---------- top ----------
await clk('[data-role=top]',1300);await ev(()=>document.getElementById('modal').classList.remove('on'));
await page_('T_files');await clk('[data-tab=champs]',900);await page_('T_champs');await clk('[data-tab=overview]',900);await page_('T_over');
console.log('errors',errs);await b.close()})();
