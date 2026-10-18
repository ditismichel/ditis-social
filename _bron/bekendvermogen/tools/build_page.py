#!/usr/bin/env python3
"""Bouwt bekendvermogen/index.html uit _bron/bekendvermogen/body.html,
met stijl en scripts uit kadoburo/index.html (het sjabloon).
Aanroep: python3 -I _bron/bekendvermogen/tools/build_page.py [duur m:ss]
"""
import os, re, sys, pathlib

D = pathlib.Path("/Users/michelgoulmy/Sites/ditis-social")
tpl = (D / "kadoburo/index.html").read_text()
body = (D / "_bron/bekendvermogen/body.html").read_text()
duur = sys.argv[1] if len(sys.argv) > 1 else "1:15"
m, s = duur.split(":")
duurlang = f"{int(s)} seconden" if int(m) == 0 else f"{int(m)} minuut {int(s)}"

style = tpl[tpl.index("<style>"):tpl.index("</style>")]
extra = """
/* Bekend Vermogen: team en referenties */
.team{display:grid;gap:14px;grid-template-columns:repeat(2,minmax(0,1fr));margin:6px 0 4px}
@media (min-width:760px){.team{grid-template-columns:repeat(4,minmax(0,1fr))}}
.team figure{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:10px}
.team img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:14px;background:#EEF2F6}
.team figcaption{font-size:14px;color:var(--muted);padding:8px 4px 2px}
.team figcaption b{display:block;font:800 18px "Host Grotesk",sans-serif;color:var(--head)}
.refs{display:grid;gap:16px}
@media (min-width:760px){.refs{grid-template-columns:1fr 1fr}}
.ref{display:block;text-decoration:none;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:22px;padding:12px}
.ref img{width:100%;aspect-ratio:16/10;object-fit:cover;object-position:top;border-radius:14px;border:1px solid var(--line)}
.ref b{display:block;font:800 21px "Host Grotesk",sans-serif;color:var(--head);margin:12px 6px 2px}
.ref span{display:block;font-size:15px;color:#2A3B57;margin:0 6px 6px}
.ref:hover b{text-decoration:underline}
.bug .stats{grid-template-columns:repeat(2,minmax(0,1fr))}
.over{display:grid;gap:26px;align-items:start}
@media (min-width:900px){.over{grid-template-columns:1fr 1fr}}
.over figure{margin:0}
.over img{width:100%;height:auto;border-radius:22px}
.over figcaption{font-size:13.5px;color:var(--muted);margin-top:8px}
.over .stats{grid-template-columns:repeat(2,minmax(0,1fr))}
.over .stat b{font-size:26px}
.pills{display:flex;flex-wrap:wrap;gap:10px}
@media (min-width:640px){.seg{grid-template-columns:repeat(2,1fr)}}
@media (min-width:760px){.stats.drie{grid-template-columns:repeat(3,minmax(0,1fr))}}
.by img[src$=".svg"]{background:var(--surface);padding:10px}
"""

# pixel-afspeelknop en WhatsApp-icoon letterlijk uit het sjabloon
pixel = re.search(r'<span class="pb">(<svg viewBox="84.4.*?</svg>)</span>', tpl, re.S).group(1)
wa = re.search(r'(<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10.*?</svg>)', tpl, re.S).group(1)

prijs = os.environ.get("PRIJS", "Eén vaste prijs, gefactureerd in 2026. <mark>[bedrag invullen]</mark>")
body = (body.replace("__PRIJS__", prijs).replace("__PIXEL__", pixel).replace("__WA__", wa)
            .replace("__DUURLANG__", duurlang).replace("__DUUR__", duur))

scripts = tpl[tpl.index("<script>\n(function(){\n  var B="):]
# staafdiagram met eigen cijfers
scripts = re.sub(r'var B=\[\[.*?\]\];',
    'var B=[["belastingadvies-groningen.nl",2523],["zzp-boekhouder.nl",1459],["wezp.nl",551],["welkombijbas.nl",91],["deboekhoudbazen.nl",25],["bekendvermogen.nl",21]];',
    scripts, count=1, flags=re.S)
# filterdemo van Kadoburo eruit
a = scripts.index("<script>\n/* Filterdemo")
b = scripts.index("/* Afspraak plannen")
scripts = scripts[:a] + "<script>\n" + scripts[b:]
# afspraakopties voor Bekend Vermogen
scripts = re.sub(r",\n    nv:''\n  \};", "\n  };", scripts)
scripts = re.sub(r"var ALT=\{.*?\n  \};", "var ALT={};", scripts, count=1, flags=re.S)
scripts = scripts.replace("var PAGE='kadoburo'", "var PAGE='bekendvermogen'")

head = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Bekend Vermogen. Dit is ABC.</title>
<meta name="description" content="Wat ditisABC zag op bekendvermogen.nl, en hoe jullie gevonden worden.">
<meta property="og:title" content="Bekend Vermogen. Dit is ABC.">
<meta property="og:description" content="Ons antwoord op jouw vraag over een nieuwe website, in een korte video.">
<meta property="og:image" content="https://www.ditis.website/bekendvermogen/media/poster.jpg">
<meta property="og:url" content="https://www.ditis.website/bekendvermogen/">
"""
out = head + style + extra + "</style>\n</head>\n<body>\n\n" + body + "\n" + scripts
# videoknop-script uit het sjabloon (klik = afspelen)
out = out.replace('<div class="dur">Met geluid kijken. Ondertitels staan in beeld.</div>',
    '<div class="dur">Met geluid kijken. Ondertitels staan in beeld.</div>\n    <script>(function(){var w=document.getElementById("vwrap"),v=w.querySelector("video");function go(){w.classList.add("speelt");v.controls=true}w.querySelector(".vplay").addEventListener("click",function(){go();var p=v.play();if(p&&p.catch)p.catch(function(){})});v.addEventListener("play",go)})();</script>', 1)
assert "__" not in out.replace("__vercel", ""), "placeholder over"
(D / "bekendvermogen/index.html").write_text(out)
print("geschreven", len(out), "tekens, duur", duur)
