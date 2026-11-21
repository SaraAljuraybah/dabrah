s=open('v5.html',encoding='utf8').read()
def rep(a,b,cnt=1):
    global s
    assert a in s,'MISSING: '+a[:80]; s=s.replace(a,b,cnt)
a=s.index('/* ---------- APP data ----------');b=s.rindex('/* login */')
s=s[:a]+open('app_block5.js',encoding='utf8').read()+s[b:]
rep("const STN=['فسيلة','نخلة صغيرة','نخلة','نخلة مثمرة'];","const STN=['فسيلة','نخلة صغيرة','نخلة','باسقة'];")
rep('<span>نخلة</span><span>نخلة مثمرة</span>','<span>نخلة</span><span>باسقة</span>')
rep('ونخلتك تكبر من فسيلة إلى نخلة مثمرة','ونخلتك تكبر من فسيلة إلى نخلة باسقة')
css=r'''
.paths{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:18px}
@media(max-width:640px){.paths{grid-template-columns:1fr}}
.path{background:rgba(241,231,214,.07);border:1px solid rgba(241,231,214,.1);border-radius:20px;padding:16px;display:flex;flex-direction:column;gap:6px;align-items:flex-start}
.path h3{font-size:18px;margin-top:4px}.path .btn{margin-top:6px;min-height:46px}
.small{font-size:12.5px}
.garden{min-height:260px}
.gsky{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.gtitle,.gpalms{position:relative;z-index:1}
.gp{background:none;border:0;color:var(--jes);position:relative;cursor:pointer;border-radius:16px;transition:transform .4s var(--ease)}
.gp:hover,.gp:focus-visible{transform:translateY(-6px)}
.gp .tip{position:absolute;bottom:calc(100% - 20px);left:50%;transform:translate(-50%,8px);white-space:nowrap;background:var(--jes);color:var(--night);font-size:12.5px;padding:6px 10px;border-radius:999px;opacity:0;pointer-events:none;transition:all .3s var(--ease);box-shadow:var(--shD);z-index:3}
.gp:hover .tip,.gp:focus-visible .tip{opacity:1;transform:translate(-50%,0)}
.gpalms{grid-template-columns:repeat(7,minmax(0,1fr))}
@media(max-width:640px){.gpalms{grid-template-columns:repeat(4,minmax(0,1fr))}}
.hist{display:grid;gap:6px;margin-top:10px}
.hi{display:grid;grid-template-columns:auto minmax(0,1.3fr) minmax(0,1.2fr) auto;gap:12px;align-items:center;background:#F7EFE2;border-radius:14px;padding:10px 14px;font-size:14.5px}
.hi>div b{display:block}
@media(max-width:640px){.hi{grid-template-columns:auto minmax(0,1fr)}.hi>span:nth-child(3),.hi>span:last-child{grid-column:2}}
.hd{width:28px;height:28px;border-radius:50%;display:grid;place-items:center;color:#fff}.hd.ok{background:var(--ok)}.hd.no{background:#B4532E}
.impact{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.impact>div{background:rgba(241,231,214,.07);border-radius:16px;padding:12px 14px;display:flex;flex-direction:column;gap:4px}
.ia{display:flex;align-items:center;gap:10px;font:700 22px 'Kufam'}.ia .was{color:#A99E8C;font-size:17px;text-decoration:line-through}.ia .now{color:var(--sand)}.ia span{color:#A99E8C}
.filters{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin:12px 0 6px}
@media(max-width:760px){.filters{grid-template-columns:repeat(2,minmax(0,1fr))}}
.filters label{display:flex;flex-direction:column;gap:4px;font-size:13px;color:var(--mut)}
.filters select{min-height:44px;border:1.5px solid var(--line);border-radius:12px;background:#fff;padding:0 10px;font-size:15px;color:var(--ink)}
.chip.sa{background:#DDEDE6;color:#1D4D42;font-size:11.5px;padding:2px 8px;margin-inline-start:4px;vertical-align:middle}
.saprio{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;background:#E6F1EA;border-radius:16px;padding:12px 14px;margin-bottom:10px}.saprio b{color:#1D4D42}
.emprow{grid-template-columns:auto minmax(0,1fr) auto}
.certfile{display:flex;gap:12px;align-items:center;background:#F7EFE2;border-radius:14px;padding:12px 14px;margin-top:10px}.certfile b{display:block}
.qz.light fieldset{border-color:var(--line);background:var(--card)}
.qz.light{color:var(--ink)}
.qz.light input{accent-color:var(--teen)}
.wk{width:100%;border-collapse:collapse;font-size:14.5px;margin-top:10px;background:var(--card);border-radius:14px;overflow:hidden}
.wk th{background:var(--night);color:var(--jes);font-weight:500;padding:8px 10px;text-align:start}.wk td{padding:8px 10px;border-top:1px solid var(--line)}.wk .num{text-align:end;font-variant-numeric:tabular-nums}
.wk tr:nth-child(6) td{background:#FBEFD6;font-weight:700}
hr.sep{border:0;border-top:1.5px dashed var(--line);margin:22px 0}
.drawer .fld input,.drawer .fld select{width:100%}
'''
rep('</style>',css+'</style>')
open('v5.html','w',encoding='utf8').write(s);print('ok')
