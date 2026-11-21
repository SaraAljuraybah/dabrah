import sys,re
P='/home/claude/proto/v11.html'
s=open(P,encoding='utf8').read()
def R(old,new,cnt=1):
    global s
    n=s.count(old)
    if n!=cnt: sys.exit(f'COUNT {n}!={cnt}: {old[:110]}')
    s=s.replace(old,new)
def cutline(start):
    """remove the whole line that contains start"""
    global s
    i=s.index(start);a=s.rindex('\n',0,i)+1;b=s.index('\n',i)+1;s=s[:a]+s[b:]

# remove learning-index machinery
cutline("/* مؤشر التعلّم: 70% عملي")
cutline("const L3=i=>{if(i===0){")
cutline("  const So=Math.min(100,25+")
cutline("  const F=Math.min(100,20+")
cutline(" return [40+(i*37)%55")
cutline("const learnIdx=i=>")
cutline("const L3SRC=")
cutline("function learnCard(i){")
cutline(" <div class=\"bars\">${[P,So,F].map((x,j)=>")
R("const byGrowth=ids=>[...ids].sort((a,b)=>(growthOf(b)-growthOf(a))||(learnIdx(b)-learnIdx(a)));",
  "const byGrowth=ids=>[...ids].sort((a,b)=>(growthOf(b)-growthOf(a))||(readyOf(b)-readyOf(a)));")
R("/* موظف الشهر: 50% التطور (15 نقطة = 100) + 50% مؤشر التعلّم */\nconst eomScore=i=>Math.round(.5*Math.min(100,growthOf(i)/15*100)+.5*learnIdx(i));",
  "/* موظف الشهر: 50% التطور (15 نقطة = 100) + 50% الجاهزية */\nconst eomScore=i=>Math.round(.5*Math.min(100,growthOf(i)/15*100)+.5*readyOf(i));")
R("/* البطل: يحقق كل الجدارات المطلوبة، والأعلى جاهزية ثم تعلّمًا */","/* البطل: يحقق كل الجدارات المطلوبة، والأعلى جاهزية ثم سعفًا */")
R("const w=[...pool].sort((a,b)=>(readyOf(b)-readyOf(a))||(learnIdx(b)-learnIdx(a)))[0];","const frOf=i=>i===0?S.fr:EMP[i].fr;const w=[...pool].sort((a,b)=>(readyOf(b)-readyOf(a))||(frOf(b)-frOf(a)))[0];")
R("تطور +${growthOf(w)} نقطة · مؤشر التعلّم ${learnIdx(w)}","تطور +${growthOf(w)} نقطة · جاهزية ${readyOf(w)}%")
R("<li>عند التعادل يتقدم الأعلى في مؤشر التعلّم.</li>","<li>عند التعادل يتقدم الأعلى جاهزية.</li>")
# drill texts
a=s.index(" if(k==='learn'||k==='learnT'||k==='learnC'){");b=s.index(" if(k==='rankd'||k==='ranka')",a);s=s[:a]+s[b:]
R("'الترتيب حسب ارتفاع الجاهزية في آخر 90 يوم، وعند التعادل مؤشر التعلّم'","'الترتيب حسب ارتفاع الجاهزية في آخر 90 يوم، وعند التعادل الأعلى جاهزية'")
R("head('موظف الشهر','(50% × التطور، و15 نقطة = 100) + (50% × مؤشر التعلّم)','حساب الجاهزية ومؤشر التعلّم')","head('موظف الشهر','(50% × التطور في آخر 90 يوم، و15 نقطة = 100) + (50% × الجاهزية)','حساب الجاهزية الأسبوعي')")
R("وأعلى جاهزية، وعند التعادل الأعلى في مؤشر التعلّم.","وأعلى جاهزية، وعند التعادل الأكثر سعفًا.")
# employee perf: remove learnCard
R("<div class=\"g2\">${learnCard(0)}${honorBoard()}</div>","${honorBoard()}")
# haya dev: remove company learning card
a=s.index("<div class=\"card reveal\"><div class=\"row between\"><h3 style=\"font-size:20px\">مؤشر التعلّم في الشركة · 70-20-10</h3>");b=s.index("\n",a);s=s[:a].rstrip(' ')+s[b+1:]
# top overview: replace learning KPI with average readiness
R("const avgL=Math.round(all.reduce((a,i)=>a+learnIdx(i),0)/N);","const avgR=Math.round(all.reduce((a,i)=>a+readyOf(i),0)/N);")
R("['متوسط مؤشر التعلّم',`${avgL}`,'70-20-10 · اضغط للتفاصيل','learnC']","['متوسط الجاهزية',`${avgR}%`,'للوظيفة التالية · اضغط للتفاصيل','readyAll']")
R(" if(k==='ready'){"," if(k==='readyAll'){return head('متوسط الجاهزية','متوسط جاهزية كل الموظفين لوظائفهم التالية','أدلة الجدارات المعتمدة و360 ومؤشرات الأداء')+list([...all].sort((a,b)=>readyOf(b)-readyOf(a)),readyOf,v=>v+'%')}\n if(k==='ready'){")
# landing
R("<li>مؤشر التعلّم 70-20-10 ودورة 30-60-90</li>","<li>دورة 30-60-90 لمتابعة تطوره</li>")
for w in ['learnIdx','L3(','L3SRC','70-20-10','learnCard']:
    if w in s: print('STILL',w,s.count(w))
open(P,'w',encoding='utf8').write(s);print('ok')
