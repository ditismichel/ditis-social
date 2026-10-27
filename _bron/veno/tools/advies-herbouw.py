#!/usr/bin/env python3
"""Zet de Veno-pitch om van 'twee gelijke routes' naar 'ons advies: opnieuw bouwen' (Michel 27-10-2026).
Aanroep: python3 -I _bron/veno/tools/advies-herbouw.py"""
import pathlib, re

B = pathlib.Path("/Users/michelgoulmy/Sites/ditis-social/_bron/veno")
body = B / "body.html"
s = body.read_text()

VOORSTEL = """    <span class="kick" style="--c:var(--orange)">dit is <i></i> ons advies</span>
    <h2>Ons advies: opnieuw bouwen</h2>
    <p class="intro">De vernieuwing staat voor 2027 al op de planning. Ons advies: ga direct voor de nieuwe webshop. Opnieuw bouwen is in verhouding vaak voordeliger dan de huidige site oplappen, en snelheid, valuta, talen en dealers komen dan in één keer goed. Het nieuwe ERP nemen we vanaf de eerste dag mee.</p>
    <div class="routes">
      <div class="blok">
        <div class="hd"><div class="L t">B</div><h3>De nieuwe webshop</h3></div>
        <span class="tijd">Ons advies · live in 2027</span>
        <ul>
          <li>Eerst een verkenning: ERP-koppeling, dealerprijzen per valuta, nabestellen, en jullie vakjargon per taal.</li>
          <li>Ontwerp in jullie huisstijl, zoals de voorproef hierboven.</li>
          <li>Gebouwd voor snelheid in zes talen en alle valuta, met de bestaande topposities veilig meegenomen.</li>
          <li>Een dealeromgeving waarin dealers zelf bestellen, gekoppeld aan het nieuwe ERP.</li>
          <li>Op onze eigen servers, met hosting en technisch onderhoud: updates eerst op een testomgeving, dagelijkse back-ups, en wij volgen beveiligingsmeldingen op.</li>
        </ul>
      </div>
      <div class="blok">
        <div class="hd"><div class="L t">A</div><h3>Overbruggen tot de nieuwe site live staat</h3></div>
        <span class="tijd">Alleen als 2027 te ver weg is</span>
        <ul>
          <li>Duurt het nog even voordat de nieuwe webshop live gaat, dan nemen we op de huidige site de grootste wachttijd weg: de valuta per land zo inrichten dat pagina's kant-en-klaar klaarstaan.</li>
          <li>Hreflang en taal-labels op alle zes de taalversies, zodat Google per land de juiste pagina toont.</li>
          <li>Je site blijft er hetzelfde uitzien. Alles wat we hier leren, gaat mee naar de nieuwe webshop.</li>
        </ul>
      </div>
      <div class="blok c">
        <div class="hd"><div class="L t">C</div><h3>Daarna, doorlopend</h3></div>
        <ul>
          <li>Een woordenlijst per taal met jullie eigen vaktermen, zodat elke nieuwe vertaling klopt en vindbaar is.</li>
          <li>Vindbaarheid in Google en AI-assistenten, in de landen waar jullie dealers zitten.</li>
          <li>Doorbouwen in kleine stappen: nieuwe productlijnen, talen of dealerfuncties wanneer jullie eraan toe zijn.</li>
        </ul>
      </div>
    </div>
    <p class="note" style="font-size:16px;margin-top:18px">Wanneer de nieuwe site live moet en hoe ver het ERP is, bespreek ik graag even met je. Daarna volgt een voorstel op maat.</p>
"""
old = re.search(r'    <span class="kick" style="--c:var\(--orange\)">dit is <i></i> ons voorstel</span>\n.*?Daarna volgt een voorstel op maat.</p>\n', s, re.S)
assert old, "voorstelsectie niet gevonden"
s = s.replace(old.group(0), VOORSTEL)

rep = {
    '<a href="#voorstel" style="--c:var(--orange)"><i></i>Twee routes</a>': '<a href="#voorstel" style="--c:var(--orange)"><i></i>Ons advies</a>',
    '<h1>Sneller kan <em>nu al</em>. Nieuw kan in 2027.</h1>': '<h1>Een nieuwe webshop maakt het <em>echt</em> snel.</h1>',
    '<span>Allebei kan. Route A maakt de huidige site binnen een paar weken snel, route B bouwt de nieuwe webshop voor 2027.</span>': '<span>Vernieuwen. Opnieuw bouwen is in verhouding vaak voordeliger dan oplappen, en lost snelheid, talen en dealers in één keer op.</span>',
    'Wil je in 2027 live, dan is deze winter het moment om de route te kiezen. En de dealers die nu klagen over de snelheid, merken route A al binnen een paar weken.': 'Wil je in 2027 live, dan is deze winter het moment om te starten. Hoe eerder we beginnen, hoe eerder je dealers op een snelle webshop bestellen.',
}
for a, b in rep.items():
    assert a in s, a[:60]
    s = s.replace(a, b)
body.write_text(s)

bp = B / "build.py"
t = bp.read_text()
t = t.replace('content="Wat ditisABC zag op venostal.com, en twee routes: nu snel, of direct naar een nieuwe webshop in 2027."',
              'content="Wat ditisABC zag op venostal.com, en waarom een nieuwe webshop de beste volgende stap is."')
bp.write_text(t)
print("body en meta aangepast")
