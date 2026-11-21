const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:820},deviceScaleFactor:1});
await p.goto('file:///home/claude/proto/dabrah.html');await p.waitForTimeout(500);
await p.evaluate(()=>document.getElementById('palm').scrollIntoView());await p.waitForTimeout(1200);
for(let i=0;i<7;i++){await p.click('#growBtn')}await p.waitForTimeout(300);
await (await p.$('#palmLand')).screenshot({path:'/home/claude/proto/palm3.png'});
await p.evaluate(()=>document.getElementById('try').scrollIntoView());await p.waitForTimeout(1500);
await (await p.$('#levels')).screenshot({path:'/home/claude/proto/lv.png'});
await b.close()})();
