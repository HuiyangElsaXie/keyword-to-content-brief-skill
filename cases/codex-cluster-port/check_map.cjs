// Local headless Chromium validation. All network requests are blocked.
const fs=require('fs'); const path=require('path'); const {chromium}=require('playwright');
(async()=>{
 const root=__dirname, browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
 const context=await browser.newContext({viewport:{width:1280,height:900}});
 const requests=[]; await context.route('**/*',r=>{requests.push(r.request().url());return r.abort();});
 const page=await context.newPage(); const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.setContent(fs.readFileSync(path.join(root,'final-awareness/cluster-map.html'),'utf8'));
 const initial=await page.locator('#pages button').count();
 await page.locator('#pages button').first().click();
 const details=await page.locator('#details').textContent();
 await page.locator('#search').fill('walkthrough');const searched=await page.locator('#pages button').count();
 await page.locator('#search').fill('');await page.locator('#role').selectOption('pillar');const pillars=await page.locator('#pages button').count();
 await page.locator('#role').selectOption('');
 await page.screenshot({path:path.join(root,'map-awareness.png'),fullPage:true});
 const result={browser:'local sandbox headless Chromium',networkBlocked:true,networkRequests:requests,initialCards:initial,clickRevealsDetails:details.includes('page-001'),unmatchedSearchCards:searched,pillarFilterCards:pillars,jsErrors:errors};
 if(initial!==4||!result.clickRevealsDetails||searched!==0||pillars!==1||errors.length||requests.length)throw Error(JSON.stringify(result));
 fs.writeFileSync(path.join(root,'map-interaction-results.json'),JSON.stringify(result,null,2)+'\n');await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
