#!/usr/bin/env python3
"""Veno-pitch: twee volwaardige routes die ook na elkaar kunnen (Michel 27-10-2026).
A = nu sneller door verhuizing naar ditisABC; B = nieuw, in verhouding voordeliger, duurt wat langer, van de grond af snel.
Aanroep: python3 -I _bron/veno/tools/routes-na-elkaar.py"""
import pathlib, re

B = pathlib.Path("/Users/michelgoulmy/Sites/ditis-social/_bron/veno")
body = B / "body.html"
s = body.read_text()

VOORSTEL = """    <span class="kick" style="--c:var(--orange)">dit is <i></i> ons voorstel</span>
    <h2>Nu sneller, of meteen nieuw. Of allebei.</h2>
    <p class="intro">Allebei kan, en ook na elkaar. Wil je dat je dealers nu al sneller bestellen, dan verhuizen we de huidige webshop naar onze servers en maken hem daar snel. Een nieuwe webshop is in verhouding voordeliger, alleen duurt het wat langer. Die bouwen we van de grond af aan snel.</p>
    <div class="routes">
      <div class="blok">
        <div class="hd"><div class="L t">A</div><h3>Nu sneller, bij ons</h3></div>
        <span class="tijd">Binnen een paar weken</span>
        <ul>
          <li>Je webshop naar een eigen server bij ons, alleen voor venostal.com, met testomgeving.</li>
          <li>De valuta per land zo inrichten dat elke pagina kant-en-klaar klaarstaat, per land en per taal.</li>
          <li>Hreflang en taal-labels op alle zes de taalversies.</li>
          <li>Scripts opschonen, beeld lichter, verspringen weg. Met een meting vooraf en achteraf.</li>
          <li>Je site blijft er hetzelfde uitzien. Kies je daarna voor route B, dan staat alles al op de goede plek.</li>
        </ul>
      </div>
      <div class="blok">
        <div class="hd"><div class="L t">B</div><h3>Meteen een nieuwe webshop</h3></div>
        <span class="tijd">In verhouding voordeliger · live in 2027</span>
        <ul>
          <li>Eerst een verkenning: dealerprijzen per valuta, nabestellen, jullie vakjargon per taal, en of de webshop aan het nieuwe ERP gekoppeld wordt.</li>
          <li>Ontwerp in jullie huisstijl, zoals de voorproef hierboven.</li>
          <li>Van de grond af aan gebouwd voor snelheid, in zes talen en alle valuta, met de bestaande topposities veilig meegenomen.</li>
          <li>Een dealeromgeving waarin dealers zelf bestellen, desgewenst gekoppeld aan het nieuwe ERP.</li>
        </ul>
      </div>
      <div class="blok c">
        <div class="hd"><div class="L t">C</div><h3>Daarna, doorlopend</h3></div>
        <ul>
          <li>Hosting en technisch onderhoud op onze eigen servers: updates eerst op de testomgeving, dagelijkse back-ups, en wij volgen beveiligingsmeldingen op.</li>
          <li>Een woordenlijst per taal met jullie eigen vaktermen, zodat elke nieuwe vertaling klopt en vindbaar is.</li>
          <li>Vindbaarheid in Google en AI-assistenten, in de landen waar jullie dealers zitten.</li>
        </ul>
      </div>
    </div>
    <p class="note" style="font-size:16px;margin-top:18px">Welke route het wordt, of eerst A en daarna B, hangt af van hoe snel je dealers sneller moeten kunnen bestellen en wanneer de nieuwe site live moet. Dat bespreek ik graag even met je. Daarna volgt een voorstel op maat.</p>
"""
old = re.search(r'    <span class="kick" style="--c:var\(--orange\)">dit is <i></i> ons advies</span>\n.*?Daarna volgt een voorstel op maat.</p>\n', s, re.S)
assert old, "adviessectie niet gevonden"
s = s.replace(old.group(0), VOORSTEL)

rep = {
    '<i></i>Ons advies</a>': '<i></i>Twee routes</a>',
    '<h1>Een nieuwe webshop maakt het <em>echt</em> snel.</h1>': '<h1>Sneller kan <em>nu al</em>. Nieuw kan in 2027.</h1>',
    '<span>Vernieuwen. Opnieuw bouwen is in verhouding vaak voordeliger dan oplappen, en lost snelheid, talen en dealers in één keer op.</span>':
        '<span>Allebei kan, ook na elkaar. Route A maakt de huidige site binnen een paar weken snel, bij ons. Route B, een nieuwe webshop, is in verhouding voordeliger en duurt wat langer.</span>',
    'Wil je in 2027 live, dan is deze winter het moment om te starten. Hoe eerder we beginnen, hoe eerder je dealers op een snelle webshop bestellen.':
        'Wil je in 2027 live, dan is deze winter het moment om te starten. En wil je dat je dealers nu al sneller bestellen, dan verhuizen we de huidige webshop binnen een paar weken.',
}
for a, b in rep.items():
    assert a in s, a[:60]
    s = s.replace(a, b)
body.write_text(s)

bp = B / "build.py"
t = bp.read_text()
t = t.replace('content="Wat ditisABC zag op venostal.com, en waarom een nieuwe webshop de beste volgende stap is."',
              'content="Wat ditisABC zag op venostal.com, en twee routes: nu sneller bij ons, of meteen een nieuwe webshop."')
bp.write_text(t)
print("routes A en B naast elkaar, ook na elkaar")
