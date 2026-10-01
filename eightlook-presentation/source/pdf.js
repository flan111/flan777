const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path=require('path');
(async()=>{
  const [,,inp,out]=process.argv;
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1920,height:1080}});
  await p.goto('file://'+path.resolve(inp));
  await p.evaluate(()=>document.fonts.ready);
  await p.waitForTimeout(500);
  await p.pdf({path:out,width:'1920px',height:'1080px',printBackground:true,preferCSSPageSize:true,margin:{top:0,right:0,bottom:0,left:0}});
  await b.close();
})();
