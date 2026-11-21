// Films the platform: full-page JPEG shots at 2.5x + element boxes (page CSS px) for camera & cursor.
const {chromium}=require('playwright');const fs=require('fs');
const OUT='/home/claude/proto/vid/shots/';fs.mkdirSync(OUT,{recursive:true});
(async()=>{
const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:720},deviceScaleFactor:2.5});const p=await ctx.newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));
const W=t=>p.waitForTimeout(t);const go=async(s,t=700)=>{await p.click(s);await W(t)};
const meta={};
const prep=async()=>{await p.evaluate(()=>{document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'));
  if(!document.getElementById('vidcss')){const s=document.createElement('style');s.id='vidcss';s.textContent='*{scroll-behavior:auto!important}.toast,#toast{display:none!important}';document.head.appendChild(s)}});await W(1600)};
// boxes: list of [name, selector or {text, sel}]
const shot=async(name,boxes,{full=true,static_=true}={})=>{
  await prep();
  if(static_)await p.evaluate(()=>{document.querySelectorAll('header,nav,.top,.bar,.appbar').forEach(e=>{const cs=getComputedStyle(e);if(cs.position==='sticky'||cs.position==='fixed'){e.dataset.vpos=cs.position;e.style.position='relative'}})});
  await p.evaluate(()=>window.scrollTo(0,0));await W(300);
  const bx=await p.evaluate(list=>{const o={};for(const [n,q] of list){let el=null;
     if(typeof q==='string')el=document.querySelector(q);else{const c=[...document.querySelectorAll(q.sel||'*')].filter(e=>e.textContent.trim().includes(q.text)&&e.offsetParent!==null);c.sort((a,b)=>a.textContent.length-b.textContent.length);el=c[0]}
     if(el){const r=el.getBoundingClientRect();o[n]=[r.left+scrollX,r.top+scrollY,r.width,r.height].map(v=>Math.round(v))}else o[n]=null}return o},boxes);
  const H=await p.evaluate(()=>document.documentElement.scrollHeight);
  await p.screenshot({path:OUT+name+'.jpg',type:'jpeg',quality:92,fullPage:full});
  if(static_)await p.evaluate(()=>document.querySelectorAll('[data-vpos]').forEach(e=>{e.style.position='';delete e.dataset.vpos}));
  meta[name]={h:full?H:720,boxes:bx};console.log(name,H,JSON.stringify(bx));
};
await p.goto('file:///home/claude/proto/dabrah.html');await W(800);
await shot('land',[['hero','.hero'],['h1','h1'],['cta',{text:'جرّب',sel:'a,button'}],['logo','header img, .logo, nav img']]);
await p.evaluate(()=>location.hash='#login');await W(600);
await shot('login0',[['emp','[data-pick=emp]'],['mgr','[data-pick=mgr]'],['fill','[data-lfill]'],['submit','button[type=submit]']],{full:false});
await go('[data-pick=emp]',300);await go('[data-lfill]',300);
await shot('login1',[['emp','[data-pick=emp]'],['fill','[data-lfill]'],['submit','button[type=submit]']],{full:false});
await go('button[type=submit]',1800);
await shot('emp-path',[['ring','.ring'],['hello','.hello'],['palm','.palmbox'],['challenge',{text:'ابدأ التحدي',sel:'button,a'}],['houses',{text:'جداراتي وطريقي',sel:'h2,h3'}],['house1','.house, svg.hs, .lv'],['r306090',{text:'30-60-90',sel:'h2,h3'}],['tabLearn','[data-tab=learn]'],['tabPerf','[data-tab=perf]'],['roleMgr','[data-role=mgr]']]);
await go('[data-tab=learn]',900);
await shot('emp-learn',[['mentor',{text:'مرشدك',sel:'h2,h3'}],['ws',{text:'الورش والدورات',sel:'h2,h3'}],['reg',{text:'سجّل',sel:'button'}],['content',{text:'محتوى من شركتك',sel:'h2,h3'}]]);
await go('[data-tab=perf]',900);
await shot('emp-perf',[['kpis','.kpis'],['honor',{text:'لوحة الشرف',sel:'h2,h3'}],['eom',{text:'موظف الشهر',sel:'*'}],['r360',{text:'تقييم 360',sel:'h2,h3'}]]);
await go('[data-role=mgr]',1400);await p.evaluate(()=>document.getElementById('modal').classList.remove('on'));
await shot('mgr-team',[['hero','.mhero'],['garden','.garden'],['ready',{text:'جاهزية فريقك',sel:'h2,h3'}],['appr',{text:'آخر الاعتمادات',sel:'h2,h3'}],['champs','.champs'],['tabKnow','[data-tab=know]'],['tabPerf','[data-tab=perf]']]);
await go('[data-tab=know]',900);
await shot('mgr-know',[['one',{text:'شخص واحد',sel:'*'}],['h',{text:'المعرفة الحرجة',sel:'h2,h3'}]]);
await go('[data-tab=perf]',900);
await shot('mgr-perf',[['kpis','.kpis'],['rot',{text:'تدوير',sel:'*'}],['load',{text:'العبء',sel:'h2,h3'}]]);
await go('[data-tab=team]',900);await p.evaluate(()=>document.querySelectorAll('details.disc').forEach(d=>d.open=true));await p.fill('#ivr','ما قدر يشرح خطوات حل تحدي الجرد بنفسه');await go('[data-act=interview][data-v="0"]',700);
await go('[data-role=haya]',1200);await p.evaluate(()=>document.getElementById('modal').classList.remove('on'));
await shot('haya-talent',[['h','h2']]);
await go('[data-tab=needs]',900);await shot('haya-needs',[['h','h2']]);
await go('[data-tab=dev]',900);await go('[data-act=newPlan]',700);
await shot('haya-dev',[['gaps',{text:'أكثر المهارات الناقصة',sel:'h2,h3'}],['plans',{text:'خطط التطوير',sel:'h2,h3'}],['send','[data-act=sendPlan]']]);
await p.evaluate(()=>{const c=document.querySelector('[data-act=closeD]');c&&c.click()});await W(500);
await go('[data-role=top]',1200);await p.evaluate(()=>document.getElementById('modal').classList.remove('on'));
await shot('top-files',[['hello',{text:'حياك فيصل',sel:'h1,h2'}],['rej',{text:'ترقيات رفضها المدير',sel:'h2,h3'}],['reason',{text:'سبب المدير',sel:'*'}],['ok','[data-act=esc]'],['esc0','[data-act=esc][data-v="0"]'],['tabChamps','[data-tab=champs]']]);
await go('[data-tab=champs]',1000);
await shot('top-champs',[['champs','.champs'],['crown','.crown'],['skills',{text:'أبطال المهارات',sel:'h2,h3,h4'}],['eom',{text:'هند الشمراني',sel:'*'}]]);
await go('[data-tab=overview]',1000);
await shot('top-overview',[['kpis','.kpis']]);
fs.writeFileSync(OUT+'meta.json',JSON.stringify(meta,null,1));console.log('errors',errs);await b.close()})();
