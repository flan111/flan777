// Renders slides of deck/deck.html to PNG for review: node preview.js [1,2,5] [scale]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const only = process.argv[2] ? process.argv[2].split(',').map(Number) : null;
  const sc = +(process.argv[3] || 0.5);
  const out = path.join(__dirname, 'deck/prev'); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: sc });
  await p.goto('file://' + path.join(__dirname, 'deck/deck.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  const n = await p.$$eval('section.slide', s => s.length);
  for (let i = 0; i < n; i++) {
    if (only && !only.includes(i + 1)) continue;
    const el = (await p.$$('section.slide'))[i];
    await el.screenshot({ path: path.join(out, `p${String(i + 1).padStart(2, '0')}.png`) });
  }
  await b.close(); console.log('ok');
})();
