s=open('v4.html',encoding='utf8').read()
def rep(a,b,cnt=1):
    global s
    assert a in s,'MISSING: '+a[:80]; s=s.replace(a,b,cnt)
# app block
a=s.index('/* ---------- APP state ----------');b=s.rindex('/* login */')
s=s[:a]+open('app_block.js',encoding='utf8').read()+s[b:]
# house with scale/theme
rep("function house(i,on){const W=60,H=56+i*30,top=12,c=on?'#A4643C':'#2A3F35',d=on?'#7E4626':'#22352C',w=on?'#F3C86B':'#3A5146';let o=`<svg width=\"${W}\" height=\"${H+top+8}\" viewBox",
"function house(i,on,k=1,light=false){const W=60,H=56+i*30,top=12,c=on?'#A4643C':light?'#EADFCB':'#2A3F35',d=on?'#7E4626':light?'#DCCDB3':'#22352C',w=on?'#F3C86B':light?'#D6C6AA':'#3A5146';let o=`<svg width=\"${(W*k).toFixed(1)}\" height=\"${((H+top+8)*k).toFixed(1)}\" viewBox")
rep("o+=`<rect x=\"${W/2-7}\" y=\"${top+H-24}\" width=\"14\" height=\"24\" rx=\"1\" fill=\"${on?'#2F6B60':'#1C2D26'}\"/><polygon points=\"${W/2-3},${top+H-14} ${W/2},${top+H-19} ${W/2+3},${top+H-14}\" fill=\"${on?'#F1E7D6':'#3A5146'}\"/>`;",
"o+=`<rect x=\"${W/2-7}\" y=\"${top+H-24}\" width=\"14\" height=\"24\" rx=\"1\" fill=\"${on?'#2F6B60':light?'#D2C1A4':'#1C2D26'}\"/><polygon points=\"${W/2-3},${top+H-14} ${W/2},${top+H-19} ${W/2+3},${top+H-14}\" fill=\"${on?'#F1E7D6':light?'#E9DECB':'#3A5146'}\"/>`;")
rep("for(let k=0;k<3;k++){const x=4+k*18,st=2.6;","for(let q=0;q<3;q++){const x=4+q*18,st=2.6;")
rep("for(let k=0;k<4;k++)o+=`<rect x=\"${6+k*14}\" y=\"${top+8}\" width=\"5\" height=\"4\" fill=\"#4A2B17\"/>`;","for(let q=0;q<4;q++)o+=`<rect x=\"${6+q*14}\" y=\"${top+8}\" width=\"5\" height=\"4\" fill=\"${on?'#4A2B17':light?'#CDBB9C':'#1A2A23'}\"/>`;")
# drawer header + bell
rep('<div class="dh"><div><span class="mut" style="color:#C3B8A6">تحدي · تقارير الأداء بالذكاء الاصطناعي</span><h2 id="dt">تقرير أداء المستودع الأسبوعي</h2></div>','<div class="dh"><div><span class="mut" id="dkind" style="color:#C3B8A6"></span><h2 id="dt"></h2></div>')
rep('<a class="back" href="#top">عن دبره</a><a class="back" href="#login" data-act="logout">تسجيل الخروج</a>','<a class="back" href="#top">عن دبره</a><a class="back" href="#login" data-act="logout">تسجيل الخروج</a><span class="bellw"><button class="bell" id="bell" aria-label="التنبيهات" aria-expanded="false">'+'__BELL__'+'<span id="bellN" class="bn"></span></button><div class="npanel" id="npanel" hidden></div></span>')
rep('__BELL__','<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 16V11a6 6 0 1112 0v5l2 2H4z"/><path d="M10 20a2 2 0 004 0"/></svg>')
# login: remove goal, greeting
rep(",['goal','الوظيفة اللي تطمح لها','select',['مخطط عمليات','مدير عمليات','محلل بيانات تشغيلية']]","")
rep("toast(`هلا ${S.names[role]}، سجّلت دخولك`)","toast(`حياك ${S.names[role]}، سجّلت دخولك`)")
# css
css=r'''
.bellw{position:relative}
.bell{position:relative;width:44px;height:44px;border-radius:50%;border:0;background:rgba(241,231,214,.08);color:var(--jes);display:grid;place-items:center}
.bn{position:absolute;top:4px;inset-inline-end:4px;min-width:18px;height:18px;border-radius:9px;background:var(--teen);color:#fff;font-size:11px;font-weight:700;display:grid;place-items:center;padding:0 4px}
.npanel{position:absolute;top:52px;inset-inline-start:0;width:min(320px,86vw);background:var(--card);color:var(--ink);border-radius:20px;box-shadow:var(--shD);padding:8px;z-index:30}
.ni{padding:12px 14px;border-radius:14px}.ni+.ni{border-top:1px solid var(--line)}.ni b{display:block;font-size:13px;color:var(--teenD)}.ni span{font-size:14.5px}
.legend{display:grid;gap:8px;margin-top:14px}.legend div{display:flex;align-items:center;gap:10px;justify-content:space-between;font-size:14px;color:var(--mut)}
.frs{display:inline-flex;gap:1px}
.hrow{display:inline-flex;gap:3px;align-items:flex-end}
.hm{position:relative;display:inline-flex;align-items:flex-end;padding-bottom:8px}
.hm.req::after{content:"";position:absolute;bottom:0;left:50%;width:7px;height:7px;margin-left:-3.5px;border-radius:50%;background:var(--sand)}
.hlegend{display:flex;align-items:center;gap:6px;margin:-6px 0 6px;font-size:13px}.hlegend .hm{padding:0}
.auto{background:#EEF5F1;border-radius:14px;padding:12px 14px;color:#1D4D42}.auto b{display:block}
.uc .new{background:#E6F1EA;outline:2px solid #9CC7AE}
.uc div span{display:block}
.mhero{padding-bottom:0;overflow:hidden}
.garden{margin:20px calc(-1*clamp(18px,2.4vw,28px)) 0;background:linear-gradient(180deg,rgba(14,26,23,0) 0%,#142A20 60%,#1E3A2B 100%);padding:14px clamp(18px,2.4vw,28px) 0;position:relative}
.garden::after{content:"";position:absolute;inset-inline:0;bottom:0;height:26px;background:#5B3A22;opacity:.55}
.gtitle{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}.gtitle span{color:#C3B8A6;font-size:14px}
.gpalms{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:6px;align-items:end;position:relative;z-index:1}
@media(max-width:640px){.gpalms{grid-template-columns:repeat(3,minmax(0,1fr))}}
.gp{text-align:center;padding-bottom:6px}.gp .gs svg{width:100%;height:150px}.gp b{display:block;font-size:14px}.gp span{font-size:12px;color:#E3C48F}
.tiles{margin:16px 0;gap:12px}.tiles>div{background:#F7EFE2;border-radius:18px;padding:14px;display:flex;flex-direction:column;gap:2px}.tiles b{font-size:22px}
.preview{background:#FBF7EF;border:1px solid var(--line);border-radius:16px;padding:14px 16px;white-space:pre-wrap;font:15px/1.8 'IBM Plex Sans Arabic',sans-serif;max-height:230px;overflow:auto;margin:0}
.quote{background:#FBF7EF;border-radius:14px;padding:12px 14px;margin:0;border-inline-start:0}
.crits{display:grid;gap:8px;margin-top:6px}
.crit{display:flex;gap:12px;align-items:flex-start;background:#F7EFE2;border-radius:14px;padding:10px 12px}
.crit b{display:block;font-size:15px}.crit .mut{font-size:13.5px}
.ci{flex:none;width:28px;height:28px;border-radius:50%;display:grid;place-items:center;background:#E6DAC6;color:var(--mut);font-weight:700;font-size:13px}
.crit.p{background:#E3F0E8}.crit.p .ci{background:var(--ok);color:#fff}
.crit.f{background:#F8E3D9}.crit.f .ci{background:#B4532E;color:#fff}
.rescard{margin-top:14px;background:var(--card);border:1.5px solid #B9D6C4;border-radius:18px;padding:14px}.rescard.bad{border-color:#E6B9A4}
.gap{border-top:1px solid var(--line)}.gap:first-of-type{border-top:0}
.gap>button{width:100%;display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr) auto;gap:14px;align-items:center;background:none;border:0;text-align:start;padding:14px 4px;min-height:60px;border-radius:14px}
.gap>button:hover{background:#F7EFE2}.gap>button>span:first-child b{display:block}
.gbar{height:10px;border-radius:5px;background:#EADFCB;overflow:hidden}.gbar i{display:block;height:100%;background:linear-gradient(90deg,var(--teen),var(--teenL));border-radius:5px;transition:width 1.2s var(--ease)}
.gap .more,.plan .more{display:grid;grid-template-rows:0fr;transition:grid-template-rows .5s var(--ease)}.gap.open .more{grid-template-rows:1fr}.gap .more>div{overflow:hidden}.gap.open .chev{transform:rotate(180deg)}.gap .chev{transition:transform .4s var(--ease);color:var(--mut)}
.names{display:grid;gap:6px;padding:0 4px 14px}
.nmrow{display:flex;justify-content:space-between;align-items:center;gap:10px;background:#F7EFE2;border-radius:12px;padding:8px 12px;font-size:14.5px}.nmrow>span:first-child b{display:block}
.plan{background:#FBF7EF;border:1px solid var(--line);border-radius:18px;padding:16px;margin-top:14px}
.sim{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:12px;padding-top:12px;border-top:1px dashed var(--line)}
.track{display:grid;gap:6px;margin-top:12px}.tp{display:flex;align-items:center;gap:10px}
.drawer.wide{width:min(720px,100%)}
.ptabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}
.ptabs button{min-height:44px;border-radius:999px;border:1.5px solid var(--line);background:var(--card);padding:0 14px;font-size:14px}
.ptabs button[aria-selected=true]{background:var(--night);color:var(--jes);border-color:var(--night)}
.ptabs button[disabled]{opacity:.45}
.pinfo{background:#F1E7D6;border-radius:16px;padding:12px 14px;display:grid;gap:2px;margin-bottom:12px}
.dept{background:var(--card);border-radius:18px;padding:6px 12px 10px;margin-bottom:10px;box-shadow:0 1px 2px rgba(0,0,0,.05)}
.dh2{display:flex;align-items:center;gap:10px;min-height:48px;font-size:16px;cursor:pointer}
.emprow{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:12px;align-items:center;min-height:48px;padding:4px 6px;border-top:1px solid var(--line);cursor:pointer}
.emprow b{display:block;font-weight:500}.emprow .mut{font-size:13px}.cost{white-space:nowrap}
.dept input,.emprow input{width:20px;height:20px;accent-color:var(--teen)}
.sum{position:sticky;bottom:-20px;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;background:var(--night);color:var(--jes);border-radius:18px;padding:14px;margin-top:8px}
.sum div{display:flex;flex-direction:column}.sum .mut{color:#C3B8A6;font-size:12.5px}.sum b{font-size:15px;white-space:nowrap}
@media(max-width:640px){.sum{grid-template-columns:repeat(2,minmax(0,1fr))}}
.qz{text-align:start;display:grid;gap:10px;margin-top:12px}
.qz fieldset{border:1px solid rgba(241,231,214,.15);border-radius:16px;padding:10px 14px}
.qz legend{font-weight:700;padding:0 6px}
.qz label{display:flex;align-items:center;gap:10px;min-height:40px;cursor:pointer}
.qz input{width:18px;height:18px;accent-color:var(--sand)}
.modal .box{position:relative;overflow:hidden;max-width:460px;max-height:92vh;overflow-y:auto}
#conf{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:2}
.celeb{position:relative;z-index:1;cursor:pointer}
.ladder .rung{flex:1 1 220px}
.skill>button{grid-template-columns:minmax(0,1.5fr) auto minmax(0,.9fr) auto}
'''
rep('</style>',css+'</style>')
open('v4.html','w',encoding='utf8').write(s);print('ok')
