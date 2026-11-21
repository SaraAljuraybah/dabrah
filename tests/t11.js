const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:860}});
await p.goto('file:///home/claude/proto/dabrah.html#login');await p.waitForTimeout(400);await p.click('[data-pick=mgr]');await p.click('button[type=submit]');await p.waitForTimeout(1500);
await p.evaluate(()=>{document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))});await p.waitForTimeout(900);await p.screenshot({path:'/home/claude/proto/v7-mgr-all.png',fullPage:true});
await p.click('[data-role=haya]');await p.waitForTimeout(800);await p.click('[data-act=box][data-k="2-2"]');await p.waitForTimeout(500);await p.evaluate(()=>{document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))});await p.waitForTimeout(900);await p.screenshot({path:'/home/claude/proto/v7-haya-all.png',fullPage:true});
await b.close()})();
