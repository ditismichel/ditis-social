#!/usr/bin/env python3
"""Voegt een referentieblok (USE Poultry Tech en Dutch Poultry Tech, klanten van ditisABC) toe aan de Veno-pitch.
Aanroep: python3 -I _bron/veno/tools/referenties.py"""
import pathlib

B = pathlib.Path("/Users/michelgoulmy/Sites/ditis-social/_bron/veno")
body = B / "body.html"
s = body.read_text()

BLOK = """<section class="alt" id="ervaring">
  <div class="wrap">
    <span class="kick" style="--c:var(--blue)">dit is <i></i> ervaring</span>
    <h2>Machines, vakjargon en meerdere talen: dat kennen we</h2>
    <p class="intro">Ook in de agrarische techniek bouwen we sites voor internationale verkoop. Twee voorbeelden uit de pluimveeverwerking, met machines die de hele wereld over gaan en vaktermen van slachten tot ontbenen.</p>
    <div class="refs">
      <a class="ref" href="https://use-poultry-tech.com" target="_blank" rel="noopener"><img src="media/ref-use.jpg" alt="Homepage van USE Poultry Tech" width="1000" height="625" loading="lazy"><span><b>USE Poultry Tech</b>Gebruikte machines, productielijnen en complete fabrieken voor de pluimveeverwerking, verkocht in Europa, Azië, Afrika, Amerika en het Midden-Oosten. Gebouwd door ditisABC, in zes talen, met hreflang per taal.<small>use-poultry-tech.com</small></span></a>
      <a class="ref" href="https://dutch-poultry-tech.com" target="_blank" rel="noopener"><img src="media/ref-dpt.jpg" alt="Homepage van Dutch Poultry Tech" width="1000" height="625" loading="lazy"><span><b>Dutch Poultry Tech</b>Nieuwe verwerkingslijnen en machines per procesfase, van slachten en plukken tot wegen en verpakken. Gebouwd door ditisABC, in het Engels en Spaans.<small>dutch-poultry-tech.com</small></span></a>
    </div>
  </div>
</section>

"""
anchor = '<section class="alt" id="voorstel">'
assert anchor in s and 'id="ervaring"' not in s
s = s.replace(anchor, BLOK + anchor)
nav_old = '<a href="#voorstel" style="--c:var(--orange)"><i></i>Twee routes</a>'
assert nav_old in s
s = s.replace(nav_old, '<a href="#ervaring" style="--c:var(--blue)"><i></i>Ervaring</a>\n' + nav_old)
body.write_text(s)

css = B / "extra.css"
c = css.read_text()
if ".refs{" not in c:
    c += """/* referenties */
.refs{display:grid;gap:16px}
@media (min-width:860px){.refs{grid-template-columns:1fr 1fr}}
.ref{display:grid;background:var(--bg);border:1px solid var(--line);border-radius:22px;overflow:hidden;text-decoration:none;color:var(--ink);transition:border-color .15s}
.ref:hover{border-color:var(--blue3)}
.ref img{width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;object-position:top;border-bottom:1px solid var(--line)}
.ref span{padding:18px 20px;display:grid;gap:6px;font-size:15.5px;color:#2A3B57}
.ref b{font:800 21px "Host Grotesk",sans-serif;color:var(--head)}
.ref small{font-size:13.5px;color:var(--muted)}
"""
    css.write_text(c)
print("referentieblok toegevoegd")
