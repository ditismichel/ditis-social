// Screenshot van één sectie op desktop (1440) en mobiel (390), met lazy images geladen.
// node shot-section.js <url> <css-selector> <uitmap>
const puppeteer = require('/Users/michelgoulmy/ditis-kiosk/node_modules/puppeteer-core');
(async () => {
  const [url, sel, dir] = process.argv.slice(2);
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new' });
  for (const [w, h, name, s] of [[1440, 1100, 'desk', 1], [390, 844, 'mob', 2]]) {
    const p = await b.newPage();
    await p.setViewport({ width: w, height: h, deviceScaleFactor: s });
    await p.goto(url, { waitUntil: 'networkidle2' });
    await p.evaluate(() => document.querySelectorAll('img[loading=lazy]').forEach(i => (i.loading = 'eager')));
    await new Promise(r => setTimeout(r, 1500));
    const el = await p.$(sel);
    await el.screenshot({ path: `${dir}/sec-${name}.png` });
    console.log(name, 'scrollWidth', await p.evaluate(() => document.documentElement.scrollWidth));
  }
  await b.close();
})();
