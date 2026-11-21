s=open('v6.html',encoding='utf8').read()
def rep(a,b,cnt=1):
    global s
    assert a in s,'MISSING: '+a[:80]; s=s.replace(a,b,cnt)
a=s.index('/* ---------- APP data ----------');b=s.rindex('/* login */')
s=s[:a]+open('app_block6.js',encoding='utf8').read()+s[b:]
rep("mgr:{t:'مدير',d:'اعتمد مهارات فريقك، وتابع جاهزيتهم للترقية.'","mgr:{t:'مدير مباشر',d:'تابع فريقك وأداءهم وعبء شغلهم، ورشّح الجاهزين.'")
rep("haya:{t:'مسؤول تطوير',d:'تابع أثر التدريب، ووجّه الميزانية لمكانها الصح.'","haya:{t:'مسؤول تطوير',d:'المواهب والوظائف والتدريب والحوكمة في مكان واحد.'")
rep('<button data-role="mgr" aria-pressed="false">مدير</button>','<button data-role="mgr" aria-pressed="false">مدير مباشر</button>')
# landing: modules section before impact
mod='''<section class="sec light" id="mods">
  <div class="wrap">
    <div class="eyebrow reveal">المنصة كاملة</div>
    <h2 class="reveal">لكل شخص في المنشأة شاشته</h2>
    <p class="sub reveal">من الموظف اللي يثبت مهارته، إلى المدير اللي يقود فريقه، إلى مسؤولة التطوير اللي تخطط للمنشأة كلها.</p>
    <div class="mods">
      <div class="mod reveal"><b class="kufi">الموظف</b><ul><li>مسارين: تحدي من الشغل، أو شهادة خارجية يثبتها</li><li>جدارات بأوزان وظيفته الجاية</li><li>تقييم 360 من أكثر زملائه احتكاكًا فيه</li><li>مرشد وورش داخلية ومحتوى من شركته</li><li>فرص نقل داخلي تطابق مهاراته</li></ul></div>
      <div class="mod reveal"><b class="kufi">المدير المباشر</b><ul><li>جاهزية فريقه بالألوان من نظرة وحدة</li><li>ملف ترقية موثّق وكشف تحيز</li><li>مؤشرات الأداء وتحليل عبء العمل</li><li>التدوير الوظيفي</li><li>المهارات الحرجة و«الظل» لنقل المعرفة</li></ul></div>
      <div class="mod reveal"><b class="kufi">مسؤولة التطوير</b><ul><li>مصفوفة المواهب والتعاقب الوظيفي</li><li>تحليل الاحتياج وفتح الوظائف وإغلاقها</li><li>خطط تطوير بأولوية للسعوديين</li><li>ميزانية الأقسام من بيانات السنة الماضية</li><li>حوكمة الجدارات والتظلّمات والترقية الاستثنائية</li></ul></div>
    </div>
  </div>
</section>

'''
rep('<section class="sec" id="impact">',mod+'<section class="sec" id="impact">')
rep('<a href="#impact" data-s="impact"><i></i><span>الأثر</span></a>','<a href="#mods" data-s="mods"><i></i><span>المنصة كاملة</span></a><a href="#impact" data-s="impact"><i></i><span>الأثر</span></a>')
rep("const SECS=['top','story','name','how','try','palm','faq','impact','final'];","const SECS=['top','story','name','how','try','palm','faq','mods','impact','final'];")
css=r'''
.tabs{display:flex;gap:6px;background:#EADFCB;padding:5px;border-radius:999px;width:fit-content;max-width:100%;overflow-x:auto}
.tabs button{min-height:44px;border:0;border-radius:999px;background:transparent;padding:0 20px;font-size:15px;white-space:nowrap;transition:background .35s var(--ease),color .35s}
.tabs button[aria-selected=true]{background:var(--night);color:var(--jes);font-weight:700}
.frozen .pv{filter:saturate(.3) hue-rotate(160deg) brightness(1.05)}
.chip.ice{background:#DCEAF3;color:#21506B}
.linkbtn{background:none;border:0;color:var(--teenD);font-size:13.5px;text-decoration:underline;padding:8px 0 0;min-height:36px;text-align:start}
.mentor{display:flex;gap:14px;align-items:center;margin:10px 0}.mentor b{display:block}
.av2{width:56px;height:56px;border-radius:18px;background:var(--palm);color:#fff;display:grid;place-items:center;font:800 24px 'Kufam'}
.job{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:14px;align-items:center;padding:14px 0;border-top:1px solid var(--line)}.job:first-child{border-top:0}.job b{display:block}
.mt{text-align:center;display:flex;flex-direction:column}.mt b{font:800 24px 'Kufam'}
.cstrip{display:flex;height:16px;border-radius:8px;overflow:hidden;margin:12px 0 8px;gap:2px}
.clegend{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13px;color:var(--mut);margin-bottom:6px}.clegend i,.gdot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-inline-end:6px}
.rot{display:flex;gap:12px;align-items:center;justify-content:space-between;background:#F7EFE2;border-radius:16px;padding:12px 14px;margin-top:10px}.rot b{display:block;font-size:15px}
.crit-row{display:flex;gap:16px;align-items:center;padding:16px 0;border-top:1px solid var(--line)}.crit-row:first-child{border-top:0}
.risk{flex:none;width:76px;height:76px;border-radius:20px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:12px}.risk b{font:800 26px/1 'Kufam'}
.risk.hi{background:#F8E3D9;color:#8A2E10}.risk.md{background:#FBEFD6;color:#7A4E0F}
.nine{display:grid;grid-template-columns:28px repeat(3,minmax(0,1fr));grid-template-rows:repeat(3,minmax(110px,auto)) 28px;gap:8px;margin-top:14px}
.yax{grid-row:1/4;writing-mode:vertical-rl;transform:rotate(180deg);text-align:center;color:var(--mut);font-size:13px}
.xax{grid-column:2/5;text-align:center;color:var(--mut);font-size:13px}
.nb{background:#F7EFE2;border-radius:16px;padding:10px;display:flex;flex-direction:column;gap:6px}.nb.star{background:#DDEDE6}
.nbl{font-size:12.5px;font-weight:700;color:var(--teenD)}.nb.star .nbl{color:#1D4D42}
.dots{display:flex;flex-wrap:wrap;gap:4px}.pd{font-size:12px;background:var(--card);border-radius:999px;padding:2px 8px;box-shadow:0 1px 2px rgba(0,0,0,.06)}
.votes{display:grid;gap:6px;margin:10px 0}.vote{display:flex;justify-content:space-between;align-items:center;background:#F7EFE2;border-radius:12px;padding:6px 12px;min-height:48px}
.pos{display:flex;gap:14px;align-items:center;justify-content:space-between;padding:14px 0;border-top:1px solid var(--line);flex-wrap:wrap}.pos:first-of-type{border-top:0}.pos>div:first-child{display:flex;flex-direction:column;gap:2px;flex:1 1 320px}.pos b{font-size:16px}
.wts{display:grid;gap:12px;margin-top:14px}.wt{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1.6fr) 54px;gap:14px;align-items:center}.wt label b{display:block}.wt input{width:100%;accent-color:var(--teen);height:30px}.wv{font:800 18px 'Kufam';text-align:end}
@media(max-width:640px){.wt{grid-template-columns:1fr 54px}.wt input{grid-column:1/3;grid-row:2}}
.psum{text-align:start}.pss{display:grid;gap:4px;margin-top:14px}.ps{display:grid;grid-template-columns:minmax(0,1.3fr) auto minmax(0,.8fr);gap:10px;align-items:center;padding:6px 0;border-top:1px solid rgba(241,231,214,.1);font-size:14px}
.mods{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:36px}@media(max-width:860px){.mods{grid-template-columns:1fr}}
.mod{background:var(--card);border-radius:26px;padding:24px;box-shadow:var(--sh)}.mod b{font-size:22px;color:var(--teenD)}.mod ul{margin:12px 0 0;padding-inline-start:18px;display:grid;gap:8px;color:var(--ink)}
'''
rep('</style>',css+'</style>')
open('v6.html','w',encoding='utf8').write(s.replace('�','\\uFFFD'));print('ok')
