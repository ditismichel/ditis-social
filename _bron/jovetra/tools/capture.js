// Screenshot van een website (desktop of mobiel) voor een pitchpagina.
// node capture.js <url> <out.png|jpg> [mobiel|desktop] [volledig|scherm] [css-selector om naartoe te scrollen]
// Gebruikt puppeteer-core uit ~/ditis-kiosk en de lokale Chrome.
const puppeteer = require('/Users/michelgoulmy/ditis-kiosk/node_modules/puppeteer-core');
(async () => {
  const [url, out, mode, full, scrollSel] = process.argv.slice(2);
  const mob = mode === 'mobiel';
  const b = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', args: ['--hide-scrollbars'],
  });
  const p = await b.newPage();
  if (mob) {
    await p.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1');
    await p.setViewport({ width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  } else {
    await p.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
  }
  await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await new Promise(r => setTimeout(r, 6000));
  await p.evaluate(() => {
    const words = ['weiger', 'alleen noodzakelijk', 'decline', 'reject', 'accepteer', 'akkoord'];
    for (const el of document.querySelectorAll('button,a')) {
      const t = (el.innerText || '').toLowerCase();
      if (words.some(w => t.includes(w))) { el.click(); break; }
    }
    document.querySelectorAll('[id*=cookie],[class*=cookie],[id*=Cookiebot],[class*=cmplz],[id*=chat],[class*=chat-widget]').forEach(e => e.style.display = 'none');
  });
  if (scrollSel) { await p.evaluate(sel => document.querySelector(sel).scrollIntoView(), scrollSel); await new Promise(r => setTimeout(r, 2500)); }
  await new Promise(r => setTimeout(r, 1200));
  const opt = { path: out, fullPage: full === 'volledig' };
  if (/\.jpe?g$/.test(out)) opt.quality = 82;
  await p.screenshot(opt);
  await b.close();
})();
