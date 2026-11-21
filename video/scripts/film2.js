// Films every state for the 80s cut at 3x. full=true -> full page (sticky bars made static); else viewport.
const {chromium}=require('playwright');const fs=require('fs');
const OUT='/home/claude/proto/vid/s2/';fs.mkdirSync(OUT,{recursive:true});
(async()=>{
const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:720},deviceScaleFactor:3});const p=await ctx.newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));
const W=t=>p.waitForTimeout(t);const meta={};
const ev=(f,a)=>p.evaluate(f,a);
const clk=async(sel,t=700)=>{await ev(s=>{const e=document.querySelector(s);if(!e)throw new Error('no '+s);e.dispatchEvent(new MouseEvent('click',{bubbles:true}))},sel);await W(t)};
const clkText=async(text,sel='button,a',t=700)=>{await ev(([x,s])=>{const c=[...document.querySelectorAll(s)].filter(e=>e.textContent.includes(x)&&e.offsetParent!==null);if(!c.length)throw new Error('no text '+x);c[0].click()},[text,sel]);await W(t)};
await p.addInitScript(()=>{const s=document.createElement('style');s.textContent='.toast,#toast{display:none!important}*{scroll-behavior:auto!important}';document.addEventListener('DOMContentLoaded',()=>document.head.appendChild(s))});
const snap=async(name,boxes=[],{full=true,wait=1500}={})=>{
  await ev(()=>document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in')));await W(wait);
  if(full)await ev(()=>{document.querySelectorAll('body *').forEach(e=>{const cs=getComputedStyle(e);if((cs.position==='sticky'||cs.position==='fixed')&&!e.closest('#modal,.drawer,#drawer,.scrim,#scrim')&&e.id!=='modal'&&!e.classList.contains('drawer')){e.dataset.vpos=1;e.style.position='relative'}});window.scrollTo(0,0)});
  else await ev(()=>window.scrollTo(0,0));
  await W(250);
  const bx=await ev(list=>{const o={};for(const [n,q] of list){let el=null;
     if(typeof q==='string')el=document.querySelector(q);else{const c=[...document.querySelectorAll(q.sel||'*')].filter(e=>e.textContent.includes(q.text)&&e.getClientRects().length);c.sort((a,b)=>a.textContent.length-b.textContent.length);el=c[0]}
     if(el){const r=el.getBoundingClientRect();o[n]=[r.left+scrollX,r.top+scrollY,r.width,r.height].map(Math.round)}else o[n]=null}return o},boxes);
  const H=await ev(()=>document.documentElement.scrollHeight);
  await p.screenshot({path:OUT+name+'.jpg',type:'jpeg',quality:92,fullPage:full});
  if(full)await ev(()=>document.querySelectorAll('[data-vpos]').forEach(e=>{e.style.position='';delete e.dataset.vpos}));
  meta[name]={h:full?H:720,boxes:bx};console.log(name,full?H:720,JSON.stringify(bx));fs.writeFileSync(OUT+'meta.json',JSON.stringify(meta,null,1));
};
await p.goto('file:///home/claude/proto/dabrah.html');await W(900);
// ---------- landing ----------
await ev(()=>{const w=document.getElementById('word');w.style.display='none';w.previousElementSibling.style.display='none';document.getElementById('meaning').style.opacity=1});
await snap('land',[['hero','.hero'],['story','#story'],['name','#name'],['meaning','#meaning'],['try','#try'],['levels','#levels'],['lvUp','#lvUp'],['age','#age'],['palm','#palm']]);
// levels 1..5 (viewport shots of the try section scrolled into view)
await ev(()=>{for(let i=0;i<6;i++)document.getElementById('lvDown').click()});await W(300);
for(let l=1;l<=5;l++){ if(l>1){await ev(()=>document.getElementById('lvUp').click());await W(500)}
  await ev(v=>{const a=document.getElementById('age');a.value=v;a.dispatchEvent(new Event('input',{bubbles:true}))},[2,2,2,2,2][l-1]);
  await snap('lv'+l,[['levels','#levels'],['lvUp','#lvUp'],['lvname','#lvname'],['age','#age']],{wait:700});}
for(const a of [0,5,9,14]){await ev(v=>{const e=document.getElementById('age');e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}))},a);await snap('age'+a,[['age','#age'],['health','.health']],{wait:600})}
// ---------- login ----------
await ev(()=>location.hash='#login');await W(700);
await snap('login0',[['emp','[data-pick=emp]']],{full:false});
await clk('[data-pick=emp]',400);await clk('[data-lfill]',400);
await snap('login1',[['fill','[data-lfill]'],['submit','button[type=submit]']]);
await clk('button[type=submit]',1800);
// ---------- employee: palm growth ----------
const fr0=await ev(()=>DABRAH.S.fr);
for(const f of [2,8,17,26]){await ev(v=>{DABRAH.S.fr=v;document.querySelector('[data-tab=path]').click()},f);await snap('palm'+f,[['palmcard',{text:'نخلتك',sel:'.card'}],['hello','.hello']],{wait:1700})}
await ev(v=>{DABRAH.S.fr=v;document.querySelector('[data-tab=path]').click()},fr0);
await snap('path0',[['hello','.hello'],['challenge',{text:'ابدأ التحدي',sel:'button'}],['cert',{text:'أضف شهادة',sel:'button'}],['r306090',{text:'30-60-90',sel:'h2,h3'}],['houses',{text:'جداراتي وطريقي',sel:'h2,h3'}]]);
// challenge flow
await clk('[data-act=openCase]',800);await snap('case0',[['next','[data-act=nextStep]']],{full:false});
for(let i=0;i<4;i++){const has=await ev(()=>!!document.querySelector('[data-act=sample]')&&document.querySelector('[data-act=sample]').offsetParent!==null);if(has)break;await clk('[data-act=nextStep]',600);await snap('case'+(i+1),[['next','[data-act=nextStep]'],['sample','[data-act=sample]']],{full:false})}
await clk('[data-act=sample]',900);await snap('caseS',[['submit','[data-act=submit]'],['check','[data-act=check]']],{full:false});
await clk('[data-act=submit]',1600);await snap('celeb',[],{full:false,wait:900});
await clk('[data-act=closeModal]',500);
// certificate flow
await clk('[data-act=openCert]',800);await clk('[data-act=certDemo]',500);await ev(()=>{DABRAH.S.cert.file='shahada.pdf';const n=document.getElementById('repn')||document.querySelector('[id^=cf]');});
await snap('cert0',[['next','[data-act=certNext]']],{full:false});
await clk('[data-act=certNext]',600);await snap('cert1',[['send','[data-act=certSend]']],{full:false});
for(let i=0;i<4;i++)await ev(([i,v])=>{const r=document.querySelector(`input[name=c${i}][value="${v}"]`);r&&(r.checked=true)},[i,[1,1,0,1][i]]);await W(200);
await snap('cert1b',[['send','[data-act=certSend]']],{full:false,wait:300});
await clk('[data-act=certSend]',1200);await snap('cert2',[],{full:false});
await ev(()=>{document.querySelectorAll('[data-act=closeModal],[data-act=closeD]').forEach(b=>b.offsetParent&&b.click())});await W(600);
await clk('[data-tab=path]',900);
await snap('path1',[['hello','.hello'],['r306090',{text:'30-60-90',sel:'h2,h3'}],['houses',{text:'جداراتي وطريقي',sel:'h2,h3'}]]);
await clk('[data-tab=perf]',900);await snap('perf',[['kpis','.kpis'],['honor',{text:'لوحة الشرف',sel:'h2,h3'}],['r360',{text:'تقييم 360',sel:'h2,h3'}]]);
await clk('[data-tab=learn]',900);await snap('learn',[['mentor',{text:'مرشدك',sel:'h2,h3'}],['content',{text:'محتوى من شركتك',sel:'h2,h3'}],['ws',{text:'الورش والدورات',sel:'h2,h3'}]]);
await clk('[data-tab=jobs]',900);await snap('jobs',[['h','h2']]);
// ---------- manager ----------
await clk('[data-role=mgr]',1300);await ev(()=>document.getElementById('modal').classList.remove('on'));
await snap('mteam',[['garden','.garden'],['champs','.champs']]);
await clk('#garden [data-i="0"]',900);await snap('mpal',[],{full:false});await clk('[data-act=closeModal]',400);
await clk('[data-tab=perf]',900);await snap('mperf0',[['load',{text:'تحليل عبء العمل',sel:'h2,h3'}],['rot',{text:'اقتراحات التدوير',sel:'h2,h3'}],['rotBtn','[data-act=rot]']]);
await ev(()=>document.querySelectorAll('[data-act=rot]').forEach(b=>b.click()));await W(400);
for(let i=0;i<3;i++){await ev(()=>{const b=document.querySelector('[data-act=rot]');b&&b.click()});await W(300)}
await snap('mperf1',[['load',{text:'تحليل عبء العمل',sel:'h2,h3'}],['rot',{text:'اقتراحات التدوير',sel:'h2,h3'}]]);
await clk('[data-tab=know]',900);await snap('mknow');
await clk('[data-tab=budget]',900);await snap('mbudget');
// ---------- haya ----------
await clk('[data-role=haya]',1300);await ev(()=>document.getElementById('modal').classList.remove('on'));
await snap('htalent0',[['box','[data-act=box]']]);
await ev(()=>{const e=[...document.querySelectorAll('[data-act=drill]')].find(x=>x.dataset.k==='ready'||x.textContent.includes('جاهزون'));e.dispatchEvent(new MouseEvent('click',{bubbles:true}))});await W(900);
await snap('hready',[],{full:false});await clk('[data-act=closeModal]',400);
await clk('[data-tab=needs]',900);await snap('hneeds');
await clk('[data-tab=dev]',900);await clk('[data-act=newPlan]',800);await snap('hplan0',[['auto','[data-act=autoSa]']],{full:false});
await clk('[data-act=autoSa]',700);await snap('hplan1',[['send','[data-act=sendPlan]']],{full:false});
await clk('[data-act=sendPlan]',800);
await snap('hdev');
await clk('[data-tab=gov]',900);await snap('hgov');
// ---------- top ----------
await clk('[data-role=top]',1300);await ev(()=>document.getElementById('modal').classList.remove('on'));
await snap('tfiles0',[['vote','[data-act=vote]']]);
await ev(()=>{const b=document.querySelector('[data-act=vote]');b&&b.click()});await W(700);await snap('tfiles1');
await clk('[data-tab=plans]',900);await snap('tplans0',[['ok','[data-act=planOk]']]);
await ev(()=>{const b=document.querySelector('[data-act=planOk]');b&&b.click()});await W(700);await snap('tplans1');
await clk('[data-tab=champs]',900);await snap('tchamps');
await clk('[data-tab=overview]',900);await snap('tover');
console.log('errors',errs);await b.close()})();
