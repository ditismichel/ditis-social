#!/usr/bin/env node
// Maakt van een HTML-fragment een pagina met wachtwoord.
// De inhoud wordt versleuteld (PBKDF2-SHA256 + AES-256-GCM) en pas in de browser
// ontsleuteld. In de publieke repo staat dus alleen de versleutelde tekst.
//
// Aanroep (wachtwoord nooit in de repo of in dit script zetten):
//   WACHTWOORD='...' node _bron/_tools/versleutel-pagina.js _prive/<slug>/inhoud.html <slug>/index.html <slug> "<klantnaam>"
//
// De bron (_prive/) staat in .gitignore en .vercelignore. Lettertypen en logo staan
// los in <slug>/fonts en <slug>/media; die zijn niet vertrouwelijk.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const [, , bron, uit, slug, klant] = process.argv;
const ww = (process.env.WACHTWOORD || '').trim();
if (!bron || !uit || !slug || !ww) {
  console.error('Gebruik: WACHTWOORD=... node versleutel-pagina.js <inhoud.html> <uit/index.html> <slug> "<klantnaam>"');
  process.exit(1);
}
if (!/^[a-z0-9-]{2,40}$/.test(slug)) { console.error('Ongeldige slug'); process.exit(1); }

const ITER = 600000;
const tekst = fs.readFileSync(bron, 'utf8');
const salt = crypto.randomBytes(16);
const iv = crypto.randomBytes(12);
const sleutel = crypto.pbkdf2Sync(ww, salt, ITER, 32, 'sha256');
const c = crypto.createCipheriv('aes-256-gcm', sleutel, iv);
const data = Buffer.concat([c.update(tekst, 'utf8'), c.final(), c.getAuthTag()]);
const D = JSON.stringify({ s: salt.toString('base64'), iv: iv.toString('base64'), c: data.toString('base64'), n: ITER });

const html = `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Rapportage | ditisABC</title>
<style>
@font-face{font-family:"Host Grotesk";src:url(fonts/hostgrotesk.woff2) format("woff2");font-weight:300 800;font-display:swap}
@font-face{font-family:Geist;src:url(fonts/geist.woff2) format("woff2");font-weight:100 900;font-display:swap}
:root{--bg:#F5FBFF;--head:#003E99;--ink:#0B1B33;--blue:#418EFF}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Geist,system-ui,-apple-system,"Segoe UI",sans-serif;font-size:16px;line-height:1.5}
a{color:#275599}
.slot{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px 16px}
.slot .kaart{background:#fff;border-radius:26px;padding:32px 28px;max-width:440px;width:100%;box-shadow:0 1px 0 rgba(0,62,153,.06)}
.slot img{width:160px;height:auto;display:block;margin:0 0 28px}
.slot h1{font-family:"Host Grotesk",system-ui,sans-serif;font-weight:800;color:var(--head);font-size:32px;line-height:1.14;margin:0 0 10px}
.slot p{margin:0 0 20px}
.slot label{display:block;font-weight:600;margin:0 0 6px}
.slot input{width:100%;font:inherit;padding:12px 14px;border:2px solid #8DBBFF;border-radius:12px;background:#fff;color:var(--ink)}
.slot input:focus-visible{outline:3px solid #FCB72B;outline-offset:2px;border-color:var(--head)}
.slot button{margin-top:14px;width:100%;font:inherit;font-weight:700;background:var(--head);color:#F5FBFF;border:0;border-radius:999px;padding:13px 22px;cursor:pointer}
.slot button:focus-visible{outline:3px solid #FCB72B;outline-offset:2px}
.slot button[disabled]{opacity:.7;cursor:progress}
.slot .fout{color:#8A1F11;font-weight:600;margin:12px 0 0;min-height:1.5em}
.slot .hulp{font-size:14px;color:#3b4a63;margin:18px 0 0}
</style>
</head>
<body>
<div class="slot" id="slot">
  <div class="kaart">
    <img src="media/ditisabc-logo.svg" alt="ditisABC, websites &amp; marketing" width="160" height="51">
    <h1>Rapportage${klant ? ' ' + klant.replace(/[&<>"]/g, '') : ''}</h1>
    <p>Deze pagina is beveiligd. Vul het wachtwoord in dat je van ons hebt gekregen.</p>
    <form id="f" autocomplete="off">
      <label for="ww">Wachtwoord</label>
      <input id="ww" name="ww" type="password" autocapitalize="off" autocorrect="off" spellcheck="false" required>
      <button id="knop" type="submit">Open de rapportage</button>
      <p class="fout" id="fout" role="alert" aria-live="assertive"></p>
    </form>
    <p class="hulp">Wachtwoord niet bij de hand? Bel 023-3020409 of mail naar marketing@ditisabc.nl.</p>
  </div>
</div>
<div id="inhoud" hidden></div>
<script>
(function(){
  var D=${D}, PAGE=${JSON.stringify(slug)};
  function b(x){var s=atob(x),a=new Uint8Array(s.length);for(var i=0;i<s.length;i++)a[i]=s.charCodeAt(i);return a}
  async function ontsleutel(ww){
    var km=await crypto.subtle.importKey('raw',new TextEncoder().encode(ww),'PBKDF2',false,['deriveKey']);
    var k=await crypto.subtle.deriveKey({name:'PBKDF2',salt:b(D.s),iterations:D.n,hash:'SHA-256'},km,{name:'AES-GCM',length:256},false,['decrypt']);
    return new TextDecoder().decode(await crypto.subtle.decrypt({name:'AES-GCM',iv:b(D.iv)},k,b(D.c)));
  }
  function ping(){
    try{
      var q=location.search;
      if(/[?&]ik=1/.test(q))localStorage.setItem('ditisabc-intern','1');
      if(/[?&]ik=0/.test(q))localStorage.removeItem('ditisabc-intern');
      if(localStorage.getItem('ditisabc-intern'))return;
      var sid=Math.random().toString(36).slice(2,10);
      var body=JSON.stringify({page:PAGE,e:'open',sid:sid,ref:document.referrer});
      if(navigator.sendBeacon)navigator.sendBeacon('/api/ping/',new Blob([body],{type:'application/json'}));
      else fetch('/api/ping/',{method:'POST',headers:{'Content-Type':'application/json'},body:body,keepalive:true});
    }catch(e){}
  }
  var f=document.getElementById('f'),veld=document.getElementById('ww'),knop=document.getElementById('knop'),fout=document.getElementById('fout');
  if(!(window.crypto&&crypto.subtle)){fout.textContent='Deze browser kan de pagina niet openen. Probeer een recente versie van Chrome, Safari, Edge of Firefox.';knop.disabled=true;return}
  f.addEventListener('submit',async function(ev){
    ev.preventDefault();
    fout.textContent='';knop.disabled=true;knop.textContent='Bezig met openen';
    try{
      var html=await ontsleutel(veld.value.trim());
      var el=document.getElementById('inhoud');
      el.innerHTML=html;el.hidden=false;
      document.getElementById('slot').remove();
      var h=el.querySelector('h1');if(h){document.title=h.textContent+' | ditisABC';h.setAttribute('tabindex','-1');h.focus({preventScroll:true})}
      window.scrollTo(0,0);
      ping();
    }catch(e){
      fout.textContent='Dat wachtwoord klopt niet. Probeer het opnieuw.';
      knop.disabled=false;knop.textContent='Open de rapportage';veld.select();
    }
  });
  veld.focus();
})();
</script>
</body>
</html>
`;

fs.mkdirSync(path.dirname(uit), { recursive: true });
fs.writeFileSync(uit, html);

// Controle: de zojuist geschreven pagina opnieuw ontsleutelen.
const m = JSON.parse(html.match(/var D=(\{.*?\}), PAGE=/s)[1]);
const buf = Buffer.from(m.c, 'base64');
const d = crypto.createDecipheriv('aes-256-gcm', crypto.pbkdf2Sync(ww, Buffer.from(m.s, 'base64'), m.n, 32, 'sha256'), Buffer.from(m.iv, 'base64'));
d.setAuthTag(buf.subarray(buf.length - 16));
const terug = Buffer.concat([d.update(buf.subarray(0, buf.length - 16)), d.final()]).toString('utf8');
if (terug !== tekst) { console.error('Controle mislukt: ontsleutelde tekst wijkt af'); process.exit(1); }
const lek = ['bestellingen', 'omzet', ww].filter(w => html.toLowerCase().includes(w.toLowerCase()));
console.log(`Geschreven: ${uit} (${Math.round(html.length / 1024)} kB), controle geslaagd` + (lek.length ? `; LET OP, leesbaar in de uitvoer: ${lek.length} zoekterm(en)` : '; geen leesbare inhoud of wachtwoord in de uitvoer'));
