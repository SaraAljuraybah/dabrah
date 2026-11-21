const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:860}});p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file:///home/claude/proto/dabrah.html#login');await p.waitForTimeout(400);await p.click('[data-pick=mgr]');await p.click('button[type=submit]');await p.waitForTimeout(1500);
await p.click('#bell');await p.waitForTimeout(300);console.log(await p.$eval('#npanel',e=>[e.hidden,e.innerHTML.slice(0,300)]));await b.close()})();
