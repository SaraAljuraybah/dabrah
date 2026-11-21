import re
s=open('v6.html',encoding='utf8').read()
def rep(a,b,cnt=1):
    global s
    assert a in s,'MISSING: '+a[:80]; s=s.replace(a,b,cnt)
a=s.index('/* ================= APP DATA ================= */');b=s.rindex('/* login */')
s=s[:a]+open('app_block7.js',encoding='utf8').read()+s[b:]
rep("const STN=['فسيلة','نخلة صغيرة','نخلة','باسقة'];","const STN=['فسيلة','نبتة','نخلة','باسقة'];")
rep('<span>فسيلة</span><span>نخلة صغيرة</span>','<span>فسيلة</span><span>نبتة</span>')
# remove unused cren + persona css
s=re.sub(r"function cren\(.*?\n",'',s,count=1)
s=re.sub(r"\.persona\{[^\n]*\n\.persona \.av\{[^\n]*\n",'',s,count=1)
# login loading state
rep("S.names[role]=$('#i-name').value.trim().split(/\\s+/)[0];S.role=role;S.logged=true;location.hash='#app';","const sb=f.querySelector('[type=submit]');sb.disabled=true;sb.textContent='جاري الدخول…';S.names[role]=$('#i-name').value.trim().split(/\\s+/)[0];S.role=role;S.logged=true;setTimeout(()=>{location.hash='#app'},350);")
css=r'''
/* v7: progressive disclosure + consistent alignment */
.disc{margin-top:12px;border-top:1px solid var(--line)}
.night .disc{border-color:rgba(241,231,214,.12)}
.disc>summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:48px;padding:6px 0;font-weight:700;color:var(--teenD)}
.night .disc>summary{color:var(--sand)}
.disc>summary::-webkit-details-marker{display:none}
.disc>summary .chev{transition:transform .4s var(--ease);color:var(--mut)}
.disc[open]>summary .chev{transform:rotate(180deg)}
.disc .dbody{padding:4px 0 6px;animation:fadeD .45s var(--ease)}
@keyframes fadeD{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}
.card>.disc:first-child{margin-top:0;border-top:0}
.kpi2{display:flex;flex-direction:column;gap:6px}.kpi2 .big{color:var(--teenD);margin:2px 0}.kpi2.night .big{color:var(--sand)}
.empty{text-align:start;padding:14px 0}.empty svg{display:block}
.legend div{text-align:start;align-items:flex-start}
.job{grid-template-columns:minmax(0,1fr) auto auto}
.plain{margin:0;padding-inline-start:18px;display:grid;gap:6px}
.ci2{flex:none;width:30px;height:30px;border-radius:50%;background:#E9B85F;color:#4A2C05;display:grid;place-items:center}
.h17{font-size:16px;margin:12px 0 6px}
.hi3{grid-template-columns:minmax(0,1fr) minmax(0,2fr) auto}
.mstart{text-align:start}.mstart .qz{margin-top:12px}
.qmsg{color:var(--sand);margin:10px 0 0}.qmsg.bad{color:#F4B29A}
.skel{height:120px;border-radius:16px;margin-top:12px;background:linear-gradient(90deg,#EFE5D3 0%,#F8F1E4 50%,#EFE5D3 100%);background-size:200% 100%;animation:sk 1s linear infinite}
@keyframes sk{to{background-position:-200% 0}}
.nine{grid-template-columns:34px repeat(3,minmax(0,1fr));grid-template-rows:repeat(3,96px) 34px}
.yax,.xax{display:flex;align-items:center;justify-content:center;color:var(--mut);font-size:13px;font-weight:700}
.yax{writing-mode:vertical-rl;transform:rotate(180deg)}
.yax span::after{content:" ↑";}
.xax span::before{content:"← ";}
.nb{border:2px solid transparent;cursor:pointer;text-align:start;justify-content:space-between;align-items:flex-start;transition:transform .35s var(--ease),border-color .3s,background .3s;font:inherit;color:inherit}
.nb:hover{transform:translateY(-3px)}.nb.sel{border-color:var(--teen);background:#FBEFE3}.nb.star.sel{background:#CFE6DB}
.nbn{font:800 30px/1 'Kufam';color:var(--ink)}
.boxd{margin-top:14px;background:#FBF7EF;border:1px solid var(--line);border-radius:18px;padding:16px;animation:fadeD .45s var(--ease)}
@media(max-width:640px){.nine{grid-template-rows:repeat(3,86px) 30px}.nbn{font-size:24px}.nbl{font-size:11.5px}}
'''
rep('</style>',css+'</style>')
s=s.replace('�','\\uFFFD')
open('v7.html','w',encoding='utf8').write(s);print('ok')
