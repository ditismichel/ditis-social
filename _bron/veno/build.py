#!/usr/bin/env python3
"""Bouwt veno/index.html uit body.html, extra.css en de vaste delen van de DoubleFOnline-pitch.
Aanroep: python3 -I _bron/veno/build.py"""
import pathlib, re

B = pathlib.Path("/Users/michelgoulmy/Sites/ditis-social/_bron/veno")
OUT = B.parent.parent / "veno" / "index.html"

css = (B / "basis.css").read_text()
css = css.replace("<style>", "").replace("</style>", "").strip()
css += "\n" + (B / "extra.css").read_text()
body = (B / "body.html").read_text().replace('<details class="plan" id="plan" open>', '<details class="plan" id="plan">')
vast = (B / "vast-onder.html").read_text()
scripts = (B / "scripts.html").read_text()

# klanten: webshops vooraan
order = ["offgridpowerstation", "candyfestival", "miffytown", "glansz", "thebastard", "deruijtermeubel", "de-centrale", "makelpuntculemborg", "karinbloemenstichting"]
rows = re.findall(r'    <a class="klant".*?</a>\n', vast)
def key(r):
    for i, k in enumerate(order):
        if k in r:
            return i
    return 99
vast = vast.replace("".join(rows), "".join(sorted(rows, key=key)))

# scripts: alleen afspraak + tracking (feeddemo eruit), PAGE = veno
start = scripts.find("/* Afspraak plannen")
scripts = "<script>\n" + scripts[start:]
scripts = scripts.replace("var PAGE='doublefonline'", "var PAGE='veno'")
assert "PAGE='veno'" in scripts and "doublefonline" not in scripts.lower()

bars = """<script>
(function(){
  var B=[["Nederland",645],["Noorwegen",351],["Frankrijk",317],["Duitsland",301],["Verenigde Staten",258],["Oostenrijk",180],["Zweden",161],["België",81],["Verenigd Koninkrijk",60],["Zwitserland",28]];
  var el=document.getElementById('bars'), max=B[0][1];
  B.forEach(function(b){
    var d=document.createElement('div'); d.className='bar';
    d.innerHTML='<div class="n"><span>'+b[0]+'</span><span>'+b[1].toLocaleString('nl-NL')+'</span></div><div class="b" style="width:'+Math.max(1,b[1]/max*100)+'%"></div>';
    el.appendChild(d);
  });
})();
</script>
"""

html = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Een snellere webshop voor VENO | ditisABC</title>
<meta name="description" content="Wat ditisABC zag op venostal.com, en waarom een nieuwe webshop de beste volgende stap is.">
<meta property="og:title" content="Een snellere webshop voor VENO | ditisABC">
<meta property="og:description" content="De scan van venostal.com: waar de traagheid vandaan komt, wat al sterk is, en een voorproef van de nieuwe webshop.">
<meta property="og:image" content="https://www.ditis.shop/veno/media/og.jpg">
<meta property="og:url" content="https://www.ditis.shop/veno/">
<style>
{css}
</style>
</head>
<body>

{body}
{vast}</main>

<footer><div class="wrap"><span class="claim">Hét webbureau uit de Bollenstreek</span><span>Deze pagina is alleen voor VENO bedoeld en niet vindbaar via Google.</span></div></footer>

{bars}{scripts}
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""
for bad in ["—", "kosten", "Kosten", "eerlijk", "korting", "Dit is ABC."]:
    assert bad not in html, "verboden: " + bad
OUT.write_text(html)
print("geschreven:", OUT, len(html), "tekens")
