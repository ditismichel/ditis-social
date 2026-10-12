// Afspraakverzoek vanaf een pitchpagina. Mailt Michel met de details, een
// "zet in agenda"-link en een .ics-bijlage. Michel bevestigt zelf.
// Env: RESEND_API_KEY (verplicht), NOTIFY_TO, NOTIFY_FROM (optioneel).
const TYPES = {
  bel: { naam: 'Belafspraak', dur: 30, plek: 'Telefonisch' },
  hil: { naam: 'Afspraak bij ditisABC', dur: 60, plek: 'ditisABC, Satellietbaan 41A, 2181 MG Hillegom' },
  nv: { naam: 'Afspraak in de showroom', dur: 60, plek: 'Kadoburo, Boekweitstraat 82, 2153 GL Nieuw-Vennep' },
};

function esc(s) { return String(s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }
function clip(v, n) { return String(v || '').replace(/[\r\n]+/g, ' ').trim().slice(0, n); }
function z(d) { return d.toISOString().replace(/[-:]/g, '').replace(/\.\d+/, ''); }
function icsEsc(v) { return String(v).replace(/\\/g, '\\\\').replace(/;/g, '\;').replace(/,/g, '\\,').replace(/\n/g, '\\n'); }

async function readBody(req) {
  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  if (!body || typeof body !== 'object') {
    const chunks = []; for await (const c of req) chunks.push(c);
    try { body = JSON.parse(Buffer.concat(chunks).toString() || '{}'); } catch { body = {}; }
  }
  return body;
}

module.exports = async (req, res) => {
  const out = (code, obj) => { res.statusCode = code; res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(obj)); };
  if (req.method !== 'POST') return out(405, { ok: false });
  const b = await readBody(req);
  if (b.website) return out(200, { ok: true }); // honeypot

  const page = String(b.page || '').toLowerCase();
  const t = TYPES[b.type];
  const start = new Date(b.start);
  const naam = clip(b.naam, 80), tel = clip(b.tel, 30), mail = clip(b.mail, 120), opm = String(b.opm || '').trim().slice(0, 500);
  const now = Date.now();
  if (!/^[a-z0-9-]{2,40}$/.test(page) || !t || isNaN(start) || start.getTime() < now || start.getTime() > now + 90 * 864e5 || !naam)
    return out(400, { ok: false });
  if (mail && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mail)) return out(400, { ok: false });
  if (b.type === 'bel' && !tel) return out(400, { ok: false });

  const end = new Date(start.getTime() + t.dur * 60000);
  const plek = b.type === 'bel' ? `Telefonisch: Michel belt ${tel}` : t.plek;
  const titel = `${naam} (${page}): ${t.naam.toLowerCase()}`;
  const omschr = [`Aangevraagd via ditis.marketing/${page}.`, tel && `Telefoon: ${tel}`, mail && `E-mail: ${mail}`, opm && `Opmerking: ${opm}`].filter(Boolean).join('\n');

  const g = new URL('https://calendar.google.com/calendar/render');
  g.searchParams.set('action', 'TEMPLATE');
  g.searchParams.set('text', titel);
  g.searchParams.set('dates', `${z(start)}/${z(end)}`);
  g.searchParams.set('details', omschr);
  g.searchParams.set('location', plek);
  g.searchParams.set('ctz', 'Europe/Amsterdam');
  if (mail) g.searchParams.set('add', mail);

  const ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//ditisABC//afspraak//NL', 'METHOD:PUBLISH', 'BEGIN:VEVENT',
    `UID:${start.getTime()}-${page}@ditis.marketing`, `DTSTAMP:${z(new Date())}`, `DTSTART:${z(start)}`, `DTEND:${z(end)}`,
    `SUMMARY:${icsEsc(titel)}`, `LOCATION:${icsEsc(plek)}`, `DESCRIPTION:${icsEsc(omschr)}`, 'END:VEVENT', 'END:VCALENDAR'].join('\r\n');

  const fmt = o => new Intl.DateTimeFormat('nl-NL', Object.assign({ timeZone: 'Europe/Amsterdam' }, o));
  const wanneer = `${fmt({ weekday: 'long', day: 'numeric', month: 'long' }).format(start)}, ${fmt({ hour: '2-digit', minute: '2-digit' }).format(start)} tot ${fmt({ hour: '2-digit', minute: '2-digit' }).format(end)}`;

  const key = process.env.RESEND_API_KEY;
  if (!key) return out(500, { ok: false });
  const to = (process.env.NOTIFY_TO || 'michel@ditisabc.nl').split(',').map(s => s.trim());
  const from = process.env.NOTIFY_FROM || 'ditis.social <melding@ditis.social>';
  const rows = [['Wat', t.naam], ['Wanneer', wanneer], ['Waar', plek], ['Naam', naam], ['Telefoon', tel || '-'], ['E-mail', mail || '-'], ['Opmerking', opm || '-']];
  const html = `<div style="font-family:Arial,sans-serif;font-size:14px;color:#3d4347">
<p style="font-size:16px"><b>Afspraakverzoek via ditis.marketing/${esc(page)}</b></p>
<table cellpadding="6" style="border-collapse:collapse">${rows.map(([k, v]) => `<tr><td style="color:#6b7378;vertical-align:top">${esc(k)}</td><td>${esc(v)}</td></tr>`).join('')}</table>
<p><a href="${esc(g.toString())}" style="display:inline-block;background:#418EFF;color:#fff;padding:10px 16px;border-radius:8px;text-decoration:none;font-weight:bold">Zet in mijn agenda</a></p>
<p style="color:#6b7378;font-size:12px">De tijd kwam uit je vrije blokken, maar check even je agenda. ${mail ? 'Met de knop gaat er ook een uitnodiging naar ' + esc(mail) + '.' : 'Er is geen e-mail opgegeven: bevestig via telefoon of WhatsApp.'} De .ics in de bijlage werkt ook.</p></div>`;

  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from, to, subject: `Afspraakverzoek ${page}: ${t.naam.toLowerCase()}, ${wanneer}`, html,
      reply_to: mail || undefined,
      attachments: [{ filename: 'afspraak.ics', content: Buffer.from(ics).toString('base64') }],
    }),
  });
  if (!r.ok) return out(502, { ok: false });
  return out(200, { ok: true });
};
