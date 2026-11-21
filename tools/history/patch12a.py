import sys
P='/home/claude/proto/v11.html'
s=open(P,encoding='utf8').read()
def R(old,new,cnt=1):
    global s
    n=s.count(old)
    if n!=cnt: sys.exit(f'COUNT {n}!={cnt}: {old[:100]}')
    s=s.replace(old,new)

# ---------- houses: triangle count = level ----------
R(""" const rows=Math.min(3,1+Math.floor(i/1.4));for(let r=0;r<rows;r++)for(let q=0;q<=r;q++){const t=7,cx=W/2+(q-r/2)*(t+3),cy=top+24+r*(t*.9+3);o+=`<polygon points="${cx-t/2},${cy+t*.9} ${cx},${cy} ${cx+t/2},${cy+t*.9}" fill="${w}"/>`}
 if(i>=2){const y2=top+H*.62;for(let q=0;q<2;q++){const t=6,cx=W/2+(q?12:-12);o+=`<polygon points="${cx-t/2},${y2+t*.9} ${cx},${y2} ${cx+t/2},${y2+t*.9}" fill="${w}" opacity=".9"/>`}}""",
""" /* عدد المثلثات = رقم المستوى */
 [[1],[2],[1,2],[2,2],[2,3]][Math.min(4,i)].forEach((cnt,r)=>{for(let q=0;q<cnt;q++){const t=8,cx=W/2+(q-(cnt-1)/2)*(t+5),cy=top+24+r*(t*.9+5);o+=`<polygon points="${cx-t/2},${cy+t*.9} ${cx},${cy} ${cx+t/2},${cy+t*.9}" fill="${w}"/>`}});""")

# ---------- competencies: فنية / تقنية / سلوكية / قيادية ----------
a=s.index("const TYPES=[");b=s.index("\n",s.index("integ:{n:'النزاهة وحماية البيانات'"))
s=s[:a]+"""const TYPES=[['فنية','تُثبت بالتحديات والشهادات المطبّقة في شغل المستودع'],['تقنية','تُثبت بتحديات على الأدوات الرقمية والذكاء الاصطناعي'],['سلوكية','تُقاس بتقييم 360 من زملاء يختارهم النظام، ومؤشرات الالتزام'],['قيادية','تُقاس بتقييم 360 ومواقف قيادية فعلية']];
const SK={cap:{n:'تخطيط الطاقة الاستيعابية',t:'فنية',req:3},inv:{n:'إدارة المخزون',t:'فنية',req:4},fc:{n:'التنبؤ بالطلب',t:'فنية',req:3},
 ai:{n:'تقارير الأداء بالذكاء الاصطناعي',t:'تقنية',req:3},xl:{n:'Excel',t:'تقنية',req:3},wms:{n:'نظام إدارة المستودع (WMS)',t:'تقنية',req:3},data:{n:'تحليل البيانات ولوحات المؤشرات',t:'تقنية',req:3},
 com:{n:'التواصل الفعّال',t:'سلوكية',req:3},team:{n:'العمل الجماعي',t:'سلوكية',req:3},prob:{n:'حل المشكلات',t:'سلوكية',req:3},safe:{n:'السلامة والجودة',t:'سلوكية',req:3},cust:{n:'التوجه بالعميل',t:'سلوكية',req:3},integ:{n:'النزاهة وحماية البيانات',t:'سلوكية',req:3},
 lead:{n:'قيادة فريق المستودع',t:'قيادية',req:3},dec:{n:'اتخاذ القرار بالبيانات',t:'قيادية',req:3},dev:{n:'تطوير الآخرين ونقل المعرفة',t:'قيادية',req:3}};"""+s[b:]
R("W:{cap:15,ai:10,inv:10,xl:5,fc:5,com:6,team:6,prob:8,lead:8,dec:7,dev:5,safe:5,cust:5,integ:5}",
  "W:{cap:15,inv:12,fc:8,ai:10,xl:5,wms:5,data:5,com:4,team:4,prob:4,safe:3,cust:3,integ:2,lead:8,dec:7,dev:5}")
R("const DER={fc:i=>cl(lvOf(i,'cap')+1),","const DER={fc:i=>cl(lvOf(i,'cap')+1),wms:i=>cl(lvOf(i,'inv')),data:i=>cl(lvOf(i,'ai')+(xlOk(i)?1:0)),")
R("...['fc','com','team','prob','dec','dev','safe','cust','integ'].map(k=>","...['fc','wms','data','com','team','prob','safe','cust','integ','dec','dev'].map(k=>")
R("d:{fc:'مشتقة من تخطيط الطاقة',","d:{fc:'مشتقة من تخطيط الطاقة',wms:'من تحديات إدارة المخزون',data:'من تقاريرك واستخدامك لـExcel',")
R("plan:ok?'وصلت المطلوب.':{fc:","plan:ok?'وصلت المطلوب.':{data:'ترتفع لما تعتمد تقارير الأداء وتجدّد Excel.',wms:'ورشة «نظام إدارة المستودع المتقدم» ثم تحدي.',fc:")
R("${Object.keys(SK).length} جدارة في أربعة أنواع: فنية، سلوكية، قيادية، جوهرية.","${Object.keys(SK).length} جدارة في أربعة أنواع: فنية، تقنية، سلوكية، قيادية.")

# ---------- Hijri / Gregorian date ----------
R("const fmtD=d=>{const x=new Date(d);return isNaN(x)?esc(d):x.toLocaleDateString('ar-SA-u-ca-gregory-nu-latn',{year:'numeric',month:'long'})};",
r"""/* التاريخ: الهجري بأرقام عربية، والميلادي بأرقام إنجليزية */
const HM=['محرم','صفر','ربيع الأول','ربيع الآخر','جمادى الأولى','جمادى الآخرة','رجب','شعبان','رمضان','شوال','ذو القعدة','ذو الحجة'];
const GM=['يناير','فبراير','مارس','أبريل','مايو','يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر'];
const AR=n=>String(n).replace(/\d/g,d=>'٠١٢٣٤٥٦٧٨٩'[d]);
const hParts=d=>{const p=new Intl.DateTimeFormat('en-u-ca-islamic-umalqura-nu-latn',{year:'numeric',month:'numeric',day:'numeric',timeZone:'UTC'}).formatToParts(d);const g=t=>parseInt(p.find(x=>x.type===t).value,10);return [g('year'),g('month'),g('day')]};
const h2g=(y,m,d)=>{const est=Date.UTC(622,6,16)+((y-1)*354.367+(m-1)*29.53+(d-1))*864e5;for(let k=-6;k<=6;k++){const t=new Date(est+k*864e5);const [a,b,c]=hParts(t);if(a===y&&b===m&&c===d)return new Date(Date.UTC(t.getUTCFullYear(),t.getUTCMonth(),t.getUTCDate()))}return null};
const fmtD=(d,cal)=>{const x=new Date(d);if(isNaN(x))return esc(d);return cal==='h'?x.toLocaleDateString('ar-SA-u-ca-islamic-umalqura-nu-arab',{year:'numeric',month:'long',day:'numeric',timeZone:'UTC'}):x.toLocaleDateString('ar-SA-u-ca-gregory-nu-latn',{year:'numeric',month:'long',day:'numeric',timeZone:'UTC'})};
function dateSel(cal,v={}){const nowY=cal==='h'?hParts(new Date())[0]:new Date().getUTCFullYear(),minY=cal==='h'?1410:1990,num=n=>cal==='h'?AR(n):String(n);
 const opt=(val,txt,sel)=>`<option value="${val}" ${sel?'selected':''}>${txt}</option>`;
 const days=Array.from({length:cal==='h'?30:31},(_,i)=>opt(i+1,num(i+1),v.d===i+1)).join('');
 const months=(cal==='h'?HM:GM).map((m,i)=>opt(i+1,`${m} (${num(i+1)})`,v.m===i+1)).join('');
 let years='';for(let y=nowY;y>=minY;y--)years+=opt(y,num(y)+(cal==='h'?' هـ':''),v.y===y);
 return `<select id="cdD" aria-label="اليوم"><option value="">اليوم</option>${days}</select><select id="cdM" aria-label="الشهر"><option value="">الشهر</option>${months}</select><select id="cdY" aria-label="السنة"><option value="">السنة</option>${years}</select>`}
const readDate=()=>({d:+$('#cdD').value||0,m:+$('#cdM').value||0,y:+$('#cdY').value||0});
const toG=(cal,{y,m,d})=>{if(!y||!m||!d)return null;if(cal==='h')return h2g(y,m,d);const t=new Date(Date.UTC(y,m-1,d));return t.getUTCDate()===d?t:null};
const fromG=(cal,t)=>{if(cal==='h'){const [y,m,d]=hParts(t);return {y,m,d}}return {y:t.getUTCFullYear(),m:t.getUTCMonth()+1,d:t.getUTCDate()}};""")
R("""<div class="fld"><label for="cd">تاريخ الحصول عليها</label><input id="cd" type="date" min="1990-01-01" max="${new Date().toISOString().slice(0,10)}" value="${esc(c.date||'')}"><span class="err"></span></div></div>""",
  """</div><div class="fld" id="cdf"><span class="lbl">تاريخ الحصول عليها</span><div class="calsw" role="radiogroup" aria-label="نوع التقويم"><label><input type="radio" name="cal" value="g" ${c.cal!=='h'?'checked':''}> ميلادي</label><label><input type="radio" name="cal" value="h" ${c.cal==='h'?'checked':''}> هجري</label></div><div class="dsel" id="dsel">${dateSel(c.cal||'g',c.date?fromG(c.cal||'g',new Date(c.date)):{})}</div><span class="err" id="cde"></span></div>""")
R("""  $('#ck').onchange=e=>{""","""  $$('input[name=cal]').forEach(r=>r.onchange=()=>{const prev=r.value==='h'?'g':'h';const t=toG(prev,readDate());$('#dsel').innerHTML=dateSel(r.value,t?fromG(r.value,t):{});S.cert.cal=r.value});
  $('#ck').onchange=e=>{""")
R("""$('#ci').value='معهد سلاسل الإمداد';$('#cd').value='2026-09-15';""","""$('#ci').value='معهد سلاسل الإمداد';const cal=document.querySelector('input[name=cal]:checked').value;$('#dsel').innerHTML=dateSel(cal,fromG(cal,new Date(Date.UTC(2026,8,15))));$('#cde').textContent='';$('#cdf').classList.remove('bad');""")
R("""  chk('cd',v=>{if(!v)return 'اختر تاريخ الحصول على الشهادة';const d=new Date(v);if(isNaN(d))return 'التاريخ غير صحيح';if(d>new Date())return 'التاريخ ما يصير في المستقبل';if(d<new Date('1990-01-01'))return 'التاريخ قديم جدًا';return ''});""",
  """  const cal=document.querySelector('input[name=cal]:checked').value,dv=readDate();const gd=toG(cal,dv);const dm=!dv.d||!dv.m||!dv.y?'اختر اليوم والشهر والسنة':!gd?(cal==='h'?'هذا اليوم غير موجود في الشهر الهجري المختار':'هذا التاريخ غير موجود'):gd>new Date()?'التاريخ ما يصير في المستقبل':'';$('#cde').textContent=dm;$('#cdf').classList.toggle('bad',!!dm);if(dm){ok=false;first=first||$('#cdD')}""")
R("date:$('#cd').value.trim(),step:1}","date:gd.toISOString().slice(0,10),cal,step:1}")
R("submitCert({k:S.cert.k,title:S.cert.title,issuer:S.cert.issuer,date:S.cert.date,","submitCert({k:S.cert.k,title:S.cert.title,issuer:S.cert.issuer,date:S.cert.date,cal:S.cert.cal,")
R("cs==='ok'?`${SK[S.cert.k].n}: ${LV[S.lv[S.cert.k]-1]}`","cs==='ok'?`${SK[S.cert.k].n}: ${LV[S.lv[S.cert.k]-1]} · ${fmtD(S.cert.date,S.cert.cal)}`")

# ---------- learning: workshops & courses ----------
R("const CT=[","const COURSES=[['k1','أساسيات تحليل البيانات للمشرفين','الإثنين 7 ديسمبر · 9 ص إلى 12 م · قاعة التدريب','12 مقعد متبقي'],['k2','السلامة في المستودعات (تجديد سنوي)','الأربعاء 9 ديسمبر · أونلاين','مفتوحة'],['k3','قيادة الفرق الميدانية','14 و15 ديسمبر · قاعة التدريب','8 مقاعد متبقية']];\nconst CT=[")
R("WS.forEach(([k,n,d])=>{if(S.ws[k])it.push(['ورشة',n,d,'ws',k,0])});","WS.forEach(([k,n,d])=>{if(S.ws[k])it.push(['ورشة',n,d,'ws',k,0])});COURSES.forEach(([k,n,d])=>{if(S.courses[k])it.push(['دورة',n,d,'course',k,0])});")
a=s.index(""" <div class="g2"><div class="card reveal"><h3 style="font-size:20px">مرشدك</h3>""");b=s.index(""" <div class="card reveal"><h3 style="font-size:20px">محتوى من شركتك</h3>""",a);e=s.index("\n",b)
mentor=s[a:s.index(""" <div class="card reveal"><h3 style="font-size:20px">ورش داخلية</h3>""",a)].rstrip('\n')
content=s[b:e]
mentor_card=mentor.replace(""" <div class="g2"><div class="card reveal">""","""<div class="card reveal">""",1).rstrip()
content_card=content.strip()
new=f"""  <div class="g2">{mentor_card}
  {content_card}</div>
  <div class="card reveal"><h2 style="font-size:22px">الورش والدورات</h2>
   <h3 class="subh">ورش داخلية</h3>${{WS.map(([k,n,d])=>`<div class="nmrow" style="margin-top:8px"><span><b>${{n}}</b><span class="mut">${{d}}</span></span>${{S.ws[k]?'<span class="chip g">مسجّل</span>':`<button class="btn ghost" data-act="ws" data-k="${{k}}" style="min-height:40px;color:var(--ink)">سجّل</button>`}}</div>`).join('')}}
   <h3 class="subh">دورات مجدولة <span class="mut" style="font-weight:400;font-size:14px">· التسجيل اختياري</span></h3>${{COURSES.map(([k,n,d,seat])=>`<div class="nmrow" style="margin-top:8px"><span><b>${{n}}</b><span class="mut">${{d}} · ${{seat}}</span></span>${{S.courses[k]?'<span class="chip g">مسجّل</span>':`<button class="btn ghost" data-act="course" data-k="${{k}}" style="min-height:40px;color:var(--ink)">سجّل</button>`}}</div>`).join('')}}</div>"""
s=s[:a]+new+s[e:]
R(" cancelWorkshop(k){delete S.ws[k]},"," cancelWorkshop(k){delete S.ws[k]},\n // POST /courses/:id/registrations · DELETE /courses/:id/registrations/me\n registerCourse(k){S.courses[k]=1},cancelCourse(k){delete S.courses[k]},")
R("if(kind==='mentor')API.cancelMentor();else if(kind==='ws')API.cancelWorkshop(k);else API.setContent(k,null);","if(kind==='mentor')API.cancelMentor();else if(kind==='ws')API.cancelWorkshop(k);else if(kind==='course')API.cancelCourse(k);else API.setContent(k,null);")
R("if(kind==='mentor')API.bookMentor();else if(kind==='ws')API.registerWorkshop(k);else API.setContent(k,'saved');","if(kind==='mentor')API.bookMentor();else if(kind==='ws')API.registerWorkshop(k);else if(kind==='course')API.registerCourse(k);else API.setContent(k,'saved');")
R(" mentor(){API.bookMentor();"," course(b){API.registerCourse(b.dataset.k);render();toast('سجّلت في الدورة، وتلقاها في «تسجيلاتي»')},\n mentor(){API.bookMentor();")
R("mentorBook:false,ws:{},","mentorBook:false,ws:{},courses:{},")
R("ما سجّلت في شيء للحين. احجز جلسة مع مرشدك، أو سجّل في ورشة، أو أضف محتوى لقائمتك من تحت.","ما سجّلت في شيء للحين. احجز جلسة مع مرشدك، أو سجّل في ورشة أو دورة، أو أضف محتوى لقائمتك من تحت.")

R("/* v8 */","/* v8 */\n.calsw{display:flex;gap:18px;margin:2px 0 8px}.calsw label{display:flex;align-items:center;gap:6px;font-weight:600}.dsel{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.6fr) minmax(0,1.1fr);gap:8px}.fld.bad .dsel select{border-color:#C0502A}.fld .lbl{display:block;font-weight:700;margin-bottom:6px}.subh{font-size:17px;margin:18px 0 2px;color:var(--teenD)}",1)
assert '�' not in s
open(P,'w',encoding='utf8').write(s);print('ok')
