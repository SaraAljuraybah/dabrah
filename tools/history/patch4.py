s=open('v3.html',encoding='utf8').read()
def rep(a,b,cnt=1):
    global s
    assert a in s,'MISSING: '+a[:70]; s=s.replace(a,b,cnt)
login='''<!-- ================= LOGIN ================= -->
<div id="login" class="view" hidden>
  <div class="top" style="background:transparent;box-shadow:none;position:relative">
    <img src="data:image/png;base64,__LOGO3__" alt="دبره">
    <a class="back" href="#top" style="margin-inline-start:auto">الرجوع للتعريف</a>
  </div>
  <div class="lwrap" id="lbox"></div>
</div>

'''
rep('<!-- ================= APP ================= -->',login+'<!-- ================= APP ================= -->')
rep('''    <a class="back" href="#top">عن دبره</a>
    <div class="roles" role="group" aria-label="بدّل المستخدم">
      <button data-role="emp" aria-pressed="true">عبدالله · موظف</button>
      <button data-role="mgr" aria-pressed="false">محمد · مدير</button>
      <button data-role="haya" aria-pressed="false">هيا · تطوير</button>
    </div>''','''    <a class="back" href="#top">عن دبره</a><a class="back" href="#login" data-act="logout">تسجيل الخروج</a>
    <div class="roles" role="group" aria-label="تبديل سريع بين الأدوار للعرض">
      <button data-role="emp" aria-pressed="true">موظف</button>
      <button data-role="mgr" aria-pressed="false">مدير</button>
      <button data-role="haya" aria-pressed="false">مسؤول تطوير</button>
    </div>''')
# state names
rep("const S={role:'emp',","const S={logged:false,names:{emp:'عبدالله',mgr:'محمد',haya:'هيا'},role:'emp',")
rep("const V={};","const nm=t=>t.replaceAll('عبدالله',S.names.emp).replaceAll('محمد',S.names.mgr).replaceAll('هيا',S.names.haya);\nconst V={};")
rep(" $('#page').innerHTML=V[S.role]();"," $('#page').innerHTML=nm(V[S.role]());")
rep("function modal(h){$('#mbox').innerHTML=h;","function modal(h){$('#mbox').innerHTML=nm(h);")
rep("function toast(m,undo){$('#tmsg').textContent=m;","function toast(m,undo){$('#tmsg').textContent=nm(m);")
rep("const S0=null;","") if "const S0=null;" in s else None
# login logic + router
a=s.index('/* router */');b=s.index("buildSky();")
LOGIN=r"""/* login */
const RI={emp:'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>',mgr:'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12l5 5L20 6"/></svg>',haya:'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"><path d="M4 20V11M10 20V5M16 20v-6M22 20H2"/></svg>'};
const ROLES={
 emp:{t:'موظف',d:'أثبت مهاراتك، واعرف طريقك للترقية.',f:[['name','الاسم الكامل','text','عبدالله الشمري'],['eid','الرقم الوظيفي','text','10482'],['title','المسمى الحالي','text','مشرف مستودع'],['dept','الإدارة','text','العمليات'],['goal','الوظيفة اللي تطمح لها','select',['مخطط عمليات','مدير عمليات','محلل بيانات تشغيلية']]]},
 mgr:{t:'مدير',d:'اعتمد مهارات فريقك، وتابع جاهزيتهم للترقية.',f:[['name','الاسم الكامل','text','محمد العنزي'],['eid','الرقم الوظيفي','text','20117'],['dept','الإدارة','text','العمليات'],['team','عدد أعضاء فريقك','number','12']]},
 haya:{t:'مسؤول تطوير',d:'تابع أثر التدريب، ووجّه الميزانية لمكانها الصح.',f:[['name','الاسم الكامل','text','هيا القحطاني'],['eid','الرقم الوظيفي','text','30561'],['org','المنشأة','text','مستودعات الشرق'],['count','عدد الموظفين','number','52']]}};
function loginStep(role){
 if(!role){$('#lbox').innerHTML=`<div class="eyebrow">تسجيل الدخول · الخطوة 1 من 2</div><h1 style="font-size:clamp(32px,4.5vw,48px)">مين أنت في المنشأة؟</h1><p style="color:#CFC4B2;margin-top:10px">اختر دورك، ونجهّز لك الشاشة اللي تناسبك.</p><div class="lroles">${Object.entries(ROLES).map(([k,r])=>`<button class="lrole" data-pick="${k}"><span class="ri">${RI[k]}</span><b>${r.t}</b><span>${r.d}</span></button>`).join('')}</div>`;return}
 const r=ROLES[role];
 $('#lbox').innerHTML=`<div class="eyebrow">تسجيل الدخول · الخطوة 2 من 2</div><h1 style="font-size:clamp(30px,4vw,44px)">بياناتك الأساسية · ${r.t}</h1><p style="color:#CFC4B2;margin-top:10px">عبّينا الحقول ببيانات تجريبية، وتقدر تعدّلها.</p>
 <form class="lform" id="lform" novalidate data-role="${role}"><div class="fgrid">${r.f.map(([id,l,t,v])=>`<div class="fld" id="f-${id}"><label for="i-${id}">${l}</label>${t==='select'?`<select id="i-${id}">${v.map(o=>`<option>${o}</option>`).join('')}</select>`:`<input id="i-${id}" type="${t==='number'?'text':'text'}" ${t==='number'||id==='eid'?'inputmode="numeric"':''} value="${v}" autocomplete="off">`}<span class="err" aria-live="polite"></span></div>`).join('')}</div>
 <div class="row between" style="margin-top:18px"><button type="button" class="btn ghost" data-pick="" style="color:var(--ink)">غيّر الدور</button><button type="submit" class="btn">دخول</button></div></form>`;
 setTimeout(()=>$('#i-name')?.focus(),200)}
document.addEventListener('click',e=>{const p=e.target.closest('[data-pick]');if(p)loginStep(p.dataset.pick||null)});
document.addEventListener('submit',e=>{const f=e.target;if(f.id!=='lform')return;e.preventDefault();const role=f.dataset.role;let okk=true;
 const chk=(id,cond,msg)=>{const w=$('#f-'+id);if(!w)return;const bad=!cond(($('#i-'+id).value||'').trim());w.classList.toggle('bad',bad);w.querySelector('.err').textContent=bad?msg:'';if(bad&&okk){okk=false;$('#i-'+id).focus()}};
 chk('name',v=>v.split(/\s+/).length>=2&&v.length>=5,'اكتب اسمك الأول واسم العائلة');
 chk('eid',v=>/^[0-9٠-٩]{4,8}$/.test(v),'الرقم الوظيفي من 4 إلى 8 أرقام');
 ['team','count'].forEach(id=>chk(id,v=>/^[0-9٠-٩]+$/.test(v)&&+v>0,'اكتب رقم صحيح أكبر من صفر'));
 ['title','dept','org'].forEach(id=>chk(id,v=>v.length>=2,'هذا الحقل مطلوب'));
 if(!okk)return;
 S.names[role]=$('#i-name').value.trim().split(/\s+/)[0];S.role=role;S.logged=true;location.hash='#app';setTimeout(()=>toast(`هلا ${S.names[role]}، سجّلت دخولك`),400)});

/* scroll spy */
const SECS=['top','story','name','how','try','palm','faq','impact','final'];
function spy(){if($('#landing').hidden)return;let cur='top';for(const id of SECS){const el=document.getElementById(id);if(el&&el.getBoundingClientRect().top<innerHeight*.45)cur=id}
 $$('#rail a').forEach(a=>a.classList.toggle('on',a.dataset.s===cur));const h=document.documentElement;$('#railbar').style.height=Math.min(100,scrollY/(h.scrollHeight-innerHeight)*100)+'%'}
addEventListener('scroll',spy,{passive:true});

/* router */
function route(){const h=location.hash;const v=h==='#app'?(S.logged?'app':'login'):h==='#login'?'login':'landing';
 $('#app').hidden=v!=='app';$('#login').hidden=v!=='login';$('#landing').hidden=v!=='landing';
 if(v==='app'){render();scrollTo({top:0})}
 if(v==='login'){if(h==='#app')history.replaceState(null,'','#login');loginStep(null);scrollTo({top:0})}
 if(v==='landing'){if(h==='#top'||!h)scrollTo({top:0});spy()}}
addEventListener('hashchange',route);

"""
s=s[:a]+LOGIN+s[b:]
# role tab labels w/ names
rep(" $$('.roles button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.role===S.role));"," $$('.roles button').forEach(b=>{b.setAttribute('aria-pressed',b.dataset.role===S.role);b.textContent=S.names[b.dataset.role]+' · '+{emp:'موظف',mgr:'مدير',haya:'تطوير'}[b.dataset.role]});")
rep(" if(a==='closeModal'){$('#modal').classList.remove('on')}"," if(a==='closeModal'){$('#modal').classList.remove('on')}\n if(a==='logout'){S.logged=false}")
# old document submit handler conflicts
rep("document.addEventListener('submit',e=>e.preventDefault());\n","")
open('v3.html','w',encoding='utf8').write(s);print('ok')
