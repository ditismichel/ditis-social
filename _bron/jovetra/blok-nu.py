#!/usr/bin/env python3
"""Eenmalig: openingsblok 'wat er al loopt' (Foome-werk) en Ahrefs-positieclaims eruit. Aanroep vanuit repo-root."""
p = '_bron/jovetra/body.html'
s = open(p).read()
blok = '''<section id="nu">
  <div class="wrap">
    <span class="kick" style="--c:var(--green-base)">dit is <i></i> wat er al loopt</span>
    <h2>Drie jaar samen aan de online marketing</h2>
    <p class="intro">Sinds 2023 verzorgt het team van Foome de online marketing van Jovetra. Elke maand een blog, posts op LinkedIn en een vaste rapportage. Foome en ditisABC gaan samen verder, dus dat werk loopt gewoon door.</p>
    <div class="stats">
      <div class="stat"><b>Sinds 2023</b><span>online marketing voor Jovetra</span></div>
      <div class="stat"><b>Elke maand</b><span>een nieuwe blog op jovetra.nl</span></div>
      <div class="stat"><b>Zo'n 15</b><span>blogs sinds begin 2025</span></div>
      <div class="stat"><b>Per kwartaal</b><span>een rapportage, en een jaarevaluatie</span></div>
    </div>
    <h3 style="font-size:26px;margin:34px 0 12px">Wat het oplevert</h3>
    <div class="list">
      <div class="li"><div class="L g">A</div><div><h3>De blogs zijn de best gevonden pagina's</h3><p>De blog over rijplaten versus draglineschotten trekt meer bezoekers uit Google dan welke andere pagina van jovetra.nl ook, de homepage inbegrepen.</p></div></div>
      <div class="li"><div class="L g">B</div><div><h3>AI gebruikt de blogs als bron</h3><p>In onze meting halen ChatGPT en Google hun antwoord over draglineschotten en kwetsbare ondergronden deels van jovetra.nl. De basis voor gevonden worden in AI ligt er dus al.</p></div></div>
      <div class="li"><div class="L g">C</div><div><h3>Korte lijnen met Ruud en Jack</h3><p>Een gedeelde contentkalender, onderwerpen die Ruud aandraagt en een belletje met Jack als er iets moet wijzigen. Zo blijven de posts dicht bij het werk van elke dag.</p></div></div>
    </div>
    <p class="note">Bezoekers per pagina: Ahrefs, oktober 2026, schattingen. AI-bronnen: onze eigen meting, 27 oktober 2026.</p>
    <div class="ask" style="margin-top:18px"><p><b>Die basis staat.</b> Wat nu remt, is de website zelf. Daar gaat de rest van deze pagina over.</p></div>
  </div>
</section>

<section class="alt" id="eerst">'''
a = '<section class="alt" id="eerst">'
assert s.count(a) == 1
s = s.replace(a, blok, 1)
R = [
    ('<a href="#eerst" style="--c:var(--orange)"><i></i>Eerst dit</a>',
     '<a href="#nu" style="--c:var(--green-base)"><i></i>Wat er al loopt</a>\n<a href="#eerst" style="--c:var(--orange)"><i></i>Eerst dit</a>'),
    ('<a class="btn o" href="#eerst">Lees de analyse</a>', '<a class="btn o" href="#nu">Lees de analyse</a>'),
    ('<b>Draglineschotten</b> <small>staan al op 1</small>', '<b>Draglineschotten</b> <small>nu al gevonden</small>'),
    ('<small>staat op 1 bij "rijplaten huren"</small>', '<small>goed vindbaar op "rijplaten huren"</small>'),
]
for x, y in R:
    assert s.count(x) == 1, x[:50]
    s = s.replace(x, y)
import re
m = re.search(r'<h3>Draglineschotten: jullie staan al bovenaan</h3><p>.*?</p>', s)
assert m
s = s.replace(m.group(0), '<h3>Draglineschotten: daar wordt Jovetra al gevonden</h3><p>Dankzij de blogs is de pagina over rijplaten versus draglineschotten de best bezochte van de site. Wat daar werkt, kan ook voor rijplaten en bouwhekken.</p>')
m = re.search(r'Op "rijplaten huren" staan sites[^<]*', s)
if m:
    s = s.replace(m.group(0), 'Ook kleinere verhuurders zijn daarop goed te vinden.')
open(p, 'w').write(s)
c = open('_bron/jovetra/extra.css').read()
if '.L.g{' not in c:
    open('_bron/jovetra/extra.css', 'w').write(c + '\n.L.g{background:var(--green);color:#fff}\n')
print('ok')
