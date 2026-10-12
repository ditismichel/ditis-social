// Meldt per mail wanneer een pitchpagina op ditis.social bekeken wordt.
// Env: RESEND_API_KEY (verplicht), NOTIFY_TO, NOTIFY_FROM (optioneel).
const EVENTS = {
  open: 'pagina geopend',
  play: 'video gestart',
  p25: 'video 25% bekeken',
  p50: 'video 50% bekeken',
  p100: 'video helemaal bekeken',
  reel: 'voorbeeldreel gestart',
  carr: 'door de carrousel geswiped',
  bel: 'op bellen geklikt',
  app: 'op WhatsApp geklikt',
  mail: 'op mailen geklikt',
};

function apparaat(ua) {
  ua = ua || '';
  const os = /iPhone/.test(ua) ? 'iPhone' : /iPad/.test(ua) ? 'iPad' : /Android/.test(ua) ? 'Android'
    : /Macintosh/.test(ua) ? 'Mac' : /Windows/.test(ua) ? 'Windows' : /Linux/.test(ua) ? 'Linux' : 'onbekend';
  const br = /Edg\//.test(ua) ? 'Edge' : /OPR\//.test(ua) ? 'Opera' : /CriOS|Chrome\//.test(ua) ? 'Chrome'
    : /FxiOS|Firefox\//.test(ua) ? 'Firefox' : /Safari\//.test(ua) ? 'Safari' : 'onbekende browser';
  const inApp = /LinkedInApp/.test(ua) ? ' (LinkedIn-app)' : /FBAN|FBAV|Instagram/.test(ua) ? ' (Meta-app)'
    : /WhatsApp/.test(ua) ? ' (WhatsApp)' : /GoogleImageProxy|via ggpht/.test(ua) ? ' (Gmail-proxy)' : '';
  return `${os}, ${br}${inApp}`;
}

function esc(s) { return String(s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }

module.exports = async (req, res) => {
  if (req.method !== 'POST') { res.statusCode = 405; return res.end(); }
  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  if (!body || typeof body !== 'object') {
    const chunks = []; for await (const c of req) chunks.push(c);
    try { body = JSON.parse(Buffer.concat(chunks).toString() || '{}'); } catch { body = {}; }
  }
  const page = String(body.page || '').toLowerCase();
  const ev = String(body.e || '');
  if (!/^[a-z0-9-]{2,40}$/.test(page) || !EVENTS[ev]) { res.statusCode = 400; return res.end('bad'); }

  const ua = req.headers['user-agent'] || '';
  if (/bot|crawl|spider|preview|facebookexternalhit|slurp|headless/i.test(ua)) { res.statusCode = 204; return res.end(); }

  const h = req.headers;
  const dec = v => { try { return decodeURIComponent(v || ''); } catch { return v || ''; } };
  const plaats = [dec(h['x-vercel-ip-city']), h['x-vercel-ip-country-region'], h['x-vercel-ip-country']].filter(Boolean).join(', ') || 'onbekend';
  const tijd = new Date().toLocaleString('nl-NL', { timeZone: 'Europe/Amsterdam', weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' });
  const bron = String(body.ref || '').slice(0, 200) || 'direct (link uit mail of app, of zelf getypt)';
  const sid = String(body.sid || '').replace(/[^a-z0-9]/gi, '').slice(0, 8) || '?';

  const key = process.env.RESEND_API_KEY;
  if (!key) { res.statusCode = 500; return res.end('RESEND_API_KEY ontbreekt'); }
  const to = (process.env.NOTIFY_TO || 'michel@ditisabc.nl').split(',').map(s => s.trim());
  const from = process.env.NOTIFY_FROM || 'ditis.social <melding@ditis.social>';
  const subject = `ditis.social/${page}: ${EVENTS[ev]}`;
  const rows = [['Wat', EVENTS[ev]], ['Wanneer', tijd], ['Waar (bij benadering)', plaats], ['Apparaat', apparaat(ua)], ['Gekomen via', bron], ['Bezoek-ID', sid]];
  const html = `<div style="font-family:Arial,sans-serif;font-size:14px;color:#3d4347">
<p style="font-size:16px"><b>ditis.social/${esc(page)}</b>: ${esc(EVENTS[ev])}</p>
<table cellpadding="6" style="border-collapse:collapse">${rows.map(([k, v]) => `<tr><td style="color:#6b7378">${esc(k)}</td><td>${esc(v)}</td></tr>`).join('')}</table>
<p style="color:#6b7378;font-size:12px">Zelfde bezoek-ID = zelfde bezoek. Locatie is gebaseerd op het internetadres en kan een paar plaatsen afwijken.</p></div>`;
  const text = rows.map(([k, v]) => `${k}: ${v}`).join('\n');

  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from, to, subject, html, text }),
  });
  if (!r.ok) { res.statusCode = 502; return res.end('resend ' + r.status + ' ' + (await r.text()).slice(0, 300)); }
  res.statusCode = 204; res.end();
};
