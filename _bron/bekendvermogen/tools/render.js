// Rendert video.html frame voor frame (30 fps) naar een stille mp4.
// node render.js <video.html> <out.mp4> [fps] | node render.js <video.html> --stills t1 t2 ...
const puppeteer = require('/Users/michelgoulmy/ditis-kiosk/node_modules/puppeteer-core');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const [html, out, ...rest] = process.argv.slice(2);
  const b = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', args: ['--hide-scrollbars', '--allow-file-access-from-files'],
  });
  const p = await b.newPage();
  await p.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(html) + (process.env.POSTER ? '#poster' : ''), { waitUntil: 'load' });
  const shot = async t => {
    await p.evaluate(t => render(t), t);
    await p.waitForFunction('window.ready === true');
    return p.screenshot({ type: 'jpeg', quality: 92 });
  };
  if (out === '--stills') {
    for (const t of rest) {
      const buf = await shot(parseFloat(t));
      require('fs').writeFileSync(path.join(path.dirname(html), `still-${t}.jpg`), buf);
    }
    await b.close(); return;
  }
  const fps = parseInt(rest[0] || '30', 10);
  const dur = await p.evaluate(() => window.DUR);
  const n = Math.ceil(dur * fps);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) {
    const buf = await shot(i / fps);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`frame ${i}/${n}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
  console.log('klaar', out, n, 'frames');
})();
