const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:860}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///home/claude/proto/dabrah.html#login');await p.waitForTimeout(400);await p.click('[data-pick=emp]');await p.click('button[type=submit]');await p.waitForTimeout(1500);
await p.click('#bell');await p.waitForTimeout(300);const n0=await p.$eval('#bellN',e=>e.textContent);await p.click('#npanel [data-dis]');await p.waitForTimeout(200);const n1=await p.$eval('#bellN',e=>e.textContent);
await p.screenshot({path:'/home/claude/proto/v6-bell.png'});await p.click('#npanel [data-disall]');await p.waitForTimeout(200);const n2=await p.$eval('#bellN',e=>e.hidden);
await p.click('[data-role=mgr]');await p.waitForTimeout(1400);await (await p.$('#garden')).screenshot({path:'/home/claude/proto/v6-garden.png'});
console.log(n0,n1,'allhidden',n2,'errors',errs);await b.close()})();
